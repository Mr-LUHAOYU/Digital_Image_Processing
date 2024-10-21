import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import cv2

INTERS = ['NEAREST', 'LANCZOS', 'BILINEAR', 'BICUBIC', 'BOX', 'HAMMING']
image_path = "img.jpeg"
image1 = Image.open(image_path)
current_image = image1
scale_factor = 1.0
angle_total = 0.0
isGray = False
current_INTER = 2
current_channels = [0, 1, 2]
flip_and_concatenate = False
bitnot = False
current_grayMethod = 'L'


def cal_convertList(channels):
    std_channels = {
        'R': 0, 'G': 1, 'B': 2,
    }
    convert_list = []
    for channel in channels:
        convert_list.append(std_channels[channel])
    return convert_list


def merge_color_channels(channel1, channel2):
    ans = []
    for channel in channel2:
        ans.append(channel1[channel])
    return ans


def swap_color_channels(image, convert_list):
    img_np = np.array(image)
    swapped_img = img_np[..., convert_list]
    return Image.fromarray(swapped_img)


def to_grayscale(image, method='L'):
    if method == 'L':
        img_np = np.array(image)
        gray_img = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        gray_image = Image.fromarray(gray_img)
    elif method == 'average':
        img_np = np.array(image)
        gray_img = np.mean(img_np, axis=2)
        gray_image = Image.fromarray(gray_img)
    elif method == 'max':
        img_np = np.array(image)
        gray_img = np.max(img_np, axis=2)
        gray_image = Image.fromarray(gray_img)
    elif method == 'min':
        img_np = np.array(image)
        gray_img = np.min(img_np, axis=2)
        gray_image = Image.fromarray(gray_img)
    else:
        raise ValueError('Invalid method for grayscale conversion.')
    return gray_image


def selectINTER(INTER: str):
    return INTERS.index(INTER)


def rotate_image(image, angle: float, scale: float, INTER):
    scale *= 0.3
    new_image = image.resize(
        (int(image.size[0] * scale), int(image.size[1] * scale)),
        resample=INTER
    )
    new_image = new_image.rotate(angle, expand=True)
    return new_image


def bitwise_not(image):
    img_np = np.array(image)
    not_img = cv2.bitwise_not(img_np)
    return Image.fromarray(not_img)


root = tk.Tk()
root.title("Image Operation")
root.geometry("1920x1080")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

operation_var = tk.StringVar(value="Original Image")
operation_label = ttk.Label(left_frame, text="Select Operation:")
operation_label.pack(pady=20)

operation_menu = ttk.Combobox(left_frame, textvariable=operation_var, state='readonly')
operation_menu['values'] = (
    "Original Image", "Swap Color Channels", "Grayscale",
    "Rotate", "Flip and Concatenate", "Bitwise Not",
)
operation_menu.pack(pady=20)

angle_label = ttk.Label(left_frame, text="Rotation Angle (degrees):")
angle_label.pack(pady=10)
angle_default = tk.StringVar(value="0.0")
angle_entry = ttk.Entry(left_frame, textvariable=angle_default)
angle_entry.pack(pady=10)

scale_label = ttk.Label(left_frame, text="Scale Factor:")
scale_label.pack(pady=10)
scale_default = tk.StringVar(value="1.0")
scale_entry = ttk.Entry(left_frame, textvariable=scale_default)
scale_entry.pack(pady=10)

INTER_var = tk.StringVar(value="BILINEAR")
INTER_label = ttk.Label(left_frame, text="Interpolation Method:")
INTER_label.pack(pady=10)
INTER_menu = ttk.Combobox(left_frame, textvariable=INTER_var, state='readonly')
INTER_menu['values'] = INTERS
INTER_menu.pack(pady=10)

channel_label = ttk.Label(left_frame, text="Color Channels to Swap:")
channel_label.pack(pady=10)
channel_default = tk.StringVar(value="RGB")
channel_menu = ttk.Combobox(left_frame, textvariable=channel_default, state='readonly')
channel_menu['values'] = ("RGB", "RBG", "GRB", "GBR", "BGR", "BRG")
channel_menu.pack(pady=10)

gray_label = ttk.Label(left_frame, text="Grayscale Conversion Method:")
gray_label.pack(pady=10)
gray_default = tk.StringVar(value="L")
gray_menu = ttk.Combobox(left_frame, textvariable=gray_default, state='readonly')
gray_menu['values'] = ("L", "average", "max", "min", "mean")
gray_menu.pack(pady=10)

image_label = ttk.Label(right_frame)
image_label.pack(pady=10, fill=tk.BOTH, expand=True)


def init_image():
    global angle_total, scale_factor, isGray, current_INTER, current_channels, \
        flip_and_concatenate, bitnot, current_grayMethod
    angle_total = 0.0
    scale_factor = 1.0
    isGray = False
    current_INTER = 2
    current_channels = [0, 1, 2]
    flip_and_concatenate = False
    bitnot = False


def flip8concatenate(img):
    imgLD = img.copy()
    imgLU = cv2.flip(imgLD, 0)
    imgRU = cv2.flip(imgLU, 1)
    imgRD = cv2.flip(imgLD, 1)
    left = np.concatenate((imgLU, imgLD), axis=0)
    right = np.concatenate((imgRU, imgRD), axis=0)
    imgMerge = np.concatenate((left, right), axis=1)
    return imgMerge


def update_image(*args, **kwargs):
    global angle_total, scale_factor, isGray, current_INTER, current_channels, \
        flip_and_concatenate, bitnot, current_grayMethod
    operation = kwargs.get('operation', 'Original Image')
    if operation == "Original Image":
        init_image()
    elif operation == "Swap Color Channels":
        channels = kwargs.get('channels', 'RGB')
        channels = cal_convertList(channels)
        current_channels = merge_color_channels(current_channels, channels)
    elif operation == "Grayscale":
        new_method = kwargs.get('method', 'L')
        isGray = new_method != current_grayMethod
        current_grayMethod = new_method
    elif operation == "Rotate":
        try:
            angle = float(angle_entry.get())
            scale = float(scale_entry.get())
            angle_total += angle + 360
            angle_total %= 360
            scale_factor *= scale
            current_INTER = selectINTER(kwargs.get('INTER', 'BILINEAR'))
        except ValueError as e:
            print(e)
            angle_entry.delete(0, tk.END)
            scale_entry.delete(0, tk.END)
            init_image()
    elif operation == "Flip and Concatenate":
        flip_and_concatenate = not flip_and_concatenate
    elif operation == "Bitwise Not":
        bitnot = not bitnot
    else:
        init_image()
    display_image()


def display_image():
    img = image1
    if isGray:
        img = to_grayscale(img)
    else:
        img = swap_color_channels(img, current_channels)
    img = rotate_image(img, angle_total, scale_factor, current_INTER)
    if flip_and_concatenate:
        img = Image.fromarray(flip8concatenate(np.array(img)))
    if bitnot:
        img = bitwise_not(img)
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk


operation_menu.bind("<<ComboboxSelected>>",
                    lambda e: update_image(operation=operation_var.get(), INTER=INTER_var.get()))
INTER_menu.bind("<<ComboboxSelected>>", lambda e: update_image(operation='Rotate', INTER=INTER_var.get()))
channel_menu.bind("<<ComboboxSelected>>",
                  lambda e: update_image(operation='Swap Color Channels', channels=channel_default.get()))
gray_menu.bind("<<ComboboxSelected>>", lambda e: update_image(operation='Grayscale', method=gray_default.get()))
update_image()
root.mainloop()
