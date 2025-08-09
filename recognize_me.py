import face_recognition
import cv2
import numpy as np
from PIL import Image

# Load the known image using OpenCV
known_image = cv2.imread(r"C:\Users\zbook\Desktop\Gui Project\images\Aaron_Eckhart\Aaron_Eckhart_0001.jpg")

# Ensure the image is loaded correctly
if known_image is None:
    print("Error: Image could not be loaded. Check the file path.")
    exit()

# Convert the loaded image from BGR to RGB (since OpenCV loads images in BGR by default)
known_image_rgb = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)

# Ensure the image is in the correct type (uint8)
known_image_rgb = np.array(known_image_rgb, dtype=np.uint8)

# Debug: Print the shape and dtype of the image
print(f"Known image shape: {known_image_rgb.shape}")
print(f"Known image dtype: {known_image_rgb.dtype}")

# Check if the image has 3 channels (RGB)
if known_image_rgb.shape[2] != 3:
    print("Error: Image does not have 3 channels (RGB).")
    exit()

# Convert the OpenCV image (numpy array) to a Pillow Image (PIL)
known_image_pil = Image.fromarray(known_image_rgb)

# Convert the Pillow image back to numpy array (to ensure compatibility with face_recognition)
known_image_rgb = np.array(known_image_pil)

# Get the face encoding for the known image
try:
    known_face_encoding = face_recognition.face_encodings(known_image_rgb)[0]
except IndexError:
    print("Error: No faces found in the image.")
    exit()

# Create an array of known face encodings
known_face_encodings = [known_face_encoding]

# Capture image from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the captured frame to RGB (important for face recognition)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Debug: Print the shape and dtype of the frame
    print(f"Frame shape: {rgb_frame.shape}")
    print(f"Frame dtype: {rgb_frame.dtype}")

    # Ensure the frame has 3 channels (RGB)
    if rgb_frame.shape[2] != 3:
        print("Error: Frame does not have 3 channels (RGB).")
        continue

    # Find all face locations in the frame
    face_locations = face_recognition.face_locations(rgb_frame)

    if not face_locations:
        print("No faces detected in the frame.")

    # Get face encodings for all faces in the frame
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the captured face to the known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        if True in matches:
            # If a match is found
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Recognized", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            # No match found
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, "Not Recognized", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show the result
    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
