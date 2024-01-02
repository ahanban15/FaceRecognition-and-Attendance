# ******************STEP 1: Webcam setup************************
import cv2

# Open the webcam (the default camera)
cap = cv2.VideoCapture(0)  # 0 indicates the default camera

cap.set(3, 640)
cap.set(4, 480)


# *******************STEP 2: SETUP GRAPHICS***********************

imgBackground = cv2.imread("Resources/background.png")


while True:
    success, img = cap.read()

    imgBackground[162:162+480, 55:55+640] = img

    cv2.imshow("Camera", img)
    cv2.imshow("Face attendance", imgBackground)
    cv2.waitKey(1)