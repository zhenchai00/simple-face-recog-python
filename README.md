# Beginner Facial Recognition AI with Python 

This is the workshop final output with the concept of attendance system using facial recognition with Python.

There have few things needed to aware to rerun again the application.

1. Run `pip install -r requirements.txt` to install all the dependencies.
2. Go to Firebase Console and get the new `serviceAccountKey.json` from `Project Overview > Project settings > Service accounts > Generate new private key` and it will download the json format file then paste it in the root folder.
3. Then go to main.py, Firebase.py and EncodeGenerator.py and change the `databaseURL` to your own Firebase realtime database URL and `storageBucket` to your own Firebase storage url without the `gs://`.
4. Run Firebase.py to generate the attendance list in the Firebase realtime database.
5. Run EncodeGenerator.py to generate the face encoding for the attendance list.
6. Run main.py to start the application.
7. Then it will run smoothly and you can try add your image with width and height of 215 x 215 pixel to the Images folder and add details into the Firebase.py. 

# License
MIT by zhenchai

You can create your own simple-face-recog-python application for free without notifying me by forking this project under the following conditions:

Do not use it as a commercial product. (You can use it for commercial purpose but you need to credit me.)