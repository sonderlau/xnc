from PIL import Image

def resize_image_to_224(image):
    """从最上方开始使用 LANCZOS 对图片取 224 x 224 大小"""
    return image.resize(
        (224, 224),
        resample=Image.LANCZOS,
        box=(0, 0, image.width, min(image.height, 224)),
    )


def compute_box_param(img_size, row, x, y):
    """识别结果 box 的归一化后的参数

    Args:
        img_size (Tuple): (img_width, img_length) 宽x高
        row (_type_): Yolov5 的识别结果
        x : 
        y : 

    Returns:
        box (List): [left, top, width, height]
    """

    # 归一化位置
    img_length = img_size[1]
    img_width = img_size[0]

    left = (row["xmin"] + x) / img_length
    top = (row["ymin"] + y) / img_width
    width = (row["xmax"] - row["xmin"]) / img_length
    height = (row["ymax"] - row["ymin"]) / img_width

    return [left, top, width, height]


def compute_debris_box(img_size, coordinate):
    """识别结果 box 的归一化后的参数
       用于 杂物堆 参数的校正

    Args:
        img_size (Tuple): (img_width, img_length) 宽x高
        coordinate (List): boudingRectangle 的坐标和长宽

    Returns:
        box (List): [left, top, width, height]
    """

    img_length = img_size[1]
    img_width = img_size[0]

    # [(864, 632, 64, 40)]

    left = coordinate[0] / img_length
    top = coordinate[1] / img_width
    width = coordinate[2] / img_length
    height = coordinate[3] / img_width

    return [left, top, width, height]