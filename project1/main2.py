import numpy as np
np.set_printoptions(precision=4)

f = np.arange(1, 10).reshape(3, 3).T
theta = np.radians(60)

rows, cols = f.shape
cx, cy = (cols - 1) / 2, (rows - 1) / 2


def bilinear_interpolate(f, x, y):
    x1, y1 = int(np.floor(x)), int(np.floor(y))
    x2, y2 = min(x1 + 1, cols - 1), min(y1 + 1, rows - 1)

    dx, dy = x - x1, y - y1

    f_xy = (1 - dx) * (1 - dy) * f[y1, x1] + dx * (1 - dy) * f[y1, x2] + \
           (1 - dx) * dy * f[y2, x1] + dx * dy * f[y2, x2]

    return f_xy


new_f = np.zeros_like(f, dtype=np.float32)

for i in range(rows):
    for j in range(cols):
        x_shifted = j - cx
        y_shifted = i - cy

        new_x_shifted = x_shifted * np.cos(theta) - y_shifted * np.sin(theta)
        new_y_shifted = x_shifted * np.sin(theta) + y_shifted * np.cos(theta)

        new_x = new_x_shifted + cx
        new_y = new_y_shifted + cy
        if 0 <= new_x <= cols - 1 and 0 <= new_y <= rows - 1:
            new_f[i, j] = bilinear_interpolate(f, new_x, new_y)

print(new_f)
