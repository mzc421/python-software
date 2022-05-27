import os
import numpy as np
import cv2


# 按照指定图像大小调整尺寸 判断图片是不是正方形，如果不是则增加短边的长度使之变成正方形
def resize_image(image, height, width):
    top, bottom, left, right = (0, 0, 0, 0)

    # 获取图像尺寸
    h, w, _ = image.shape

    # 对于长宽不相等的图片，找到最长的一边
    longest_edge = max(h, w)

    # 计算短边需要增加多上像素宽度使其与长边等长
    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass

    # RGB颜色
    BLACK = [0, 0, 0]

    # 给图像增加边界，是图片长、宽等长，cv2.BORDER_CONSTANT指定边界颜色由value指定
    constant = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)

    # 调整图像大小并返回
    return cv2.resize(constant, (height, width))


# 读取训练数据
images = []
labels = []


def read_path(image_size, path_name):
    for dir_item in os.listdir(path_name):
        # 得到所有文件的绝对路径 os.path.join:连接两个或更多的路径名组件
        path = os.path.abspath(os.path.join(path_name, dir_item))
        # 如果是文件夹，继续递归调用
        if os.path.isdir(path):
            read_path(image_size, path)
        else:
            if dir_item.endswith('.jpg'):
                image = cv2.imread(path)
                # image = resize_image(image, image_size, image_size)
                image = cv2.resize(image, (image_size, image_size))
                # print(image.shape)
                images.append(image)
                labels.append(path_name)

    return images, labels


# 从指定路径读取数据
def load_dataset(image_size, path_name):
    images, labels = read_path(image_size, path_name)

    # 将输入的所有图片转成四维数组，尺寸为(图片数量*IMAGE_SIZE*IMAGE_SIZE*3)
    # 图片为64 * 64像素,一个像素3个颜色值(RGB)
    images = np.array(images)
    # print(images.shape)
    # 标注数据，'tupian2'文件夹下都是我的脸部图像，全部指定为0，另外一个文件夹下是同学的，全部指定为1
    labels = np.array([0 if label.endswith('tupian2') else 1 for label in labels])

    return images, labels


if __name__ == '__main__':
    image_size = 64
    images, labels = load_dataset(image_size, r'./data')
