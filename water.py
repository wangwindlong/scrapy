import cv2
import numpy as np

# 加载图片
image = cv2.imread('image.jpg')

# 将图片转换为灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 对灰度图像进行阈值处理，将白色空隙转换为纯白色
_, threshold = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# 进行形态学操作，去除噪点
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=2)

# 确定背景区域
sure_bg = cv2.dilate(opening, kernel, iterations=3)

# 执行距离变换
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)

# 找到未确定的区域
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)

# 标记分水岭算法的标签
_, markers = cv2.connectedComponents(sure_fg)

# 增加标签值，使得背景标签为1
markers = markers + 1

# 将未确定的区域标记为0
markers[unknown == 255] = 0

# 应用分水岭算法
markers = cv2.watershed(image, markers)
image[markers == -1] = [0, 0, 255]  # 将分割线标记为红色

# 显示结果
cv2.imshow('Segmented Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()