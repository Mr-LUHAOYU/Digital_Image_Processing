import numpy as np
np.set_printoptions(precision=4)

f = np.arange(1, 10).reshape(3, 3).T
kx, ky = 2.3, 1.6

rows, cols = f.shape
new_rows = round(rows * ky)
new_cols = round(cols * kx)
new_f = np.zeros((new_rows, new_cols))

for i in range(new_rows):
    for j in range(new_cols):
        src_x = i / ky
        src_y = j / kx
        x1, y1 = int(src_x), int(src_y)
        x2, y2 = min(x1 + 1, rows - 1), min(y1 + 1, cols - 1)
        dx, dy = src_x - x1, src_y - y1
        new_f[i, j] = (1 - dx) * (1 - dy) * f[x1, y1] + dx * (1 - dy) * f[x2, y1] + \
                      (1 - dx) * dy * f[x1, y2] + dx * dy * f[x2, y2]

print(new_f)
