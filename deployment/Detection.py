from PIL import Image
from fastapi import FastAPI

import os


# import uvicorn
from debris_detection import debris_detection
from time import time

# utils
from tools.Enums import (
    StatueCode,
    ErrorMessages,
    SignleDetectionObject,
    DetectionResult,
    IMAGE_SIZE_LENGTH,
    IMAGE_SIZE_WIDTH,
)

from detection_inference import (
    yolov5_inference,
    recognition_process,
    trash_can_classification,
)
from tools.image_path import validate_image
from tools.compute import compute_debris_box

start = time()


def calc_time(start):
    print(time() - start)
    start = time()


# * 根目录
ROOT_PATH = os.getcwd()


# ==================================
# * 初始化
app = FastAPI()


@app.get("/detect", response_model=DetectionResult)
async def detect(path: str = "", location: str = ""):

    start = time()

    # 返回内容格式
    resp = DetectionResult()
    resp.code = StatueCode.FAILED

    # 校验图片地址
    try:
        file_full_path = validate_image(path, ROOT_PATH)
    except Exception as e:
        # 返回错误信息
        resp.msg = repr(e)
        return resp
    
    print(file_full_path)
    # 读入 图片
    image_in = Image.open(file_full_path)

    # 图片长宽
    img_length, img_width = image_in.size

    if img_length != IMAGE_SIZE_LENGTH or img_width != IMAGE_SIZE_WIDTH:
        resp.msg = ErrorMessages.IMG_SIZE_ERROR
        return resp

    print("Validation Done")
    calc_time(start)

    # ? 非垃圾桶 直接放入结果集
    # ? cleaner / car / trash_can

    result = yolov5_inference(image_in)

    r, flag = recognition_process(result, img_length, img_width)

    print("Common Objects Done")
    calc_time(start)

    # * 垃圾桶再分类
    # * 与上述识别结果拼接
    resp.data = trash_can_classification(result, image_in) + r

    resp.code = StatueCode.SUCCEED

    print("Trash_can classification Done")
    calc_time(start)

    # ---杂物堆识别---------------------------------------------

    if location == "":
        # * 未指定 机位 不识别杂物堆 直接返回
        return resp

    if flag == True:
        # * 存在 行人/车辆 不识别杂物堆
        return resp

    result_debris, location_name = debris_detection(file_full_path, location)

    if result_debris == -1:
        # 未找到机位代号
        resp.code = StatueCode.FAILED
        resp.msg = ErrorMessages.LOCATION_NAME_UNKNOWN
        return resp

    # 遍历所有的结果
    for debris in result_debris:
        debris_dict = {
            "name": "debris_pile",
            "confidence": 1.0,
            "box": compute_debris_box((img_width, img_length), debris),
        }

        resp.data.append(SignleDetectionObject(**debris_dict))

    # 地点名称 + 代号
    return resp


import uvicorn
if __name__ == "__main__":
    # todo: debug
    uvicorn.run(app, port=8521, host='192.168.1.33')
