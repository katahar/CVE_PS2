'''
PS2-1: Converting a grayscale image to a pseudo-color image

Your program should perform the following five steps to convert a grayscale image:
    (1) Ask the user for an input grayscale image and display the input image in the first window.
    (2) Find the lowest pixel value and the highest pixel value in the grayscale image.
    (3) Make a look-up table to convert the lowest gray value to blue and the highest gray value to red.
        The other gray values should be mapped to rainbow colors by the method explained in the lecture.
    (4) Using OpenCV functions, draw a cross in a circle to indicate the pixel of the highest gray value.
        Draw the cross and circle with white. If multiple pixels share the same highest gray value, place the
        cross and circle at the center of gravity of these pixels. Figure 4 shows a sample input image and
        output image.
    (5) Save the final color image as input-filename-color.png and display the file in the second window.

Note: In the second and third steps, you must write your own Python code rather than using OpenCV built-
in functions. In the fourth step, use OpenCV functions such as cv2.line() and cv2.circle().

Apply your program to the five grayscale images shown in Figure 5

Note to self: be sure to run "conda activate cve" before running this file

'''


import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt

def get_lut_ind(input, min, max):
    if input<=min:
        return 0
    elif input>=max:
        return 255
    else:
        return int( ((input-min)/(max-min)) *255 )

parser = argparse.ArgumentParser(description='Pseudo Color generation via OpenCV')
parser.add_argument('-i', '--input', help='Path to input image.', default='x-ray.png')
parser.add_argument('-t', '--type',help='Type of colormap.', type=int, default='2')
args = parser.parse_args()

window_name = 'pseudo-color using OpenCV'

image = cv2.imread(args.input, 0)
max_ind = np.unravel_index(np.argmax(image, axis=None), image.shape)
max_val = image[max_ind]
min_ind = np.unravel_index(np.argmin(image, axis=None), image.shape)
min_val = image[min_ind]

print("Image shape")
print(image[0,0].shape)

print("max")
print( (image[max_ind]))
print(max_ind)

print("min")
print( (image[min_ind]))
print(min_ind)

LUT = np.zeros([256,3])

# sets anything below minimum as blue
for i in range(min_val+1):
    LUT[i] = [255,0,0]

# sets anything above maximum as red
for i in range(max_val+1):
    LUT[255-i] = [0,0,255]

# seg_len = int((ma
# x_val-min_val)/4)
seg_len = int(256/4)
half_seg_len = int(seg_len/2)
print("Seg len " + str(seg_len))
# # BGR 
# # first quarter. Blue is max, green is increasing, red is 0
# for i in range(seg_len):
#     LUT[i] = [255, int(i*255/seg_len),0]

# # second quarter.  blue is decreasing, green is max, red is 0
# for i in range(seg_len):
#     LUT[seg_len + i] = [int(255 - (i*255/seg_len)),255, 0]

# # third quarter. blue is 0, green is max,  red is increasing
# for i in range(seg_len):
#     LUT[seg_len+ seg_len+ i] = [0,255,int(i*255/seg_len)]

# # fourth quarter.  blue is 0, green is decreasing. red is max
# for i in range(seg_len):
#     LUT[seg_len + seg_len + seg_len +i] = [0,int(255 - (i*255/seg_len)),255]


# BGR 
# first half_section. Blue is increasing from half, green is 0, red is 0
for i in range(half_seg_len):
    LUT[i] = [int(255/2) +int(i*255/seg_len), 0,0]

# first full section. Blue is max, green is increasing, red is 0
for i in range(seg_len):
    LUT[half_seg_len + i] = [255, int(i*255/seg_len),0]

# second full section.  blue is decreasing, green is max, red is increasing
for i in range(seg_len):
    LUT[half_seg_len + seg_len + i] = [int(255 - (i*255/seg_len)),255, int(i*255/seg_len)]

# third full section.  blue is 0, green is decreasing, red is max
for i in range(seg_len):
    LUT[half_seg_len + seg_len + seg_len + i] = [0,int(255 - (i*255/seg_len)), 255]

# last  half section.  blue is 0, green is 0, red is decreasing
for i in range(half_seg_len):
    LUT[half_seg_len + seg_len + seg_len + seg_len + i] = [0,0, int(255 - (i*255/seg_len))]

# print(LUT)

correct_image = cv2.applyColorMap(image, args.type)
new_image = np.zeros([image.shape[0], image.shape[1], 3], np.uint8)
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        # print(str(i) + ", " + str(j) + ": " + str(image[i,j]) + "->" + str(get_lut_ind(image[i,j], min_val, max_val)) + str(LUT[get_lut_ind(image[i,j], min_val, max_val)]))
        new_image[i,j,:] = LUT[get_lut_ind(image[i,j], min_val, max_val)]


cv2.namedWindow("manual version", cv2.WINDOW_NORMAL)
cv2.namedWindow("correct image", cv2.WINDOW_NORMAL)
cv2.namedWindow("original", cv2.WINDOW_NORMAL)

cv2.imshow("correct image", correct_image)
cv2.imshow("original", image)
cv2.imshow("manual version", new_image)
cv2.waitKey()