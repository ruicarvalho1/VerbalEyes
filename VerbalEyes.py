import cv2
from ultralytics import YOLO
from gtts import gTTS
import os
import threading
from playsound import playsound
import face_recognition
import time
import platform


model = YOLO("yolov8m.pt")

cap = cv2.VideoCapture(0)


known_image = face_recognition.load_image_file("rui.jpg")
known_encodings = face_recognition.face_encodings(known_image)
if len(known_encodings) == 0:
    raise SystemExit("Nenhum encoding encontrado para 'rui.jpg'.")
known_encoding = known_encodings[0]
known_name = "Rui"


current_name = "User"
already_greeted = False
last_spoken = None
speaking = False


def speak(text):
    global speaking
    speaking = True
    try:
        tts = gTTS(text=text, lang='en')
        filename = "temp.mp3"
        tts.save(filename)
        if platform.system() == 'Darwin':
            os.system(f"afplay {filename}")
        else:
            playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"Erro no speak(): {e}")
    speaking = False

def get_hand_position(x_center, frame_width):
    if x_center < frame_width // 3:
        return "right hand"
    elif x_center > 2 * frame_width // 3:
        return "left hand"
    return "center"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_height, frame_width = frame.shape[:2]
    hand_objects = {"left hand": None, "right hand": None}
    current_name = "User"

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)
    for face_encoding, face_location in zip(face_encodings, face_locations):
        match = face_recognition.compare_faces([known_encoding], face_encoding, tolerance=0.5)[0]
        if match:
            current_name = known_name
            if not already_greeted and not speaking:
                already_greeted = True
                threading.Thread(target=speak, args=(f"Hello {known_name}",)).start()
                time.sleep(3)

    results = model(frame, conf=0.5)
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            name = model.names[cls_id]
            if name.lower() == "person":
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1
            area = w * h
            frame_area = frame_width * frame_height

            if area < 0.03 * frame_area or y2 < frame_height // 2:
                continue

            conf = float(box.conf[0])
            x_center = (x1 + x2) // 2
            hand_pos = get_hand_position(x_center, frame_width)
            if hand_pos in ["left hand", "right hand"]:

                if hand_objects[hand_pos] is None or conf > hand_objects[hand_pos][1]:
                    hand_objects[hand_pos] = (name, conf, (x1, y1, x2, y2))

    current_objects = []
    for hand, obj_info in hand_objects.items():
        if obj_info is not None:
            name, conf, (x1, y1, x2, y2) = obj_info
            label = f"{name} ({conf:.2f})"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            current_objects.append((hand, name))

    if current_objects and not speaking:
        messages = [f"you have a {name} in your {hand}" for hand, name in current_objects]
        full_message = f"{current_name}, " + " and ".join(messages)
        if full_message != last_spoken:
            threading.Thread(target=speak, args=(full_message,)).start()
            last_spoken = full_message


    cv2.imshow("Face & Object Detection", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
