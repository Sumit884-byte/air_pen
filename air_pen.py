import cv2
import numpy as np
import mediapipe as mp

# Use the new MediaPipe Tasks API
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Create the hand landmarker
base_options = python.BaseOptions(
    model_asset_path='hand_landmarker.task'
)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.8,
    min_hand_presence_confidence=0.8,
    min_tracking_confidence=0.8
)
detector = vision.HandLandmarker.create_from_options(options)

# Initialize Webcam
cap = cv2.VideoCapture(0)

# Create a blank canvas to draw on
canvas = None

# Track the previous position to draw lines
px, py = 0, 0

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # Flip for "mirror" effect

    if canvas is None:
        canvas = np.zeros_like(img)

    # Convert to RGB for MediaPipe
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Convert to MediaPipe Image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    results = detector.detect(mp_image)

    if results.hand_landmarks:
        for hand_landmarks in results.hand_landmarks:
            # Index finger tip is landmark #8
            landmark = hand_landmarks[8]
            h, w, c = img.shape
            cx, cy = int(landmark.x * w), int(landmark.y * h)

            # Check if middle finger is DOWN (to draw) or UP (to stop)
            # Landmark 12 is the middle finger tip, 10 is the second joint
            m_finger = hand_landmarks[12]
            if m_finger.y > hand_landmarks[10].y:  # Middle finger folded
                if px == 0 and py == 0:
                    px, py = cx, cy

                # Draw on the canvas
                cv2.line(canvas, (px, py), (cx, cy), (0, 255, 0), 10)
                px, py = cx, cy
            else:
                # Reset previous points if not drawing
                px, py = 0, 0
    else:
        # Reset if no hands are detected
        px, py = 0, 0

    # Combine the webcam feed with the canvas
    # 1. Create a mask of the drawing
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_canvas, 20, 255, cv2.THRESH_BINARY)
    inv_mask = cv2.bitwise_not(mask)

    # 2. Black out the area of the drawing in the original image
    img_bg = cv2.bitwise_and(img, img, mask=inv_mask)

    # 3. Add the canvas colors to the blacked-out area
    img = cv2.add(img_bg, canvas)

    cv2.imshow("Air Canvas (Close: Press 'q', Clear: Press 'c')", img)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('c'):
        canvas = np.zeros_like(img)

cap.release()
cv2.destroyAllWindows()