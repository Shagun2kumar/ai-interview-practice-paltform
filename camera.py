import cv2
import numpy as np

# Haar cascades
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml')


def analyze_confidence():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return {"score": 50, "msg": "Camera not working"}

    scores = []

    for i in range(25):   # more frames = more accuracy
        ret, frame = cap.read()
        if not ret:
            continue

        h, w, _ = frame.shape
        center_x, center_y = w//2, h//2

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        score = 50
        feedback = []

        for (x, y, fw, fh) in faces:

            face_center_x = x + fw//2
            face_center_y = y + fh//2

            # 👀 Eye Contact
            face = gray[y:y+fh, x:x+fw]
            eyes = eye_cascade.detectMultiScale(face)

            if len(eyes) >= 2:
                score += 20
            else:
                feedback.append("Maintain eye contact")

            # 🙂 Face Position (center)
            if abs(face_center_x - center_x) < 100:
                score += 10
            else:
                feedback.append("Keep face centered")

            # 🙂 Face Distance (closer)
            if fw > 150:
                score += 10
            else:
                feedback.append("Move slightly closer")

            # 🎥 Stability (blur detection)
            blur = cv2.Laplacian(gray, cv2.CV_64F).var()

            if blur > 60:
                score += 10
            else:
                feedback.append("Reduce movement / blur")

        scores.append(score)

    cap.release()

    if len(scores) == 0:
        return {"score": 50, "msg": "No face detected"}

    final_score = int(np.mean(scores))

    # FINAL MESSAGE
    if final_score > 85:
        msg = "Excellent confidence"
    elif final_score > 60:
        msg = "Good, improve eye contact"
    else:
        msg = "Low confidence, improve posture"

    return {
        "score": min(final_score, 100),
        "msg": msg
    }

