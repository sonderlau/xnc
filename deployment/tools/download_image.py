"""
用于从网络上或者待识别的图片
下载并检测
"""
import requests
from PIL import Image

TEMP_IMAGE_FILE = '/assets/tmp.jpg'

print("download successful")

def get_url_image(url: str, root_path: str):
    
    # 查看是否存在
    f = open(root_path + TEMP_IMAGE_FILE,'wb')
    
    # TODO: verify 是否开启
    response = requests.get(url, verify=False)
    
    if response.status_code == 404:
        # 图片不存在
        return None
    
    f.write(response.content)
    f.close()
    
    return Image.open(root_path + TEMP_IMAGE_FILE)