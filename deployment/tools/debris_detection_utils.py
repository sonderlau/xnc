import json
from PIL import Image, ImageDraw
import cv2
import numpy as np


# -------------------------------------------------------
# ? : 本地测试用
import requests

URL = "http://127.0.0.1:8521/detect"


def get_box(absolute_path: str):
    """获取识别的结果

    Args:
        absolute_path (string): 图片的绝对路径

    Returns:
        Dict: 识别的结果集
    """
    payload = {"path": absolute_path}
    r = requests.get(url=URL, params=payload)
    return r.json()["data"]


# -------------------------------------------------------


def get_road_info(path: str):
    """读取道路边界配置
    返回 Dict
    """
    with open(f"{path}/road_edge.json", "r") as edges:
        return json.load(edges)


# * 裁剪多边形区域
def polygon_crop(img_binary, xys):
    """裁剪出图片中的一块多边形

    Args:
        img_binary (Pillow Image): 待裁剪的图片
        xys (array): 一组坐标组成的数组

    Returns:
        Pillow Image: 裁剪后的图片
    """

    # 遮罩层
    maskimg_binary = Image.new("RGB", img_binary.size, (0, 0, 0))
    
    # 多边形内 1
    #      外 0
    ImageDraw.Draw(maskimg_binary).polygon(xys, fill=(1,1,1), outline=1)
    mask = np.array(maskimg_binary)
    
    filtered = np.array(img_binary) * mask
    
    return Image.fromarray(filtered, "RGB")

# * 可识别物体遮罩
def mask_detected_objects(img_binary, boxes):
    """图片中识别到的物体进行遮罩

    Args:
        img_binary (Pillow Image): 待遮罩的图片
        boxes (Dict): 识别的结果

    Returns:
        Pillow Image: 遮罩后的图片
    """

    width, height = img_binary.size

    # 遍历所有识别的结果
    for _ in boxes:
        # 某个 box
        box = _["box"]

        # 归一化 转换
        x1 = box[0] * width
        y1 = box[1] * height

        x2 = box[2] * width + x1
        y2 = box[3] * height + y1

        # 绘制黑色
        ImageDraw.ImageDraw(img_binary).rectangle(
            ((x1, y1), (x2, y2)), fill=(0, 0, 0), outline=None
        )

    return img_binary


def binaryzation(test, origin):
    """图片比对得到二值化后的待识别图

    Args:
        test (Pillow Image): 实例图
        origin (Pillow Image): 基准图

    Returns:
        Pillow Image: 遮罩后的图片
    """

    # 1920 * 1080
    w, h = origin.size

    # 转换为数组
    # shape = (1080, 1920, 3)
    test = np.array(test, dtype=int)
    origin = np.array(origin, dtype=int)

    # 黑 / 白  图层
    black = np.ones((1080, 1920), dtype=np.uint8) * 255
    white = np.zeros((1080, 1920), dtype=np.uint8)

    # 计算 RGB 差值平方 之和
    binarized = np.sum((origin - test) ** 2, axis=2)

    # 阈值筛选
    filtered = np.where(binarized > 140 ** 2 , black, white)

    return Image.fromarray(filtered, "L")


def find_contours(img_binary, params):
    """找到最大包括的椭圆形

    Args:
        img_binary (OpenCV Image): 二值化后的图片
        params (Enum): 限制参数
    """
    MIN_IMAGE_AREA = params["MIN_IMAGE_AREA"]
    MAX_AREA_WIDTH = params["MAX_IMAGE_WIDTH"]
    MAX_AREA_HEIGHT = params["MAX_IMAGE_HEIGHT"]

    # 寻找最大边界
    contours, _ = cv2.findContours(
        img_binary, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE
    )

    # 筛选后的边界
    contours_filtered = []

    for i in contours:

        # 框选面积
        S = cv2.contourArea(i)

        if S < MIN_IMAGE_AREA:
            continue

        # 椭圆形拟合边界
        ellipse = cv2.fitEllipse(i)
        # 长轴 短轴
        w = ellipse[1][0]
        h = ellipse[1][1]

        if w > MAX_AREA_WIDTH or h > MAX_AREA_HEIGHT:
            continue

        contours_filtered.append(cv2.boundingRect(i))

    return contours_filtered
    # # 绘制边界
    # cv2.drawContours(origin, contours_filtered, contourIdx=-1, color=(0,0,255), thickness=3)

    # cv2.imwrite('cluster.jpg', origin)
