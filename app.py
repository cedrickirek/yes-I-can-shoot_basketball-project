"""
Basketball Shot Analyzer
A computer vision application that analyzes basketball shooting form using MediaPipe pose detection.
Focus: Release angle analysis for 3-point shots
"""

import gradio as gr
import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path
import tempfile
from scipy.ndimage import gaussian_filter1d

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def calculate_angle(point1, point2, point3):
    """
    Calculate angle between three points.
    Args:
        point1, point2, point3: Tuples of (x, y) coordinates
    Returns:
        Angle in degrees
    """
    # Convert points to numpy arrays
    a = np.array(point1)
    b = np.array(point2)  # vertex point
    c = np.array(point3)
    
    # Calculate vectors
    ba = a - b
    bc = c - b
    
    # Calculate angle using dot product
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    
    return np.degrees(angle)


def analyze_release_angle(landmarks, frame_width, frame_height):
    """
    Analyze the release angle of the shooting arm.
    Focuses on right arm (can be modified for left-handed shooters).
    
    Returns:
        - release_angle: The angle at the elbow during release
        - feedback: Text feedback on the shot
    """
    # Get key landmarks (right arm)
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
    
    # Convert normalized coordinates to pixel coordinates
    shoulder = (right_shoulder.x * frame_width, right_shoulder.y * frame_height)
    elbow = (right_elbow.x * frame_width, right_elbow.y * frame_height)
    wrist = (right_wrist.x * frame_width, right_wrist.y * frame_height)
    
    # Calculate elbow angle
    elbow_angle = calculate_angle(shoulder, elbow, wrist)
    
    # Provide feedback based on angle
    # Optimal release angle is typically between 90-120 degrees at the elbow
    if 90 <= elbow_angle <= 120:
        feedback = "✅ GOOD: Release angle is optimal!"
        status = "good"
    elif 80 <= elbow_angle < 90:
        feedback = "⚠️ MINOR ISSUE: Elbow angle slightly too tight. Try extending your arm more at release."
        status = "warning"
    elif 120 < elbow_angle <= 140:
        feedback = "⚠️ MINOR ISSUE: Elbow angle slightly too wide. Try keeping your elbow more bent at release."
        status = "warning"
    else:
        feedback = "❌ NEEDS WORK: Release angle is outside optimal range. Focus on proper elbow positioning."
        status = "poor"
    
    return elbow_angle, feedback, status


