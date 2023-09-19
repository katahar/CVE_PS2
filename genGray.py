import cv2
import numpy as np

img = np.empty((256,256), np.uint8)

for i in range(256):
    img[:,i] = i

cv2.imwrite("gray.png", img)
