import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图像并转换为浮点型
image = cv2.imread('plane.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 转换为RGB
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # 灰度化

# 自适应阈值进行二值化
T, BW = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 使用Otsu算法自动获取阈值

# 显示二值化图像
plt.figure()
plt.imshow(BW, cmap='gray')
plt.title('二值化图像')
plt.show()

# 形态学滤波：开运算 + 闭运算
kernel = np.ones((3, 3), np.uint8)
Morph = cv2.morphologyEx(BW, cv2.MORPH_OPEN, kernel)  # 开运算
Morph = cv2.morphologyEx(Morph, cv2.MORPH_CLOSE, kernel)  # 闭运算

# 显示形态学滤波后的图像
plt.figure()
plt.imshow(Morph, cmap='gray')
plt.title('形态学滤波')
plt.show()

# 找到边界并绘制
contours, _ = cv2.findContours(Morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[-1::]

# 绘制轮廓
plt.figure()
plt.imshow(Morph, cmap='gray')
plt.title('划分的区域')
for contour in contours:
    contour = contour.squeeze()  # 去掉多余的维度
    plt.plot(contour[:, 0], contour[:, 1], 'r', linewidth=2)
plt.show()

# 对每个轮廓进行傅里叶变换处理
M = np.zeros(len(contours))  # 记录每个轮廓要保留的傅里叶系数数量
S = np.zeros_like(Morph)

for k, contour in enumerate(contours):
    N = len(contour)
    if N % 2 != 0:  # 如果轮廓点数是奇数，添加一个点
        contour = np.vstack([contour, contour[-1]])
        N += 1
    M[k] = int(N * 1 / 4)  # 计算傅里叶变换后要保留的系数数量
    contour = contour.reshape(-1, 2)

    # 对每个轮廓的坐标进行傅里叶变换
    z = contour[:, 1] + 1j * contour[:, 0]  # 使用复数表示坐标
    Z = np.fft.fft(z)
    Y = np.abs(Z)
    I = np.argsort(Y)  # 按照幅度排序

    Z[I[range(int(M[k]))]] = 0  # 去除幅度最小的部分
    zz = np.fft.ifft(Z)  # 逆傅里叶变换得到去噪后的轮廓
    zz = zz[::-1]  # 逆序
    # 绘制去噪后的轮廓
    plt.plot(np.real(zz), np.imag(zz), 'b', linewidth=2)
plt.show()
