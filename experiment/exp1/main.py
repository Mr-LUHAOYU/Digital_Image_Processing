import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import cv2

image_path = "1.png"
image1 = Image.open(image_path)
current_image = image1
scale_factor = 1.0
angle_total = 0.0
isGray = False
current_INTER = cv2.INTER_LINEAR
current_channels = [0, 1, 2]


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


def to_grayscale(image):
    gray_image = image.convert('L')
    return gray_image


def selectINTER(INTER: str):
    if INTER == 'NEAREST':
        return cv2.INTER_NEAREST
    elif INTER == 'LINEAR':
        return cv2.INTER_LINEAR
    elif INTER == 'CUBIC':
        return cv2.INTER_CUBIC
    elif INTER == 'AREA':
        return cv2.INTER_AREA
    elif INTER == 'LANCZOS4':
        return cv2.INTER_LANCZOS4
    else:
        return cv2.INTER_LINEAR


def rotate_image(image, angle, scale, INTER):
    img_np = np.array(image)
    if not isGray:
        rows, cols, channels = img_np.shape
    else:
        rows, cols = img_np.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, scale)
    rotated_img = cv2.warpAffine(img_np, M, (cols, rows), flags=INTER, borderValue=(255, 255))
    return Image.fromarray(rotated_img, 'L') if isGray else Image.fromarray(rotated_img, 'RGBA')


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
operation_menu['values'] = ("Original Image", "Swap Color Channels", "Grayscale", "Rotate")
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

INTER_var = tk.StringVar(value="LINEAR")
INTER_label = ttk.Label(left_frame, text="Interpolation Method:")
INTER_label.pack(pady=10)
INTER_menu = ttk.Combobox(left_frame, textvariable=INTER_var, state='readonly')
INTER_menu['values'] = ("NEAREST", "LINEAR", "CUBIC", "AREA", "LANCZOS4")
INTER_menu.pack(pady=10)

channel_label = ttk.Label(left_frame, text="Color Channels to Swap:")
channel_label.pack(pady=10)
channel_default = tk.StringVar(value="RGB")
channel_menu = ttk.Combobox(left_frame, textvariable=channel_default, state='readonly')
channel_menu['values'] = ("RGB", "RBG", "GRB", "GBR", "BGR", "BRG")
channel_menu.pack(pady=10)

image_label = ttk.Label(right_frame)
image_label.pack(pady=10)


def init_image():
    global angle_total, scale_factor, isGray, current_INTER, current_channels
    angle_total = 0.0
    scale_factor = 1.0
    isGray = False
    current_INTER = cv2.INTER_LINEAR
    current_channels = [0, 1, 2]


def update_image(*args, **kwargs):
    global angle_total, scale_factor, isGray, current_INTER, current_channels
    operation = kwargs.get('operation', 'Original Image')
    if operation == "Original Image":
        init_image()
    elif operation == "Swap Color Channels":
        channels = kwargs.get('channels', 'RGB')
        channels = cal_convertList(channels)
        current_channels = merge_color_channels(current_channels, channels)
    elif operation == "Grayscale":
        isGray = not isGray
    elif operation == "Rotate":
        try:
            angle = float(angle_entry.get())
            scale = float(scale_entry.get())
            angle_total += angle + 360
            angle_total %= 360
            scale_factor *= scale
            current_INTER = selectINTER(kwargs.get('INTER', 'LINEAR'))
        except ValueError:
            angle_entry.delete(0, tk.END)
            scale_entry.delete(0, tk.END)
            init_image()
    else:
        init_image()
    display_image()


def display_image():
    img = image1
    if isGray:
        img = to_grayscale(img)
    else:
        img = swap_color_channels(img, current_channels+[3])
    img = rotate_image(img, angle_total, scale_factor, current_INTER)

    siz = (np.array(image1.size) * 0.5).astype(int).tolist()
    img_resized = img.resize(siz)
    img_tk = ImageTk.PhotoImage(img_resized)
    image_label.config(image=img_tk)
    image_label.image = img_tk


operation_menu.bind("<<ComboboxSelected>>", lambda e: update_image(operation=operation_var.get()))
INTER_menu.bind("<<ComboboxSelected>>", lambda e: update_image(operation='Rotate', INTER=INTER_var.get()))
channel_menu.bind("<<ComboboxSelected>>", lambda e: update_image(operation='Swap Color Channels', channels=channel_default.get()))
update_image()
root.mainloop()
