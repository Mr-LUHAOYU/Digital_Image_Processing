import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, exposure, util, filters
from scipy.ndimage import median_filter, convolve

# Load and convert the image
Image1 = io.imread('lotus.bmp')
Image1 = util.img_as_float(Image1)
gray = color.rgb2gray(Image1)

# Display histogram
plt.figure()
plt.hist(gray.ravel(), bins=256, histtype='step', color='black')
plt.title('Histogram')
plt.show()

# Image dimensions
h, w = gray.shape

# Piecewise linear transformation
NewImage1 = np.zeros((h, w))
a, b, c, d = 80/256, 180/256, 30/256, 220/256
for x in range(w):
    for y in range(h):
        if gray[y, x] < a:
            NewImage1[y, x] = gray[y, x] * c / a
        elif gray[y, x] < b:
            NewImage1[y, x] = (gray[y, x] - a) * (d - c) / (b - a) + c
        else:
            NewImage1[y, x] = (gray[y, x] - b) * (1 - d) / (1 - b) + d

plt.figure()
plt.imshow(NewImage1, cmap='gray')
plt.title('Piecewise Linear Transformation')
plt.show()

# Histogram equalization
NewImage2 = exposure.equalize_hist(gray)
plt.figure()
plt.imshow(NewImage2, cmap='gray')
plt.title('Histogram Equalization')
plt.show()

# Color transformation
NewImage3 = np.zeros((h, w, 3))
for x in range(w):
    for y in range(h):
        if gray[y, x] < 64/256:
            NewImage3[y, x, 0] = 0
            NewImage3[y, x, 1] = 4 * gray[y, x]
            NewImage3[y, x, 2] = 1
        elif gray[y, x] < 128/256:
            NewImage3[y, x, 0] = 0
            NewImage3[y, x, 1] = 1
            NewImage3[y, x, 2] = 2 - 4 * gray[y, x]
        elif gray[y, x] < 192/256:
            NewImage3[y, x, 0] = 4 * gray[y, x] - 2
            NewImage3[y, x, 1] = 1
            NewImage3[y, x, 2] = 0
        else:
            NewImage3[y, x, 0] = 1
            NewImage3[y, x, 1] = 4 - 4 * gray[y, x]
            NewImage3[y, x, 2] = 0

plt.figure()
plt.imshow(NewImage3)
plt.title('Color Transformation')
plt.show()

# Add noise and apply median filter
noiseIsp = util.random_noise(gray, mode='s&p', amount=0.1)
noiseIg = util.random_noise(gray, mode='gaussian')
result1 = median_filter(noiseIsp, size=3)
result2 = median_filter(noiseIg, size=3)

plt.figure()
plt.subplot(121)
plt.imshow(result1, cmap='gray')
plt.title('Salt & Pepper Noise 3x3 Median Filter')
plt.subplot(122)
plt.imshow(result2, cmap='gray')
plt.title('Gaussian Noise 3x3 Median Filter')
plt.show()

# Sobel edge detection and sharpening
H1 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
H2 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
R1 = convolve(gray, H1)
R2 = convolve(gray, H2)
edgeImage = np.abs(R1) + np.abs(R2)
sharpImage = gray + edgeImage

plt.figure()
plt.subplot(121)
plt.imshow(edgeImage, cmap='gray')
plt.title('Sobel Edge Image')
plt.subplot(122)
plt.imshow(sharpImage, cmap='gray')
plt.title('Sobel Sharpened Image')
plt.show()