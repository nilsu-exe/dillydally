#MADE WITH HELP OF GEMINI
import cv2
import shutil
import sys
import numpy as np
import mediapipe as mp
import random

# --- Configuration ---
VIDEO_SOURCE = 0

# MODE: Set to 'MATRIX' for letters, or 'BLOCKS' for solid pixels
MODE = "MATRIX"

# SPACING: 1 = Normal, 2 = Wide (Adds a space between chars to correct aspect ratio)
SPACING = 2

# --- Character Sets ---
MATRIX_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&[]{}/|?!=+-_"
# Block characters from light to dark
BLOCK_CHARS = " ░▒▓█"

# --- Setup MediaPipe ---
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=0)


def get_frame_string(frame, mask, width, height):
    # Resize to fit terminal
    # If SPACING is 2, we need half the width resolution so it fits when we double it
    render_width = width // SPACING

    small_frame = cv2.resize(frame, (render_width, height))
    small_mask = cv2.resize(mask, (render_width, height), interpolation=cv2.INTER_NEAREST)

    # Boost Brightness
    small_frame = cv2.convertScaleAbs(small_frame, alpha=1.5, beta=30)

    output = ""

    for y in range(height):
        row_string = ""
        for x in range(render_width):
            if small_mask[y, x] > 0.1:
                b, g, r = small_frame[y, x]

                # Logic for different looks
                if MODE == "MATRIX":
                    char = random.choice(MATRIX_CHARS)
                else:
                    # In BLOCK mode, we map brightness to a block shape
                    brightness = (int(b) + int(g) + int(r)) // 3
                    # Map 0-255 to index 0-4
                    idx = int((brightness / 255) * (len(BLOCK_CHARS) - 1))
                    char = BLOCK_CHARS[idx]

                # Add Color + Char
                pixel = f"\033[38;2;{r};{g};{b}m{char}"

                # Handle Spacing (Widen the pixel)
                if SPACING == 2:
                    # If spacing is on, we print the char + a space, OR double chars
                    # Using double char "AA" or "██" makes pixels look square!
                    row_string += pixel + pixel
                else:
                    row_string += pixel

            else:
                # Background
                row_string += " " * SPACING

        output += row_string + "\033[0m\n"

    return output


# --- Main Loop ---
cap = cv2.VideoCapture(VIDEO_SOURCE)

try:
    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = segmentation.process(rgb_frame)
        mask = results.segmentation_mask

        columns, lines = shutil.get_terminal_size()

        # Pass the terminal size to the renderer
        art = get_frame_string(frame, mask, columns, lines - 1)

        sys.stdout.write("\033[H" + art)
        sys.stdout.flush()

except KeyboardInterrupt:
    print("\033[0m\nExiting...")
    cap.release()
