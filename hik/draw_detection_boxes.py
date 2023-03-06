"""
发送识别请求，并绘制识别的框
"""
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

URL = "http://116.233.79.75:8521/detect"

IMAGE_URL = """https://ncrj.sdsea.top/resource/image/camera_images/613a3593-e9bd-44b7-8502-f0288e619cf3.jpg"""

# 不同物体的框颜色
colors = {
    "debris_pile": (13, 63, 103),
    "trash_can_overfull": (245, 88, 123),
    "trash_can_covered": (139, 194, 76),
    "trash_can_uncovered": (255, 245, 145),
    "people": (45, 36, 138),
    "car": (253, 112, 19),
}

payload = {"path": IMAGE_URL, "location": "247DMSH"}

FONT_SIZE = 700

r = requests.get(URL, params=payload).json()

response = requests.get(IMAGE_URL, verify=False)
image = Image.open(BytesIO(response.content))

img_length, img_width = image.size

font = ImageFont.truetype("LXGWWenKaiMono-Regular.ttf", FONT_SIZE)

for box in r["data"]:
    print(box["name"])

    detection_points = box["box"]
    left = detection_points[0] * img_length
    top = detection_points[1] * img_width
    width = detection_points[2] * img_length
    height = detection_points[3] * img_width

    # 计算绘制矩形的点

    x_0 = left
    y_0 = top

    x_1 = x_0 + width
    y_1 = y_0 + height

    draw = ImageDraw.ImageDraw(image)

    # 颜色
    color = colors[box["name"]]
    
    # 物体方框
    draw.rectangle([x_0, y_0, x_1, y_1], fill=None, outline=color, width=5)

    # 文字框
    # x 轴不变
    font_y = y_0 - 15 if y_0 - 5 > FONT_SIZE else y_1
    draw.text((x_0, font_y), box["name"], fill=color)

image.save("./test.jpg")
