from PIL import Image
import os
from tools.debris_detection_utils import (
    polygon_crop,
    get_road_info,
    binaryzation,
    find_contours
)

import cv2
import numpy as np

# ! 存储文件地址
ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
BASELINE_PATH = "/baseline"


def debris_detection(img_path, location: str):
    """识别图片中是否有杂物堆

    Args:
        img_path (string): 待识别的图片的路径
        location (string): 图片所属机位的代号

    Returns:
        List: 物体轮廓数组 / -1 机位名称不存在
        str: 地址名称 
    """

    configs = get_road_info(f"{ABSOLUTE_PATH}{BASELINE_PATH}")

    location_info = configs[location]  # 道路信息


    # ! 机位名称不存在
    if location_info == None:
        return -1, location_info["name"]

    img = Image.open(img_path).convert("RGB")  # 待识别图片
    img_baseline = Image.open(f"{ABSOLUTE_PATH}{BASELINE_PATH}/{location}.jpg").convert(
        "RGB"
    )  # 基准图片

    # img.save("./assets/img.jpg")
    # img_baseline.save("./assets/baseline.jpg")

    # # * 对两图片中识别物体 遮罩
    # img = mask_detected_objects(img, boxes)
    # img_baseline = mask_detected_objects(img_baseline, boxes)

    # * 裁剪图片
    edges = tuple(tuple(i) for i in location_info["edge"])
    
    img = polygon_crop(img, edges)
    img_baseline = polygon_crop(img_baseline, edges)

    # img.save("./assets/polygon_img.jpg")
    # img_baseline.save("./assets/polygon_baseline.jpg")

    # * 比对 生成比对值的二值化图片
    img_difference = binaryzation(img, img_baseline)
    
    # TODO: 传 Image 转数组后的结果到 OpenCV 中，识别结果有问题
    # TODO: 图片格式规范化

    TMP_IMAGE_PATH = "./assets/temporary.jpg"

    img_difference.save(TMP_IMAGE_PATH)
    # * 寻找轮廓
    img = cv2.imdecode(np.fromfile(TMP_IMAGE_PATH, np.uint8), cv2.CV_8UC1)
    return (find_contours(img, params=configs["params"]), location_info["name"])
