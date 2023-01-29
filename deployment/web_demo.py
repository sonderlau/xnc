
from pathlib import Path

import streamlit as st
import time
import os
import requests
import requests
from PIL import Image, ImageDraw, ImageFont

img_source_list = ("本地", "测试")

# ! 检测图片地址
detect_file_path = ""

detection_colors = {
    "cleaner": "#F15412",
    "trash": "#1F4690",
    "car": "#1F4690",
    "trash_can_covered": "#5FD068",
    "trash_can_overfull": "#D61C4E",
    "trash_can_uncovered": "#FEF9A7",
    "people": "#F2D1D1",
    "traffic police": "red",
    "waitor": "red",
    "flight_attendant": "red"
}



def get_all_test_images():
    r = os.listdir('data/images/test_images/')
    r.insert(0, "")
    return r

def get_subdirs(b="."):
    """
    Returns all sub-directories in a specific Path
    """
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd):
            result.append(bd)
    return result


def user_select_preset_images(index, parameters):
    print(index, parameters)


def get_detection_folder():
    """
    Returns the latest folder in a runs\detect
    """
    return max(get_subdirs(os.path.join("runs", "detect")), key=os.path.getmtime)


if __name__ == "__main__":
    
    is_valid = False

    st.title("在线检测Demo")


    img_source = st.sidebar.radio("图片来源", img_source_list, index=0)
    
    if img_source == img_source_list[0]:
        # * 上传图片
        uploaded_file = st.sidebar.file_uploader("上传图片", type=["png", "jpeg", "jpg"])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text="资源加载中..."):
                st.sidebar.image(uploaded_file)
                detect_file_path = f"data/images/{uploaded_file.name}"
                picture = Image.open(uploaded_file).save(detect_file_path)
        else:
            is_valid = False
    elif img_source == img_source_list[1]:
        # * 自选择图片
        selected_img = st.sidebar.selectbox("选择测试图片", get_all_test_images(), index=0)
        if selected_img != "":
            print("选择了", selected_img)
            detect_file_path = f"data/images/test_images/{selected_img}"
            is_valid = True
            st.sidebar.image(detect_file_path)
        else:
            is_valid = False
    else:
        print(img_source, img_source_list)
        st.error('选择出错')

    

    

    # * check validation
    if is_valid:
        if st.button("开始检测"):
            with st.spinner(text="处理中..."):
                print(detect_file_path)
                
                
                image = Image.open(detect_file_path)

                img_length, img_width = image.size
                
                frame_size = int(min(img_length, img_width) / 400)
                font_size = frame_size * 10
                
                arial = ImageFont.FreeTypeFont('./data/Arial.ttf', size=font_size)
                # 调用 get 接口 获取结果
                result = requests.get(f'http://192.168.1.33:8521/detect?path={detect_file_path}').json()

                for box in result['data']:
                    print(box['name'])
                    
                    detection_points = box['box']
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
                    draw.rectangle([x_0, y_0, x_1, y_1], fill=None, outline=detection_colors[box["name"]], width=frame_size)
                    draw.text([x_0, y_0 - 5], box["name"], font=arial, anchor='lb', fill=detection_colors[box["name"]])
                image.save('./result.jpg')
                print(result)
                
                # time.sleep(0.5)

                st.image(image)
                
                # 画出图片

