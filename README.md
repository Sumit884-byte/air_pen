# Air Pen 🖋️

Air Pen is a computer vision-based application that allows you to draw in the air using your index finger and a webcam. It uses MediaPipe Hand Landmarker to track your finger movements and OpenCV to render the drawing on a virtual canvas.

## Features 🚀

- **Air Writing:** Draw smoothly on the screen using your index finger.
- **Controls:** 
  - **Draw:** Fold your middle finger and move your index finger.
  - **Stop Drawing:** Lift your middle finger.
  - **Clear Canvas:** Press `c`.
  - **Quit:** Press `q`.
- **Real-time Feedback:** See your drawing overlaid on the webcam feed.

## Prerequisites 📋

- Python 3.x
- Webcam

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/Sumit884-byte/air_pen.git
   cd air_pen
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the [Hand Landmarker Task](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task) file and place it in the project root (if it's not already there).

## Usage 💻

Run the script:
```bash
python air_pen.py
```

## How it Works 🧠

Modified MediaPipe Hand Landmarker tracks 21 hand landmarks in real-time. The script specifically tracks:
- **Index Finger Tip (Landmark 8):** Used as the pen point.
- **Middle Finger Tip (Landmark 12) & Second Joint (Landmark 10):** Comparison between these two determines the "drawing" state (folded vs. extended).

## License 📄

MIT
