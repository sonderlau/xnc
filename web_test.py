
from pathlib import Path

import streamlit as st
import time
import torch
import os
from PIL import Image

model = torch.hub.load(".", "custom", path="./best.pt", source="local")

img_source_list = ("本地", "测试")

# ! 检测图片地址
detect_file_path = ""


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

    st.title("环卫工人检测 Demo")

    # ! define yolov5 model

    # ! model configs
    # ? 开启图片增强用于推理
    images_augmentation = st.sidebar.checkbox(
        "开启图片增强 (Image Augmentation)",
        value=False,
        help="启用 Test Time Augmentation 增强数据识别结果",
    )

    if images_augmentation:
        model.augment = True

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
        selected_img = st.sidebar.selectbox("选择测试图片", ["", 1, 2, 3, 4, 5], index=0)
        if selected_img != "":
            print("选择了", selected_img)
            detect_file_path = f"data/images/test_images/{selected_img}.jpg"
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
                result = model(Image.open(detect_file_path), size=640)
                result.save()

                time.sleep(0.5)

                for img in os.listdir(get_detection_folder()):
                    st.image(str(Path(f"{get_detection_folder()}") / img))
