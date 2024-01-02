# ******************STEP 1: Webcam setup************************
import os

import cv2

# Open the webcam (the default camera)
cap = cv2.VideoCapture(0)  # 0 indicates the default camera

cap.set(3, 640)
cap.set(4, 480)

# *******************STEP 2: SETUP GRAPHICS***********************

imgBackground = cv2.imread("Resources/background.png")

# importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []

print(modePathList)

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

print(len(imgModeList))

# *********************STEP 3: ENCODING GENERATOR************************

# final call to camera run
while True:
    success, img = cap.read()

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeList[3]

    # cv2.imshow("Camera", img)
    cv2.imshow("Face attendance", imgBackground)
    cv2.waitKey(1)
