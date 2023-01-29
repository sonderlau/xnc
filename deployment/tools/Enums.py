from enum import Enum
from pydantic import BaseModel
from typing import List
# 图片尺寸

IMAGE_SIZE_LENGTH = 1920
IMAGE_SIZE_WIDTH = 1080

# 正则

REGEX_URL = """(?:https?):\/\/(\w+:?\w*)?(\S+)(:\d+)?(\/|\/([\w#!:.?+=&%!\-\/]))?"""

# 域名 白名单

DOMAIN_WHITELIST = ["ncrj.sdsea.top:4433", "i.328888.xyz"]

# ==================================

# * 支持的文件类型
FILE_ACCEPTED_TYPES_LIST = [".jpg", ".jpeg", ".png"]

# * Yolov5 权重文件路径
YOLOV5_WEIGHT_FILE_PATH = "./yolov5-7.0/weights/yolov5s6_1280_.pt"

# * ConvNeXt 权重文件路径
CONVNEXT_WEIGHT_FILE_PATH = (
    "/home/hik/xnc/checkpoint-499.pth"
    # "./checkpoint-499.pth"
)

# ===================================
# 垃圾桶的分类
trash_can_categories = (
    "trash_can_covered",
    "trash_can_overfull",
    "trash_can_uncovered",
)


class StatueCode(int, Enum):
    SUCCEED = 0
    FAILED = -1


class ErrorMessages(str, Enum):
    # * 网络地址文件
    URL_NOT_IN_WHITELIST = "当前域名不在白名单内"
    URL_ASSET_NOT_FOUND = "图片不存在"

    # * 文件路径
    FILE_PATH_EMPTY = "文件路径为空"
    FILE_PATH_INVALID = "目标文件不存在或者路径不合法"

    # * 文件
    FILE_TYPE_NOT_CORRECT = "文件类型不合法!"
    FILE_ACCEPTED_TYPES = "目前支持的格式有 : jpg / jpeg / png"

    # * 模型运行出错
    MODEL_RUN_ERROR = "模型运行出错"

    # * 图片尺寸
    IMG_SIZE_ERROR = "只支持1920*1080大小的图片尺寸"

    # * 地点
    LOCATION_NAME_UNKNOWN = "机位代号不存在"


class SignleDetectionObject(BaseModel):
    name: str
    box: List[float]
    confidence: float


class DetectionResult(BaseModel):
    code: int = StatueCode.FAILED
    data: List[SignleDetectionObject] = []
    msg: str = "Success"