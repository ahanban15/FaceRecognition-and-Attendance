# ******************STEP 1: Webcam setup************************
import os
import pickle

import bbox
import cv2
import cvzone
import face_recognition
import numpy as np

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate(
    "faceattendance-and-recognition-firebase-adminsdk-qxxb5-f986cd2945.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-and-recognition-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendance-and-recognition.appspot.com"

})

bucket = storage.bucket()

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

# *******************Step 5: DATABASE SETUP ON GOOGLE FIREBASE***************

# *******************Step 6: ADD DATA TO DATABASE from AddDataToDatabase.py***************

# *******************Step 7: ADD IMAGES TO DATABASE from EncodeGenerator.py***************

# *******************Step 8: REALTIME DATABASE UPDATE ****************************

modeType = 0
counter = 0
id = -1
imgStudent = []

# final call to camera run
while True:
    success, img = cap.read()

    # RESIZING oUR IMAGES
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

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
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

            id = studentIDs[matchIndex]

            if counter == 0:
                counter = 1
                modeType = 1

    if counter!=0:
        # Get the data
        if counter == 1:
            studentInfo = db.reference(f'Students/{id}').get()
            # print(studentInfo)

            # Get the image
            blob = bucket.get_blob(f'Images/{id}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)

            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

        # obtain image

        cv2.putText(imgBackground, str(studentInfo['total_attendance']),(861, 125),
        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        cv2.putText(imgBackground, str(studentInfo['major']),(1006, 550),
        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        cv2.putText(imgBackground, str(studentInfo['id']),(1006, 493),
        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

        cv2.putText(imgBackground, str(studentInfo['cgpa']),(910, 625),
        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

        cv2.putText(imgBackground, str(studentInfo['year']),(1025, 625),
        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

        cv2.putText(imgBackground, str(studentInfo['starting_year']),(1125, 625),
        cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)

        offset = (414 - w)//2

        cv2.putText(imgBackground, str(studentInfo['name']), (808+offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

        imgBackground[175:175+216, 909:909+216] = imgStudent

        counter+=1


    cv2.imshow("Camera", img)
    cv2.imshow("Face attendance", imgBackground)
    cv2.waitKey(1)
