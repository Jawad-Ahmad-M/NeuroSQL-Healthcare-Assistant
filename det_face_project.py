import cv2
import subprocess
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

face_detected_time = 0
face_detected = False

def specific_function():
    print("Face detected for more than 5 seconds! Running specific function...")

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        if not face_detected:  
            face_detected_time = time.time()  
            face_detected = True
    else:
        face_detected = False  

    if face_detected and time.time() - face_detected_time >= 5:
        print("face detected")
        subprocess.Popen(["python", "main.py"])
        break  

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Live Face Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
