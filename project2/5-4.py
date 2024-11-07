import numpy as np

hist = [560, 920, 1046, 705, 356, 267, 170, 72]
bins = [0, 1, 2, 3, 4, 5, 6, 7]

hist = np.array(hist)
bins = np.array(bins)

cdf = hist[:] / np.sum(hist[:]) * np.max(bins)
cdf = np.cumsum(cdf)
cdf = np.round(cdf).astype(int)
print(cdf)
