# 🟢 Matrix Rain Video Filter

A real-time Python video filter that renders the user as dynamic ASCII characters.

![Demo](demo.gif)

## 💡 About
This project uses **Computer Vision** to recreate the iconic "digital rain" aesthetic from *The Matrix*. It captures live video, removes the background using AI segmentation, and reconstructs the user's image using colored text characters.
vid_to_ascii.py -> renders the whole image
terminal.py -> "prints" the output image to the terminal
selfie_to_ascii.py -> uses mediapipe to just use the filter on the person, removes background
## 🛠 Tech Stack
* **Python 3.x**
* **OpenCV:** For image processing, grid sampling, and real-time rendering.
* **MediaPipe:** For robust, real-time selfie segmentation (background removal).
* **NumPy:** For high-performance array manipulation.
