import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(
    "faceattendance-and-recognition-firebase-adminsdk-qxxb5-f986cd2945.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-and-recognition-default-rtdb.firebaseio.com"
})

ref = db.reference('Students')

data = {
    "211210072":
        {
            "name": "Emily",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 10,
            "cgpa": 7,
            "year": 2024,
            "last_attendance_time_stamp": "2024-01-03 09:28:00"
        },
    "211210073":
        {
            "name": "Elon",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 2,
            "cgpa": 9,
            "year": 2024,
            "last_attendance_time_stamp": "2024-01-03 09:20:00"

        },
    "211210074":
        {
            "name": "Murtaza",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 15,
            "cgpa": 8.84,
            "year": 2024,
            "last_attendance_time_stamp": "2024-01-03 09:15:00",
        }
    }

for key, value in data.items():
    ref.child(key).set(value)
