import cv2
import mediapipe as mp
import time
import sys
import math
import threading

# --- Header ---
def header():
    print()
    print("=" * 50)
    print("🌟 Selamat Datang di Perkenalan Mahasiswa Baru UMSIDA 🌟".center(50))
    print("=" * 50)

# --- Fungsi efek typing dengan callback saat selesai ---
def type_writer_threaded(text, delay=0.05, on_complete=None):
    def typing_animation():
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
        if on_complete:
            on_complete()
    thread = threading.Thread(target=typing_animation)
    thread.daemon = True
    thread.start()

# --- MediaPipe setup ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    static_image_mode=False,
    max_num_hands=1
)
mp_drawing = mp.solutions.drawing_utils

def fingers_up(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []
    # Thumb (horizontal)
    fingers.append(hand_landmarks.landmark[tips[0]].x <
                   hand_landmarks.landmark[tips[0] - 1].x)
    # Index–Pinky (vertical)
    for i in range(1, 5):
        fingers.append(hand_landmarks.landmark[tips[i]].y <
                       hand_landmarks.landmark[tips[i] - 2].y)
    return fingers  # [thumb, index, middle, ring, pinky]

def detect_gesture(hand_landmarks):
    fingers = fingers_up(hand_landmarks)
    thumb, index, middle, ring, pinky = fingers

    if all(fingers): 
        return "open"

    # >>> GESTUR BARU: thumb & pinky up, others down <<<
    if thumb and pinky and not any([index, middle, ring]):
        return "thumb_pinky"

    # Rock 🤘 : index & pinky up
    if index and pinky and not any([middle, ring, thumb]):
        return "rock"

    # Okay 👌
    ix, iy = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
    tx, ty = hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y
    if math.hypot(ix - tx, iy - ty) < 0.05 and middle and ring and pinky:
        return "okay"

    # Four fingers
    if not thumb and all([index, middle, ring, pinky]):
        return "four_fingers"

    # Peace ✌️
    if index and middle and not any([ring, pinky, thumb]):
        return "peace"

    return None

# --- Video capture ---
cap = cv2.VideoCapture(0)
done_gestures = set()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            gesture = detect_gesture(hand_landmarks)

            if gesture == "open" and "intro" not in done_gestures:
                header()
                type_writer_threaded("Halo! Perkenalkan nama saya Ubed.", delay=0.05)
                done_gestures.add("intro")

            elif gesture == "thumb_pinky" and "faculty" not in done_gestures:
                # gunakan gestur baru (thumb + pinky) untuk menampilkan teks fakultas
                type_writer_threaded("Saya dari Fakultas Sains dan Teknologi.", delay=0.05)
                done_gestures.add("faculty")

            elif gesture == "rock" and "program" not in done_gestures:
                type_writer_threaded("Saya dari Program Studi Informatika.", delay=0.05)
                done_gestures.add("program")

            elif gesture == "okay" and "year" not in done_gestures:
                type_writer_threaded("Saya angkatan 2025-2026.", delay=0.05)
                done_gestures.add("year")

            elif gesture == "four_fingers" and "hobby" not in done_gestures:
                type_writer_threaded("Saya suka coding dan bermain game.", delay=0.05)
                done_gestures.add("hobby")

            elif gesture == "peace" and "closing" not in done_gestures:
                type_writer_threaded(
                    "Sampai jumpa dan semoga hari Anda menyenangkan! ✌️",
                    delay=0.05,
                    on_complete=lambda: print("=" * 50)
                )
                done_gestures.add("closing")

    cv2.imshow("Gesture Intro", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
