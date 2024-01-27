import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://face-recog-python-ec2ea-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('Students')

# python dictionary
data = {
    "TP011111":{
        "name" : "Lee Wen Han",
        "major" : "CS(AI)",
        "starting_year" : 2021,
        "total_attendance" : 20,
        "grades" : "A",
        "year" : 2,
        "last_attendance_taken" : "2024-01-26 16:10:30",
    },
    "TP012345":{
        "name" : "TP  012345",
        "major" : "CS(AI)",
        "starting_year" : 2021,
        "total_attendance" : 20,
        "grades" : "A",
        "year" : 2,
        "last_attendance_taken" : "2024-01-26 16:10:30",
    },
    "TP054321":{
        "name" : "TP  054321",
        "major" : "CS(AI)",
        "starting_year" : 2021,
        "total_attendance" : 20,
        "grades" : "A",
        "year" : 2,
        "last_attendance_taken" : "2024-01-26 16:10:30",
    },
    "TP063338":{
        "name" : "TP  063338",
        "major" : "CS(AI)",
        "starting_year" : 2021,
        "total_attendance" : 20,
        "grades" : "A",
        "year" : 2,
        "last_attendance_taken" : "2024-01-26 16:10:30",
    },
    "TP068713":{
        "name" : "Suzanne Lai",
        "major" : "CS(AI)",
        "starting_year" : 2021,
        "total_attendance" : 20,
        "grades" : "A",
        "year" : 2,
        "last_attendance_taken" : "2024-01-26 16:10:30",
    },
    "TP088888":{
        "name" : "TP  088888",
        "major" : "CS(AI)",
        "starting_year" : 2021,
        "total_attendance" : 20,
        "grades" : "A",
        "year" : 2,
        "last_attendance_taken" : "2024-01-26 16:10:30",
    },
}

for key, value in data.items():
    ref.child(key).set(value)