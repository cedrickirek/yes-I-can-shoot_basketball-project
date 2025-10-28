# 🚀 Quick Start Guide

## Setup (First Time Only)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Installation
```bash
python test_installation.py
```

You should see all green checkmarks ✅

---

## Running the Application

### Start the App
```bash
python app.py
```

The app will open in your browser at: `http://localhost:7860`

---

## Using the Application

### Step 1: Record Your Shot
- Film a basketball shot (3-pointer recommended)
- Make sure you're fully visible in the frame
- Side angle view works best
- Good lighting is important

### Step 2: Upload Video
- Click the upload area in the web interface
- Select your video file
- Supported formats: MP4, AVI, MOV

### Step 3: Analyze
- Toggle "Show Skeleton Overlay" if you want to see the pose detection
- Click "🔍 Analyze Shot"
- Wait for processing (usually 10-30 seconds)

### Step 4: Review Results
- Watch the annotated video
- Read the detailed analysis
- Follow the recommendations

---

## Tips for Best Results

✅ **DO:**
- Film from the side showing your shooting arm
- Ensure good lighting
- Keep the camera steady
- Make sure your full upper body is visible
- Film in landscape mode

❌ **AVOID:**
- Filming from directly in front or behind
- Poor lighting or shadows
- Shaky camera
- Cutting off parts of your body
- Filming in portrait mode

---

## Understanding Your Results

### Elbow Angle at Release
- **90-120°** = ✅ GOOD (Optimal)
- **80-90°** or **120-140°** = ⚠️ NEEDS MINOR ADJUSTMENT
- **< 80°** or **> 140°** = ❌ NEEDS WORK

### Common Issues & Fixes

**Angle Too Tight (< 90°)**
- **Problem**: Shooting with a bent elbow
- **Fix**: Extend your arm more at release
- **Practice**: Focus on full extension at the peak

**Angle Too Wide (> 120°)**
- **Problem**: Releasing with arm too straight
- **Fix**: Keep more bend in your elbow
- **Practice**: Work on proper follow-through

---

## Troubleshooting

### "No pose detected"
- Make sure you're fully visible in the frame
- Check lighting conditions
- Ensure camera is stable
- Try recording from a different angle

### App won't start
- Run `python test_installation.py` to check for issues
- Make sure all dependencies are installed
- Check if port 7860 is available

### Video processing is slow
- This is normal! Processing takes time
- Shorter videos = faster processing
- 10-second clips are ideal for testing

---

## Next Steps

1. ✅ Record and analyze multiple shots
2. ✅ Track your progress over time
3. ✅ Compare different shooting positions (corner, wing, top of key)
4. ✅ Share your results with coaches or teammates
5. ✅ Keep practicing!

---

## Demo Videos to Try

If you don't have a video yet, you can:
1. Find basketball shooting videos on YouTube
2. Use your phone to record a friend shooting
3. Record yourself using a tripod or phone stand

---

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review the technical details in the code comments
- Open an issue on GitHub if you find bugs

---

**Good luck improving your shot! 🏀**
