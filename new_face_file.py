import numpy as np
import cv2
import pickle



face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner1.yml")

labels = {"person_name":1}
with open("labels.pickle",'rb') as f:
  og_labels = pickle.load(f)
  labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)

while True:
  ret,frame = cap.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
  for (x,y,w,h) in faces:
    # print(x,y,w,h)
    roi_grey = gray[y:y+h, x:x+w]
    roi_color = frame[y:y+h, x:x+w]

    # recognize? deep learned model predict keras, tensorflow, pytorch, scikit learn, 

    id_, config = recognizer.predict(roi_grey)
    if config < 60:
      print(id_)
      print(labels[id_])
      font = cv2.FONT_HERSHEY_SIMPLEX
      name = labels[id_]
      stroke = 2
      color = (255,255,255)
      cv2.putText(frame, name, (x, y + h - 10), font, 1, color, stroke, cv2.LINE_AA)
    img_item = "my-image.png"
    cv2.imwrite(img_item, roi_color)

    color = (0,255,0) # BGR
    stroke = 2
    end_cord_x = x + w 
    end_cord_y = y + h
    cv2.rectangle(frame,(x,y) , (end_cord_x,end_cord_y), color,stroke)


  #Display the resulting image
  cv2.imshow('frame',frame)
  if cv2.waitKey(20) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()