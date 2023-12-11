import cv2
import numpy as np


def detect_lines(image_path, line_width):
    savepath = "."
    # 读取图像
    image = cv2.imread(image_path)

    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 进行边缘检测
    edges = cv2.Canny(gray, 50, 150)

    # 进行霍夫变换检测直线
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=line_width, maxLineGap=10)

    # 根据直线的方向进行分组
    vertical_lines = []
    horizontal_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(x2 - x1) > abs(y2 - y1):
            vertical_lines.append(line[0])
        else:
            horizontal_lines.append(line[0])

    # 对横线进行裁剪
    for line in horizontal_lines:
        x1, y1, x2, y2 = line
        cropped_image = image[y1:y2, x1:x2]
        # 在这里可以对裁剪后的图像进行进一步处理，比如保存或显示
        cv2.imwrite(savepath + "\\vertical.jpg", cropped_image, [cv2.IMWRITE_AVIF_QUALITY, 98])

    # 对竖线进行裁剪
    for line in vertical_lines:
        x1, y1, x2, y2 = line
        cropped_image = image[y1:y2, x1:x2]
        # 在这里可以对裁剪后的图像进行进一步处理，比如保存或显示
        cv2.imwrite(savepath + "\\horizontal.jpg", cropped_image, [cv2.IMWRITE_AVIF_QUALITY, 98])


if __name__ == '__main__':
    # 调用函数进行识别和裁剪
    detect_lines('image.jpg', 2)
