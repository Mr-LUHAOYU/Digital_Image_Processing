import numpy as np
from matplotlib import pyplot as plt


def display(image):
    plt.imshow(image, cmap='gray', vmin=0, vmax=7)
    plt.colorbar()
    plt.show()


n, m, k = 10, 10, 7
img = [[1] * m for _ in range(n // 2)] + [[0] * m for _ in range(n // 2)]
img = np.array(img).T

display(img)

hist, bins = np.histogram(img.flatten(), bins=k, range=(0, k))

cdf = hist / np.sum(hist) * k
cdf = np.cumsum(cdf)
cdf = np.round(cdf).astype(int)
img_new = cdf[img]

display(img_new)
