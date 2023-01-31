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