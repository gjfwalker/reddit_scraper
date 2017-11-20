import ctypes
import os
import numpy as np
import time

folder = os.path.join("D:\\", "Documents", "backgrounds")
pics = []

for fn in os.listdir(folder):
    if fn.endswith(".jpg") or fn.endswith(".bmp") or fn.endswith(".png"):
        pics.append(os.path.join(folder, fn))

while True:
    image_path = pics[np.random.randint(0, len(pics)-1)]
    print(image_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
    time.sleep(30)