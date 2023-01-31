from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import cv2
import json
import os
from gray_image import gray, polygon_crop


def sort_two_num(first, second):
    """按照大到小 排序两个参数 大 小

    Args:
        first (_type_): 数字
        second (_type_): 数字

    Returns:
        Tuple: 大,小
    """
    if first > second:
        return first, second
    else:
        return second, first


def binaryzation(test, origin):
    """图片比对得到二值化后的待识别图

    Args:
        test (Pillow Image): 实例图
        origin (Pillow Image): 基准图
        threshold (int): 二值化的阈值 (0-255)

    Returns:
        Pillow Image: 遮罩后的图片
    """

    # TODO: 图片尺寸
    # 1920 * 1080
    w, h = origin.size

    # 转换为数组
    # shape = (1080, 1920, 3)
    test = np.array(test, dtype=int)
    origin = np.array(origin, dtype=int)

    # 黑 / 白  图层
    black = np.ones((h, w), dtype=np.uint8) * 255
    white = np.zeros((h, w), dtype=np.uint8)

    # 计算 RGB 差值平方 之和
    binarized = np.sum((origin - test) ** 2, axis=2)

    # 阈值筛

    sum = np.divide(binarized, (255 * 3), dtype=np.float32)

    # 取整 转 8bit
    sum = np.around(sum).astype(np.uint8)
    # filtered = Image.fromarray(filtered, "L")


    return cv2.adaptiveThreshold(
        sum,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=7,
        C=0,
    )


def find_contours(img_binary):
    """找到最大包括的椭圆形

    Args:
        img_binary (OpenCV Image): 二值化后的图片
        params (Enum): 限制参数
    """
    # MIN_IMAGE_AREA =
    MAX_IMAGE_AREA = 17100
    MIN_IMAGE_SIZE = 20

    # 寻找最大边界
    contours, _ = cv2.findContours(
        img_binary, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE
    )

    # 筛选后的边界
    contours_filtered = []
    contours_ignored = [[], [], []]  # 太小  # 太大  # 比例

    # 遍历结果
    for i in contours:

        # 框选面积
        S = cv2.contourArea(i)

        if S < 500:
            # contours_ignored.append(cv2.boundingRect(i))
            continue

        # 椭圆形拟合边界
        ellipse = cv2.fitEllipse(i)

        # print(ellipse)

        # 长轴 短轴
        w, h = sort_two_num(ellipse[1][0], ellipse[1][1])

        if w < MIN_IMAGE_SIZE:
            # 太小
            contours_ignored[0].append(cv2.boundingRect(i))
            continue

        if np.divide(w, h) > 2.5:
            contours_ignored[2].append(cv2.boundingRect(i))
            continue

        if w > 200:
            contours_ignored[1].append(cv2.boundingRect(i))
            continue

        contours_filtered.append(cv2.boundingRect(i))

    return contours_filtered, contours_ignored


# def multi_binarization_threshold():

colors = [
    (139, 194, 76),  # 绿色 - 小
    (255, 245, 145),  # 黄色 - 大
    (45, 36, 138),  # 紫色 - 比例
]

# 遍历所有图片
edge = ""
with open("road_edge.json", "r") as edges:
    edge = json.load(edges)

filenames = os.listdir(r"./pics")

for file in filenames:

    baseline_name = file.split("-")[0]
    baseline = Image.open(f"../dataset/baseline/{baseline_name}.jpg").convert("RGB")
    img = Image.open(f"./pics/{file}").convert("RGB")

    location_params = edge[baseline_name]
    threshold = int(location_params["threshold"])

    # 多边形遮罩
    xys = tuple(tuple(i) for i in location_params["edge"])

    baseline = polygon_crop(baseline, xys)
    img = polygon_crop(img, xys)

    # ? 只使用 一档 47
    BLUR_RADIUS = 9
    result = binaryzation(img, baseline)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    coutours, contours_ignored = find_contours(result)

    draw = ImageDraw.Draw(img)

    for c in coutours:

        draw.rectangle(
            [c[0], c[1], c[0] + c[2], c[1] + c[3]], outline=(255, 0, 0), width=5
        )

    for i in range(3):
        for c in contours_ignored[i]:

            draw.rectangle(
                [c[0], c[1], c[0] + c[2], c[1] + c[3]], outline=colors[i], width=5
            )

    img.save(f"./coutours/{file}", mode="L")
