import cv2
import face_recognition
import time
import os
import numpy as np

# Directory where user data will be stored
data_dir = "users_data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def add_user():
    """
    Captures three images (30° left, 30° right, and frontal) for a new user
    and saves the face encodings to disk.
    """
    username = input("Enter new user name (no spaces): ").strip()
    if not username:
        print("Invalid name. Please try again.")
        return

    user_dir = os.path.join(data_dir, username)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    else:
        print(f"User '{username}' already exists. Overwriting images...")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    orientations = [
        ("left30", "Please turn your face ~30 degrees to the LEFT and press 'c' to capture."),
        ("right30", "Please turn your face ~30 degrees to the RIGHT and press 'c' to capture."),
        ("front", "Please face the camera straight and press 'c' to capture.")
    ]

    for tag, instruction in orientations:
        print(instruction)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            # Ensure we have a writable, contiguous frame
            frame = frame.copy()
            cv2.imshow("Capture - Press 'c' to capture or 'q' to quit", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                # Convert BGR to RGB and ensure contiguous uint8
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_frame = np.ascontiguousarray(rgb_frame, dtype=np.uint8)

                # Locate faces in the RGB image
                face_locs = face_recognition.face_locations(rgb_frame)
                if not face_locs:
                    print("Face not detected. Please remove glasses/adjust lighting/position.")
                    continue

                # Save original BGR image
                img_path = os.path.join(user_dir, f"{tag}.png")
                cv2.imwrite(img_path, frame)
                print(f"Captured and saved: {img_path}")
                break
            elif key == ord('q'):
                print("User capture aborted.")
                cap.release()
                cv2.destroyAllWindows()
                return

    cap.release()
    cv2.destroyAllWindows()
    print(f"User '{username}' added successfully!\n")


def recognize_user(timeout=15):
    """
    Attempts to recognize a user from the live camera feed for up to 'timeout' seconds.
    If recognized, welcomes the user. Otherwise, offers to add a new user.
    """
    # Load known encodings
    known_encodings = []
    known_users = []
    for user in os.listdir(data_dir):
        user_dir = os.path.join(data_dir, user)
        if not os.path.isdir(user_dir):
            continue
        for img_file in ["left30.png", "right30.png", "front.png"]:
            path = os.path.join(user_dir, img_file)
            if os.path.exists(path):
                img = face_recognition.load_image_file(path)
                encs = face_recognition.face_encodings(img)
                if encs:
                    known_encodings.append(encs[0])
                    known_users.append(user)

    if not known_encodings:
        print("No users found. Please add a user first.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    start = time.time()
    print(f"Starting recognition (timeout in {timeout}s)...")

    while True:
        if time.time() - start > timeout:
            print("Unknown person (timeout reached). Would you like to register? (y/n)")
            choice = input().lower()
            if choice == 'y':
                add_user()
            break

        ret, frame = cap.read()
        if not ret:
            continue

        # Ensure writable contiguous frame
        frame = frame.copy()

        # Convert BGR to RGB and ensure contiguous uint8
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame = np.ascontiguousarray(rgb_frame, dtype=np.uint8)

        # Locate and encode faces in the RGB image
        face_locs = face_recognition.face_locations(rgb_frame)
        face_encs = face_recognition.face_encodings(rgb_frame, face_locs)

        if face_encs:
            for enc in face_encs:
                results = face_recognition.compare_faces(known_encodings, enc)
                if True in results:
                    name = known_users[results.index(True)]
                    print(f"✅ Welcome back, {name}!")
                    cap.release()
                    cv2.destroyAllWindows()
                    return
            print("Face detected but not recognized. Please register if you're new.")
            break
        else:
            print("Face not detected. Please remove glasses/adjust lighting/position.")
            time.sleep(0.5)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    while True:
        print("\nMenu:\n1) Add new user\n2) Recognize user\n3) Exit")
        choice = input("Select an option: ")
        if choice == '1':
            add_user()
        elif choice == '2':
            recognize_user()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please select 1, 2, or 3.")
