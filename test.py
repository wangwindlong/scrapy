import cv2
import numpy as np

# 读取图像
image = cv2.imread('image.jpg')

# 将图像转换为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 对灰度图像进行阈值处理，将白色空隙转换为纯白色
_, threshold = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)

# 进行形态学操作，去除噪点
kernel = np.ones((2, 2), np.uint8)
opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=1)
# 使用Canny边缘检测
edges = cv2.Canny(opening, 100, 150)

# 进行膨胀和腐蚀操作
kernel = np.ones((2,2), np.uint8)
dilated = cv2.dilate(edges, kernel, iterations=3)
eroded = cv2.erode(dilated, kernel, iterations=2)

# 使用霍夫变换检测直线
lines = cv2.HoughLinesP(eroded, 1, np.pi/180, threshold=100, minLineLength=150, maxLineGap=3)

# 绘制检测到的直线
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 1)

# 显示结果图像
cv2.imshow('Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
