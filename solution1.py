# 验证验证码
import itertools
from queue import Queue

import cv2


def get_dynamic_binary_image(source_path, to_path):
    """获取 灰度/二值图"""
    im = cv2.imread(source_path)

    # 灰度化
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # 二值化
    th1 = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21,  1)
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



# cfs 切割
def cfs(im, x_fd, y_fd):
    """

    """
    h, w = img.shape[:2]
    for y, x in itertools.product(range(0, h), range(0, w)):





  xaxis=[]
  yaxis=[]
  visited =set()
  q = Queue()
  q.put((x_fd, y_fd))
  visited.add((x_fd, y_fd))
  offsets=[(1, 0), (0, 1), (-1, 0), (0, -1)]#四邻域

  while not q.empty():
      x,y=q.get()

      for xoffset,yoffset in offsets:
          x_neighbor,y_neighbor = x+xoffset,y+yoffset

          if (x_neighbor,y_neighbor) in (visited):
              continue  # 已经访问过了

          visited.add((x_neighbor, y_neighbor))

          try:
              if im[x_neighbor, y_neighbor] == 0:
                  xaxis.append(x_neighbor)
                  yaxis.append(y_neighbor)
                  q.put((x_neighbor,y_neighbor))

          except IndexError:
              pass

  # print(xaxis)
  if (len(xaxis) == 0 | len(yaxis) == 0):
    xmax = x_fd + 1
    xmin = x_fd
    ymax = y_fd + 1
    ymin = y_fd

  else:
    xmax = max(xaxis)
    xmin = min(xaxis)
    ymax = max(yaxis)
    ymin = min(yaxis)
    #ymin,ymax=sort(yaxis)

  return ymax,ymin,xmax,xmin

def detectFgPix(im,xmax):
  '''搜索区块起点
  '''

  h,w = im.shape[:2]
  for y_fd in range(xmax+1,w):
      for x_fd in range(h):
          if im[x_fd,y_fd] == 0:
              return x_fd,y_fd


def CFS(im):
    """切割字符位置"""
    zoneL = []  # 各区块长度L列表
    zoneWB = []  # 各区块的X轴[起始，终点]列表
    zoneHB = []  # 各区块的Y轴[起始，终点]列表

    xmax = 0
    # 上一区块结束黑点横坐标,这里是初始化
    for i in range(10):

        try:
            x_fd, y_fd = detectFgPix(im, xmax)
            # print(y_fd,x_fd)
            xmax, xmin, ymax, ymin = cfs(im, x_fd, y_fd)
            L = xmax - xmin
            H = ymax - ymin
            zoneL.append(L)
            zoneWB.append([xmin, xmax])
            zoneHB.append([ymin, ymax])

        except TypeError:
            return zoneL, zoneWB, zoneHB

    return zoneL, zoneWB, zoneHB


def find_contours(img):
    result = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow("binary2", img)
    print()



if __name__ == '__main__':
    img = get_dynamic_binary_image("img.png", "dio.png")
    img = clear_border(img, "dio2.png")
    img = interference_line(img, "dio3.png")
    img = interference_point(img, "dio4.png")
    # find_contours(img)
