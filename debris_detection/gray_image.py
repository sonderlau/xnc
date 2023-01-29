"""灰度图片生成

pics/                  实例图片
gray_out/              生成的灰度图
../dataset/baseline    基准图片  

"""

import os
from PIL import Image, ImageDraw
import numpy as np
from PIL import Image
import json

def gray(test, origin):
    # 转换为数组
    # shape = (1080, 1920, 3)
    test = np.array(test, dtype=np.int16)
    origin = np.array(origin, dtype=np.int16)

    # 计算 RGB 差值平方 之和
    sum = np.sum((origin - test) ** 2, axis=2, dtype=np.float32)

    # 每个像素点的计算值大小: [0, 255*255*3]
    # 将该值放缩到 0-255 范围内

    sum = np.divide(sum, (255 * 3), dtype=np.float32)

    # 取整 转 8bit
    sum = np.around(sum).astype(np.uint8)

    return Image.fromarray(sum, "L")
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

# 遍历所有图片
edge = ""
with open("road_edge.json", "r") as edges:
    edge = json.load(edges)

filenames = os.listdir(r"./pics")

for file in filenames:

    baseline_name = file.split("-")[0]
    baseline = Image.open(f"../dataset/baseline/{baseline_name}.jpg").convert("RGB")
    img = Image.open(f"./pics/{file}").convert("RGB")

    # 多边形遮罩
    xys = tuple(tuple(i) for i in edge[baseline_name]["edge"]) 
    
    baseline = polygon_crop(baseline, xys)
    img = polygon_crop(img, xys)

    result = gray(img, baseline)

    result.save(f"./output/{file}", mode="L")
