# 🏀 Basketball Shot Analyzer

An AI-powered basketball shooting form analyzer that uses computer vision to provide real-time feedback on your shooting technique.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

This application analyzes basketball shooting form by detecting body pose and calculating the release angle at the elbow. Built with MediaPipe and Gradio, it provides instant visual feedback and actionable recommendations for improving your shot.

### Key Features

- **Real-time Pose Detection**: Uses Google's MediaPipe for accurate body tracking
- **Release Angle Analysis**: Calculates elbow angle at the optimal release point
- **Visual Feedback**: Overlays skeleton visualization on your shooting video
- **Detailed Reports**: Provides comprehensive analysis with specific recommendations
- **Easy-to-Use Interface**: Simple web UI built with Gradio - no technical knowledge required

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd basketball-shot-analyzer
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python app.py
```

The application will launch in your web browser at `http://localhost:7860`

## How to Use

1. **Record a video** of a basketball shot:
   - Ensure the shooter is clearly visible
   - Include the full shooting motion from setup to follow-through
   - Good lighting is important for accurate detection
   - Recommended: Side angle view showing the shooting arm

2. **Upload the video** to the application

3. **Choose settings**:
   - Toggle skeleton overlay on/off

4. **Click "Analyze Shot"** to process the video

5. **Review results**:
   - Watch the annotated video with pose overlay
   - Read the detailed analysis report
   - Follow the specific recommendations

## 🎓 Understanding the Analysis

### Release Angle

The **elbow angle at release** is one of the most critical aspects of shooting form:

- **Optimal Range**: 90-120 degrees
- **Too Tight (< 90°)**: Results in flat shots and reduced range
- **Too Wide (> 120°)**: Reduces control and accuracy

### How It Works

1. **Pose Detection**: MediaPipe identifies 33 body landmarks in each frame
2. **Release Point Identification**: Tracks wrist height to find the release moment
3. **Angle Calculation**: Computes elbow angle using shoulder, elbow, and wrist positions
4. **Feedback Generation**: Compares angle to optimal ranges and provides recommendations

## Technical Details

### Architecture

```
Video Input → MediaPipe Pose Detection → Angle Calculation → Analysis Report
                                       ↓
                                  Visual Overlay
```

### Key Components

- **MediaPipe Pose**: Pre-trained ML model for human pose estimation
- **OpenCV**: Video processing and frame manipulation
- **Gradio**: Web interface framework
- **NumPy**: Mathematical computations

### Performance

- Processing time: ~1-2 seconds per second of video
- Accuracy: Depends on video quality and lighting
- Supported formats: MP4, AVI, MOV, and most common video formats

## Project Structure

```
basketball-shot-analyzer/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── examples/             # Sample videos (optional)
```

## Customization

### Analyzing Left-Handed Shooters

Currently configured for right-handed shooters. To analyze left-handed shooters, modify the `analyze_release_angle()` function:

```python
# Change these lines:
right_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
right_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
right_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
```

### Adjusting Optimal Angle Range

Modify the feedback thresholds in `analyze_release_angle()`:

```python
if 90 <= elbow_angle <= 120:  # Change these values
    feedback = "✅ GOOD: Release angle is optimal!"
```

## Future Enhancements

- [ ] Left-handed shooter support toggle
- [ ] Follow-through analysis (wrist snap angle)
- [ ] Jump height measurement
- [ ] Shot arc prediction
- [ ] Multi-angle analysis (front + side views)
- [ ] Shot tracking database (track improvement over time)
- [ ] Real-time camera input (not just uploaded videos)
- [ ] Mobile app version
- [ ] Comparison with professional shooter form

## Contributing

Contributions are welcome! Areas for improvement:

1. Additional metrics (knee bend, hip rotation, etc.)
2. Better UI/UX design
3. Performance optimizations
4. Support for different sports (football, volleyball, etc.)

## Known Limitations

- Requires clear visibility of the shooter
- Best results with side-angle videos
- Currently only analyzes right-handed shooters
- Does not account for shot result (make/miss)
- Single camera angle limits 3D analysis

## Resources & References

- [MediaPipe Pose Documentation](https://google.github.io/mediapipe/solutions/pose.html)
- [Basketball Shooting Form Guide](https://www.breakthroughbasketball.com/fundamentals/shooting.html)
- [Optimal Release Angles Study](https://www.researchgate.net/publication/biomechanics-basketball-shooting)

## Author

Created by [Your Name] as a portfolio project demonstrating:
- Computer Vision / Machine Learning
- Video Processing
- Python Development
- UI/UX Design
- Sports Analytics

## License

MIT License - feel free to use this project for learning and personal use.

## Acknowledgments

- Google MediaPipe team for the pose detection model
- Gradio team for the excellent UI framework
- Basketball coaching community for form analysis insights

---

**Questions or suggestions?** Open an issue or reach out!

**Want to see it in action?** Check out the [demo video](link-to-demo) or [live deployment](link-to-deployed-app).
