import itertools

from cv2 import cv2


# 灰度化 / 二值化
def get_dynamic_binary_image(source_path, to_path, clear_size=21):
    """灰度/二值图"""
    im = cv2.imread(source_path)
    # 灰度化
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # 二值化
    th1 = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51,  1)
    cv2.imwrite(to_path, th1)
    return th1


def clear_border(img, to_path, border_size=2):
    """清除边框"""
    h, w = img.shape[:2]
    for y, x in itertools.product(range(0, w), range(0, h)):
        if y < border_size or y > w - border_size:
            img[x, y] = 255
        if x < border_size or x > h - border_size:
            img[x, y] = 255
    cv2.imwrite(to_path, img)
    return img


# 点降噪
def interference_point(img, to_path, count_=5):
    """
    9邻域框,以当前点为中心的田字框,黑点个数
    :param to_path:
    :param x:
    :param y:
    :return:
    """
    # todo 判断图片的长宽度下限
    h, w = img.shape[:2]

    for y, x in itertools.product(range(1, w - 1), range(1, h - 1)):
        count = 0
        for val in (img[x, y - 1], img[x, y + 1], img[x - 1, y], img[x + 1, y], img[x - 1, y - 1], img[x - 1, y + 1],
                    img[x + 1, y - 1], img[x + 1, y + 1]):
            if val > 245:
                count = count + 1
        if count >= count_:
            img[x, y] = 255

    for y, x in itertools.product(range(1, w - 1)[::-1], range(1, h - 1)[::-1]):
        count = 0
        for val in (img[x, y - 1], img[x, y + 1], img[x - 1, y], img[x + 1, y], img[x - 1, y - 1], img[x - 1, y + 1],
                    img[x + 1, y - 1], img[x + 1, y + 1]):
            if val > 245:
                count = count + 1
        if count >= count_:
            img[x, y] = 255
    cv2.imwrite(to_path, img)
    return img


def interference_line(img, to_path):
    """清除线噪音"""
    h, w = img.shape[:2]
    for y, x in itertools.product(range(1, w - 1), range(1, h - 1)):
        count = 0
        for val in (img[x, y - 1], img[x, y + 1], img[x - 1, y], img[x + 1, y]):
            if val > 245:
                count = count + 1
        if count > 2:
            img[x, y] = 255
    cv2.imwrite(to_path, img)
    return img


if __name__ == '__main__':
    img = get_dynamic_binary_image("dio-1.jpg", "dio.png", 91)
    img = clear_border(img, "dio2.png", 10)
    img = interference_line(img, "dio3.png")
    img = interference_point(img, "dio4.png")
