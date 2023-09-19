import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Pseudo Color generation via OpenCV')
parser.add_argument('-i', '--input', help='Path to input image.', default='x-ray.png')
parser.add_argument('-t', '--type',help='Type of colormap.', type=int, default='2')
args = parser.parse_args()

window_name = 'pseudo-color using OpenCV'

image = cv2.imread(args.input, 0)
new_image = cv2.applyColorMap(image, args.type)

cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.imshow(window_name, new_image)
cv2.waitKey()
