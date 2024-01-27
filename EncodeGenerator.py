import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://face-recog-python-ec2ea-default-rtdb.asia-southeast1.firebasedatabase.app/',
    'storageBucket': 'face-recog-python-ec2ea.appspot.com'
})

folderPathImages = 'Images'
listPathImages = os.listdir(folderPathImages)
imgListImages = []

# extracting student ids
studentIds = []
for path in listPathImages:
    imgListImages.append(cv2.imread(os.path.join(folderPathImages, path)))
    studentIds.append(os.path.splitext(path)[0])
    
    fileName = f'{folderPathImages}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

def generateEncodings(images):
    encodeList = []
    
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    
    return encodeList

encodeListKnown = generateEncodings(imgListImages)
encodeListWithIds = [encodeListKnown, studentIds]

# open new file in WRITE MODE
encodeFile = open('Encodings.p', 'wb')
# using pickle to dump the data
pickle.dump(encodeListWithIds, encodeFile)
# close the file
encodeFile.close()