def process_video(video_path, show_skeleton=True):
    """
    Process video and analyze basketball shooting form.
    
    Args:
        video_path: Path to input video
        show_skeleton: Whether to overlay skeleton on output video
    
    Returns:
        - output_video_path: Path to processed video
        - analysis_text: Text analysis of the shot
    """
    if video_path is None:
        return None, "Please upload a video file."
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create temporary output video file
    output_path = tempfile.mktemp(suffix='.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Storage for analysis
    angles_data = []
    best_frame_idx = 0
    best_wrist_height = 0
    
    # First pass: Collect wrist positions
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=1
    ) as pose:
        
        frame_idx = 0
        wrist_positions = []
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            
            # Convert BGR to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Process with MediaPipe
            results = pose.process(image)
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                # Track right wrist y-position (use left if right not visible)
                right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
                left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
                
                if right_wrist.visibility > left_wrist.visibility:
                    wrist_y = right_wrist.y * height
                else:
                    wrist_y = left_wrist.y * height
                
                wrist_positions.append(wrist_y)
            else:
                wrist_positions.append(np.nan)
            
            frame_idx += 1

    cap.release()

    # Detect release frame using velocity (gradient)
    wrist_array = np.array(wrist_positions)
    dy = np.gradient(wrist_array)  # Velocity
    dy_smooth = gaussian_filter1d(np.nan_to_num(dy, nan=0.0), sigma=1.0)

    # Find fastest upward motion in middle 80% of video
    n = len(dy_smooth)
    if n > 0:
        search_start = int(n * 0.1)
        search_end = int(n * 0.9)
        search_slice = dy_smooth[search_start:search_end]
        best_frame_idx = int(np.argmin(search_slice) + search_start)
    else:
        best_frame_idx = 0

    # Second pass: annotate video and analyze
    cap = cv2.VideoCapture(video_path)

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=1
    ) as pose:
        
        frame_idx = 0
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            
            # Convert BGR to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Process with MediaPipe
            results = pose.process(image)
            
            # Convert back to BGR for OpenCV
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            if results.pose_landmarks:
                # Draw skeleton if requested
                if show_skeleton:
                    mp_drawing.draw_landmarks(
                        image,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
                    )
                
                # Analyze release angle
                landmarks = results.pose_landmarks.landmark
                angle, feedback, status = analyze_release_angle(landmarks, width, height)
                
                # Store analysis for release frame
                if frame_idx == best_frame_idx:
                    angles_data.append({
                        'frame': frame_idx,
                        'angle': angle,
                        'feedback': feedback,
                        'status': status
                    })
                
                # Add angle text to frame
                cv2.putText(image, f'Elbow Angle: {angle:.1f}°', 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (255, 255, 255), 2)
                
                # Mark release frame
                if frame_idx == best_frame_idx:
                    cv2.putText(image, 'RELEASE POINT', 
                            (width - 250, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                            1.0, (0, 0, 255), 3)
            else:
                # No pose detected
                cv2.putText(image, 'No pose detected', 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (0, 0, 255), 2)
            
            out.write(image)
            frame_idx += 1

    cap.release()
    out.release()
    
    # Generate analysis report
    if angles_data:
        # Get the analysis at the release point (highest wrist)
        release_data = angles_data[best_frame_idx] if best_frame_idx < len(angles_data) else angles_data[-1]
        
        analysis = f"""
## 🏀 Basketball Shot Analysis Report

### Release Point Analysis
**Frame:** {release_data['frame']}/{total_frames}
**Elbow Angle at Release:** {release_data['angle']:.1f}°

### Feedback
{release_data['feedback']}

### Technical Details
- **Optimal Range:** 90-120° at the elbow
- **Your Angle:** {release_data['angle']:.1f}°
- **Status:** {release_data['status'].upper()}

### Recommendations
"""
        
        if release_data['status'] == 'good':
            analysis += "- Your release angle is in the optimal range! Keep practicing this form.\n"
            analysis += "- Focus on consistency - try to replicate this angle on every shot.\n"
        elif release_data['status'] == 'warning':
            if release_data['angle'] < 90:
                analysis += "- Try extending your arm slightly more at the release point.\n"
                analysis += "- Focus on a smooth, upward motion rather than pushing the ball.\n"
            else:
                analysis += "- Keep your elbow more bent at release for better control.\n"
                analysis += "- Practice your follow-through with a higher elbow position.\n"
        else:
            analysis += "- Review proper shooting form fundamentals.\n"
            analysis += "- Practice your shot motion slowly, focusing on elbow positioning.\n"
            analysis += "- Consider recording from multiple angles for comprehensive analysis.\n"
        
        analysis += "\n### Next Steps\n"
        analysis += "1. Record multiple shots to track consistency\n"
        analysis += "2. Compare angles across different shooting positions\n"
        analysis += "3. Work on maintaining optimal form under game conditions\n"
    else:
        analysis = """
## ⚠️ Analysis Failed

Could not detect pose in the video. Please ensure:
- The shooter is clearly visible in the frame
- Good lighting conditions
- Camera is stable and at an appropriate distance
- Shooter's full body (or at least upper body) is visible

Try recording another video with better visibility!
"""
    
    return output_path, analysis


# Create Gradio interface
def create_interface():
    with gr.Blocks(title="Basketball Shot Analyzer", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🏀 Basketball Shot Analyzer
            
            Analyze your basketball shooting form using AI-powered pose detection.
            This tool focuses on **release angle analysis** - one of the most critical aspects of shooting form.
            
            ### How to use:
            1. Upload a video of a basketball shot (3-point attempt recommended)
            2. Choose whether to show the skeleton overlay
            3. Click "Analyze Shot" to get detailed feedback
            
            **Tip:** For best results, ensure the shooter is clearly visible and the shooting arm is in frame.
            """
        )
        
        with gr.Row():
            with gr.Column():
                video_input = gr.Video(label="Upload Basketball Shot Video")
                skeleton_checkbox = gr.Checkbox(
                    label="Show Skeleton Overlay",
                    value=True,
                    info="Display pose detection skeleton on the output video"
                )
                analyze_btn = gr.Button("🔍 Analyze Shot", variant="primary", size="lg")
                
                gr.Markdown(
                    """
                    ### 📊 What we analyze:
                    - **Elbow angle at release** (optimal: 90-120°)
                    - **Release point detection**
                    - **Form consistency**
                    
                    ### 🎯 Coming soon:
                    - Follow-through analysis
                    - Jump height measurement
                    - Multiple angle comparison
                    """
                )
            
            with gr.Column():
                video_output = gr.Video(label="Analyzed Video")
                analysis_output = gr.Markdown(label="Analysis Report")
        
        # Set up the analysis action
        analyze_btn.click(
            fn=process_video,
            inputs=[video_input, skeleton_checkbox],
            outputs=[video_output, analysis_output]
        )
        
        gr.Markdown(
            """
            ---
            ### 💡 Tips for Better Shooting Form:
            - **Elbow Position:** Keep your elbow under the ball, aligned with your shoulder
            - **Release Point:** Release at the peak of your jump or at full extension
            - **Follow Through:** Snap your wrist downward after release (goose neck)
            - **Consistency:** Focus on repeating the same motion every time
            
            **Note:** This tool analyzes right-handed shooters by default. Left-handed version coming soon!
            """
        )
    
    return demo


if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=False)
