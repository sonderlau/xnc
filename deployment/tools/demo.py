from PIL import Image, ImageDraw
import os
import cv2
import torch.hub as th

# * Yolov5 权重文件路径
YOLOV5_WEIGHT_FILE_PATH = "./yolov5-7.0/weights/yolov5-car85-p70.onnx"

class_types = ('car', 'cleaner', 'people', 'traffic police', 'trash_can')

# yolov5
model = th.load("./yolov5-7.0", "custom", path=YOLOV5_WEIGHT_FILE_PATH, source="local")

img = Image.open('./assets/real_people_car.jpg')

for x in range(
        0, 1600, 260
    ):  # (0，360；260，620；520，880；780，1040，1400；1300，1660；1560，1920；)
        for y in range(0, 960, 240):
            detect_img = img.crop((x, y, x + 360, y + 360))  # 360 * 360

            result = model(detect_img)

            tmp = result.pandas().xyxy[0]
            print(tmp)
            # for row in tmp.itertuples():
            #     xmax = int(getattr(row, 'xmax')) + x
            #     ymax = int(getattr(row, 'ymax')) + y
            #     xmin = int(getattr(row, 'xmin')) + x
            #     ymin = int(getattr(row, 'ymin')) + y
                
            #     class_num = int(getattr(row, 'name')[-1])
            #     name = class_types[class_num]
            #     print(name)
            #     print(getattr(row, 'confidence'))
            #     print((xmin, ymin, xmax, ymax))
            #     ImageDraw.Draw(img).rectangle((xmin, ymin, xmax, ymax), fill=None, outline=(255,0,0), width=3)

img.save('./tensorrt_inference.jpg')
                
                
                
            