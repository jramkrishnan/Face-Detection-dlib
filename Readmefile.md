The aim is to create an application which tracks students entering and leaving schools with the help of face detection models.
The data will also be cross-checked with the help of RFID system.

Project Structure
face-recognition-app/
├── app.py
├── face_recognition_system.py
├── templates/
│   └── index.html
├── known_faces/
├── Dockerfile
├── requirements.txt
└── kubernetes/
    ├── deployment.yaml
    ├── service.yaml
    ├── persistent-volume.yaml
    └── persistent-volume-claim.yaml
