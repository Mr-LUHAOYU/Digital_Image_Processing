import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

f = np.array(Image.open('img.jpeg'))


def bilinear_interpolate(f, x, y):
    h, w = f.shape[:2]

    x1, y1 = int(np.floor(x)), int(np.floor(y))
    x2, y2 = min(x1 + 1, w - 1), min(y1 + 1, h - 1)

    dx = x - x1
    dy = y - y1

    value = (1 - dx) * (1 - dy) * f[y1, x1] + dx * (1 - dy) * f[y1, x2] + \
            (1 - dx) * dy * f[y2, x1] + dx * dy * f[y2, x2]

    return value


def show_image(img, title):
    plt.imshow(img.astype(np.uint8))
    plt.title(title)
    plt.axis('off')
    plt.show()


def rotate_image(f, angle, expand=True):
    h, w = f.shape[:2]
    cx, cy = w / 2, h / 2
    angle_rad = np.radians(angle)

    corners = np.array([
        [-cx, -cy], [w - cx, -cy],
        [-cx, h - cy], [w - cx, h - cy]
    ])

    rotation_matrix = np.array([
        [np.cos(angle_rad), np.sin(angle_rad)],
        [-np.sin(angle_rad), np.cos(angle_rad)]
    ])

    new_corners = np.dot(corners, rotation_matrix.T)

    min_x, min_y = np.min(new_corners, axis=0)
    max_x, max_y = np.max(new_corners, axis=0)

    new_w = int(np.ceil(max_x - min_x))
    new_h = int(np.ceil(max_y - min_y))

    new_cx, new_cy = new_w / 2, new_h / 2

    new_img = np.zeros((new_h, new_w, f.shape[2]), dtype=f.dtype) if len(f.shape) == 3 else np.zeros((new_h, new_w),
                                                                                                     dtype=f.dtype)

    for i in range(new_h):
        for j in range(new_w):
            x_shifted = j - new_cx
            y_shifted = i - new_cy

            original_x_shifted = x_shifted * np.cos(-angle_rad) + y_shifted * np.sin(-angle_rad)
            original_y_shifted = -x_shifted * np.sin(-angle_rad) + y_shifted * np.cos(-angle_rad)

            original_x = original_x_shifted + cx
            original_y = original_y_shifted + cy

            if 0 <= original_x < w and 0 <= original_y < h:
                new_img[i, j] = bilinear_interpolate(f, original_x, original_y)
            else:
                new_img[i, j] = 255

    return new_img


rotated_img = rotate_image(f, 20)
show_image(f, "Original Image")
show_image(rotated_img, "Rotated Image (20°)")


def horizontal_flip(f):
    return f[:, ::-1]


flipped_img = horizontal_flip(rotated_img)
show_image(flipped_img, "Horizontally Flipped Image")


def shear_transform(f, kx, ky):
    h, w = f.shape[:2]

    new_img = np.zeros_like(f)

    for i in range(h):
        for j in range(w):
            new_x = j + kx * i
            new_y = i + ky * j

            if 0 <= new_x < w and 0 <= new_y < h:
                new_img[i, j] = bilinear_interpolate(f, new_x, new_y)

    return new_img


sheared_img = shear_transform(flipped_img, kx=0.3, ky=0.5)
show_image(sheared_img, "Sheared Image (kx=0.3, ky=0.5)")


def scale_image(f, scale_x, scale_y):
    h, w = f.shape[:2]
    new_h, new_w = int(h * scale_y), int(w * scale_x)

    new_img = np.zeros((new_h, new_w, f.shape[2]))

    for i in range(new_h):
        for j in range(new_w):
            src_x = j / scale_x
            src_y = i / scale_y

            new_img[i, j] = bilinear_interpolate(f, src_x, src_y)

    return new_img


scaled_img = scale_image(sheared_img, 0.6, 0.6)
show_image(scaled_img, "Scaled Image (kx=ky=0.6)")

show_image(scaled_img, "Final Transformed Image")
# show_image(scale_image(rotate_image(f, 80), 1.2, 1.2), '')
