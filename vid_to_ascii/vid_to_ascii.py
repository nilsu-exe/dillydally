import cv2
import numpy as np
import random


VIDEO_SOURCE = 0  # Use 0 for webcam, or put a filename like 'video.mp4'
CELL_SIZE = 6
FONT_SCALE = 0.2
DENSITY_THRESHOLD = 20  # If a pixel is too dark, we don't draw anything


CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&[]{}/|?!=+-_"


def process_frame(frame):
    height, width, _ = frame.shape

    cols = width // CELL_SIZE
    rows = height // CELL_SIZE
    small_frame = cv2.resize(frame, (cols, rows))

    text_canvas = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(rows):
        for x in range(cols):

            pixel_color = small_frame[y, x]
            b, g, r = map(int, pixel_color)

            #Average brightness
            brightness = (b + g + r) / 3

            # Only draw if the pixel is bright enough
            if brightness > DENSITY_THRESHOLD:

                char = random.choice(CHARS)

                pos_x = x * CELL_SIZE
                pos_y = y * CELL_SIZE

                cv2.putText(
                    text_canvas,
                    char,
                    (pos_x, pos_y + CELL_SIZE),  # Offset y to align text
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
    char_frame = process_frame(frame)

    cv2.imshow('Matrix Text Effect', char_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()