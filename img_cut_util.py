import itertools
import queue
from collections import defaultdict
from typing import List

from cv2 import cv2
from numpy.core.multiarray import ndarray
from traitlets import Tuple

from img_pretreat_util import get_dynamic_binary_image


def projection_method_cut(img: ndarray, scanning_width: int, high: int, split_size=4):
    """
    投影法 分割

    :param img: img numpy
    :param scanning_width: 检测宽度
    :param high:
    :return:
    """
    begin, end = 0, scanning_width
    h, w = img.shape[:2]

    def zero():
        return 0
    y_count = defaultdict(zero)
    for x in range(0, w):
        for y in range(0, h):
            if img[y, x] == 0:
                y_count[x] += 1

    start, over = min(y_count.keys()), max(y_count.keys())

    for x in range(start, over):
        pass

    return y_count


def cfs(img, cut_size=4):
    """用队列和集合记录遍历过的像素坐标代替单纯递归以解决cfs访问过深问题"""
    filter_set = set()
    result_list = []

    def deeping_search(position, result, search_set):
        """深度查找"""
        displacement_list =[(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, 1), (0, -1)]
        for displacement in displacement_list:
            dis = (position[0] + displacement[0], position[1] + displacement[1])
            if dis in search_set:
                continue

            if img[dis[0], dis[1]] == 0:
                result.append(dis)
                search_set.add(dis)
                deeping_search(dis, result, search_set)
            search_set.add(dis)

    h, w = img.shape[:2]
    for x, y in itertools.product(range(1, w - 1), range(1, h - 1)):

        if (y, x) in filter_set:
            continue

        if img[y, x] == 255:
            filter_set.add((y, x))
            continue
        else:
            result = []
            deeping_search((y, x), result, filter_set)
            result_list.append(result)

    result_list.sort(key=len, reverse=True)

    for result in result_list[:4]:
        max_y = max(result, key=lambda _: _[0])[0]
        min_y = min(result, key=lambda _: _[0])[0]
        max_x = max(result, key=lambda _: _[1])[1]
        min_x = min(result, key=lambda _: _[1])[1]

        # yield list(itertools.product([max_y, min_y], [max_x, min_x]))
        yield [(max_y, min_y), (max_x, min_x)]

if __name__ == '__main__':
    # img = get_dynamic_binary_image("dio-1.jpg", "dio-2.jpg")
    img = get_dynamic_binary_image("di4.png", "di4-2.png")
    for result in cfs(img):
        print(result)
    # print(projection_method_cut(img, 10, 5))



