
from torch import load


from numpy import exp
import torch.hub as th
import os
import torch.nn as nn


from torchvision import transforms
from ConvNeXt.models.convnext import convnext_tiny

from tools.Enums import SignleDetectionObject, trash_can_categories
from tools.compute import compute_box_param
from tools.compute import resize_image_to_224

# !!! 配置
# * 根目录
ROOT_PATH = os.getcwd()

# * Yolov5 权重文件路径
YOLOV5_WEIGHT_FILE_PATH = "./yolov5-7.0/weights/v19_augmented_1280_3.pt"

# * ConvNeXt 权重文件路径
CONVNEXT_WEIGHT_FILE_PATH = (
    "/home/hik/xnc/checkpoint-499.pth"
)
# !!!

# YOLOv5
model = th.load("./yolov5-7.0", "custom", path=YOLOV5_WEIGHT_FILE_PATH, source="local",  _verbose=False)

# ConvNext
convnext = convnext_tiny(pretrained=False, in_22k=False)
# 修改 Linear 层 768 -> 3
convnext.head = nn.Linear(768, 3)
convnext.load_state_dict(load(CONVNEXT_WEIGHT_FILE_PATH)["model"])


def yolov5_inference(img):
    return model(img, size=1280, augment=True).pandas().xyxy[0]

def convnext_inference(img):
    return convnext(img)

# Image transfrom
transform_method = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ]
)

def recognition_process(result, img_length, img_width ):
    """归一化YOLO识别结果

    Args:
        result (_type_): YOLO识别结果
        img_length (_type_): 图片长
        img_width (_type_): 图片宽

    Returns:
        List: SingleDetectionObject 物体
        Flag: Boolean 是否有目标物体
    """
    r = []
    flag = False
    for _, row in result.iterrows():
        name = row["name"]
        
        
        # ! 垃圾桶 这里不处理
        if name == "trash_can":
            continue
        
        
        if name == "people" or name == "car":
            flag = True

        detected_datas = {}

        detected_datas["name"] = row["name"]
        detected_datas["confidence"] = row["confidence"]

        # 归一化位置
        detected_datas["box"] = compute_box_param(
            (img_width, img_length), row, 0, 0
        )

        r.append(SignleDetectionObject(**detected_datas))
    return r,flag

def trash_can_classification(result, detect_img):
    img_length, img_width = detect_img.size
    r = []
    for _, row in result.iterrows():
        
        detected_datas = {}
        
        #* 只处理垃圾桶
        if row["name"] != "trash_can":
            continue
        
        croped = detect_img.crop(
                    (row["xmin"], row["ymin"], row["xmax"], row["ymax"]))
        
        # 尺寸 224x224
        croped = resize_image_to_224(croped)

        croped = transform_method(croped).unsqueeze(0)

        # 对每个分类的值取 自然指数
        result = convnext_inference(croped).detach().squeeze(0).apply_(exp)

        # 每个分类的概率和
        sum = result.sum()
        predict = (result / sum).tolist()

        # 取得分类结果
        detected_datas["name"] = trash_can_categories[
            predict.index(max(predict))
        ]

        # 可信度 计算 两者较小值
        detected_datas["confidence"] = min(max(predict), row["confidence"])

        detected_datas["box"] = compute_box_param(
            (img_width, img_length), row, 0, 0
        )

        if detected_datas["confidence"] > 0.5:
            r.append(SignleDetectionObject(**detected_datas))
    return r

    
    
    
    
    
    
    
    # 1920 * 1080
    # 使用滑动窗口检测垃圾桶

    # for x in range(
    #     0, 1600, 260
    # ):  # (0，360；260，620；520，880；780，1040，1400；1300，1660；1560，1920；)
    #     for y in range(0, 960, 240):  # (0，360；240，600；480，860；720，1080；)
    #         detect_img = image_in.crop((x, y, x + 360, y + 360))  # 360 * 360
    #         # 预测结果
    #         try:
    #             result = yolov5_inference(image_in).pandas().xyxy[0]
    #             # print(result)
    #         except Exception as e:
    #             # resp.msg = e
    #             resp.code = StatueCode.FAILED
    #             return resp

    #         for _, row in result.iterrows():

    #             # ? 还需要对垃圾桶再进行一次分类识别

    #             # print(row)

    #             if row["name"] == "trash_can":

    #                 # 对垃圾桶种类 分类

    #                 detected_datas = {}

    #                 # * 裁剪图片
    #                 croped = detect_img.crop(
    #                     (row["xmin"], row["ymin"], row["xmax"], row["ymax"])
    #                 )

    #                 # 尺寸 224x224
    #                 croped = resize_image_to_224(croped)

    #                 croped = transform_method(croped).unsqueeze(0)

    #                 # 对每个分类的值取 自然指数
    #                 result = convnext_inference(croped).detach().squeeze(0).apply_(exp)

    #                 # 每个分类的概率和
    #                 sum = result.sum()
    #                 predict = (result / sum).tolist()

    #                 # 取得分类结果
    #                 detected_datas["name"] = trash_can_categories[
    #                     predict.index(max(predict))
    #                 ]

    #                 # 可信度 计算 两者较小值
    #                 detected_datas["confidence"] = min(max(predict), row["confidence"])

    #                 detected_datas["box"] = compute_box_param(
    #                     (img_width, img_length), row, x, y
    #                 )

    #                 if detected_datas["confidence"] > 0.5:
    #                     resp.data.append(SignleDetectionObject(**detected_datas))
