import cv2 # image recognition by webcam
import os # to get the path of the file
import pickle
import face_recognition
import numpy as np
import cvzone
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://face-recog-python-ec2ea-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'face-recog-python-ec2ea.appspot.com'
})

bucket = storage.bucket()

# initializing webcam and reading background image
capture = cv2.VideoCapture(1)
capture.set(3,680)
capture.set(4,480)
backgroundImg = cv2.imread('Resources/Background.png')

folderPathMode = 'Resources/Modes'
listPathMode = os.listdir(folderPathMode)
imgListMode = []

for path in listPathMode:
    imgListMode.append(cv2.imread(os.path.join(folderPathMode, path)))

encodeFile = open('Encodings.p', 'rb')
encodeListWithIds = pickle.load(encodeFile)
encodeFile.close()

encodeListKnown, studentIds = encodeListWithIds

modeType = 0
counter = 0
id = -1

while True:
    success, image = capture.read()

    # onto the position of 162:162 + 480, 55:55 + 640, you are paste webcam over the backgroundImg
    backgroundImg[162:162 + 480, 55:55 + 640] = image
    backgroundImg[44:44 +633, 808:808 + 414] = imgListMode[modeType]

    # making the image smaller 1/4 of its size
    smallImg = cv2.resize(image, (0, 0), None, 0.25, 0.25)
    # converting the image to RGB
    smallImg = cv2.cvtColor(smallImg, cv2.COLOR_BGR2RGB)

    # FINDING the face in the current frame
    faceCurrentFrame = face_recognition.face_locations(smallImg)
    # encoding the face found in the image
    encodeCurrentFrame = face_recognition.face_encodings(smallImg, faceCurrentFrame)

    if faceCurrentFrame:
        for encodeFace, faceLocation in zip(encodeCurrentFrame, faceCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDistance = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDistance)

            if matches[matchIndex]:
                print("Registered Student Detected: ")
                print(studentIds[matchIndex])

                y1, x2, x1, y2, = faceLocation
                y1, x2, x1, y2 = y1 * 4, x2 * 4, x1 * 4, y2 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                backgroundImg = cvzone.cornerRect(backgroundImg, bbox, rt=0)
                id = studentIds[matchIndex]
            
                if counter == 0:
                    counter = 1
                    modeType = 1

        if counter != 0:
            if counter == 1:
                # retrieving students information from database
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)

                # retrieving student image from storage
                blob = bucket.blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                studentImg = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # update attendance record and data
                dateTime = datetime.strptime(studentInfo['last_attendance_taken'], 
                                            '%Y-%m-%d %H:%M:%S')
                timeInSecsElapsed = (datetime.now() - dateTime).total_seconds()
                print(timeInSecsElapsed)

                if timeInSecsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1

                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_taken').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    modeType = 3
                    counter = 0
                    backgroundImg[44:44 + 633, 808:808 + 414] = imgListMode[modeType]

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2
        
                backgroundImg[44:44 + 633, 808:808 + 414] = imgListMode[modeType]
        
                if counter < 10:
                    cv2.putText(backgroundImg, str(studentInfo['total_attendance']), (861, 125) , 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(backgroundImg, str(studentInfo['major']), (1006, 550) , 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(backgroundImg, str(id), (1006, 493) , 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(backgroundImg, str(studentInfo['grades']), (910, 625) , 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    cv2.putText(backgroundImg, str(studentInfo['year']), (1025, 625) , 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    cv2.putText(backgroundImg, str(studentInfo['starting_year']), (1125, 625) , 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

                    (width, height), baseline = cv2.getTextSize(str(studentInfo['name']), cv2.FONT_HERSHEY_SIMPLEX, 1, 1)

                    center_offset = (414 - width) // 2
                    cv2.putText(backgroundImg, str(studentInfo['name']), (808 + center_offset, 425) , 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 1)
                    backgroundImg[175:175 + 216, 909:909 + 216] = studentImg

            counter += 1

            if counter > 20:
                counter = 0
                modeType = 0
                studentInfo = []
                studentImg = []
                backgroundImg[44:44 + 633, 808:808 + 414] = imgListMode[modeType]
    else:
        modeType = 0
        counter = 0

    cv2.imshow('Attendance System', backgroundImg)
    cv2.waitKey(1)