# ******************STEP 1: Webcam setup************************
import os
import pickle

import bbox
import cv2
import cvzone
import face_recognition
import numpy as np

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
# go to EncodeGenerator.py

# *********************STEP 4: FACE RECOGNITION************************
file = open("EncodeFile.p", 'rb')
encodeListKnownWithIDs = pickle.load(file)
file.close()
encodeListKnown, studentIDs = encodeListKnownWithIDs



# final call to camera run
while True:
    success, img = cap.read()

    # RESIZING oUR IMAGES
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(matches)
        # print(faceDis)

        # to get the min distance wala index
        matchIndex = np.argmin(faceDis)

        # if matches[matchIndex]:
            # print("Known face detected")
            # print(studentIDs[matchIndex])

        if matches[matchIndex]:
    #         create a rect box
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = 4*y1, 4*x2, 4*y2, 4*x1
            bbox = 55+x1, 162+y1, x2-x1, y2-y1
            cvzone.cornerRect(imgBackground, bbox, rt=0)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[3]

    # cv2.imshow("Camera", img)
    # cv2.imshow("Face attendance", imgBackground)
    # cv2.waitKey(1)
