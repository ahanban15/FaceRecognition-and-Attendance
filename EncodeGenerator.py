import cv2
import face_recognition
import pickle
import os

folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)

imgList = []
studentIds = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

#     print(path)
#     print(os.path.splitext(path))
#     print(os.path.splitext(path)[0])
# print(len(imgList))
# print(studentIds)


# FNC TO GENERATE A LIST WITH ALL THE ENCODINGS
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


encodeListKnown = findEncodings(imgList)
# print(encodeListKnown)

encodeListKnownWithIDs = [encodeListKnown, studentIds]

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIDs, file)
file.close()
