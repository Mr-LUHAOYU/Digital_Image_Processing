import numpy as np
from matplotlib import pyplot as plt


def display(image):
    plt.imshow(image, cmap='gray', vmin=0, vmax=7)
    plt.colorbar()
    plt.show()


n, m, k = 10, 10, 7
img = [[1] * m for _ in range(n // 2)] + [[0] * m for _ in range(n // 2)]
img = np.array(img).T

hist, bins = np.histogram(img.flatten(), bins=k, range=(0, k))
cdf = np.cumsum(hist)
cdf_normalized = cdf * hist.max() / cdf.max()

cdf_m = np.ma.masked_equal(cdf, 0)
cdf_m = (cdf_m - cdf_m.min()) * k / (cdf_m.max() - cdf_m.min())
cdf = np.ma.filled(cdf_m, 0).astype(int)
img_new = cdf[img]

display(img)
display(img_new)
