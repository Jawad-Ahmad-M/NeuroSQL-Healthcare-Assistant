import cv2
import numpy as np
from facenet import facenet  # Assuming facenet is a module in the extracted files

# Load the pre-trained model
model = facenet.load_model(r"C:\Users\zbook\Downloads\Compressed\20180408-102900\20180408-102900\20180408-102900.pb")

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame for face detection
    # (Assuming you have a function to detect faces)
    faces = detect_faces(frame)  # Implement this function based on your model

    for face in faces:
        # Recognize the face
        embedding = facenet.get_embedding(face)  # Get the face embedding
        identity = recognize_face(embedding)  # Implement this function to recognize the face

        # Draw rectangle and label on the frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  # Draw rectangle around face
        cv2.putText(frame, identity, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
