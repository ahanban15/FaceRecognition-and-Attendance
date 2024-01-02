# ******************STEP 1: Webcam setup************************
import cv2

# Open the webcam (the default camera)
cap = cv2.VideoCapture(0)  # 0 indicates the default camera

cap.set(3, 640)
cap.set(4, 480)

