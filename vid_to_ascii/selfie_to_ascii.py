import cv2
import numpy as np
import mediapipe as mp
import random

VIDEO_SOURCE = 0
CELL_SIZE = 6
FONT_SCALE = 0.2
DENSITY_THRESHOLD = 20
CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&[]{}/|?!=+-_"

# --- Setup MediaPipe Selfie Segmentation ---
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=0)


# model_selection=1 is 'landscape' mode (faster/lighter), 0 is general (slightly better quality)

def process_frame_text(frame):
    height, width, _ = frame.shape

    cols = width // CELL_SIZE
    rows = height // CELL_SIZE
    small_frame = cv2.resize(frame, (cols, rows))

    text_canvas = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(rows):
        for x in range(cols):
            pixel_color = small_frame[y, x]
            b, g, r = map(int, pixel_color)

            if (b + g + r) > DENSITY_THRESHOLD:
                char = random.choice(CHARS)
                pos_x = x * CELL_SIZE
                pos_y = y * CELL_SIZE

                cv2.putText(
                    text_canvas,
                    char,
                    (pos_x, pos_y + CELL_SIZE),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    FONT_SCALE,
                    (b, g, r),
                    1
                )
    return text_canvas


cap = cv2.VideoCapture(VIDEO_SOURCE)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = segmentation.process(rgb_frame)

    #I used if probability>0.45 its a person, can be changed
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.45

    #Change 0->black to another value
    bg_removed_frame = np.where(condition, frame, 0)


    final_output = process_frame_text(bg_removed_frame)

    cv2.imshow('Matrix Selfie', final_output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()