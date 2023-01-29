from tools.Enums import (
    REGEX_URL,
    DOMAIN_WHITELIST,
    ErrorMessages,
    FILE_ACCEPTED_TYPES_LIST,
)
from tools.download_image import get_url_image, TEMP_IMAGE_FILE
import re
import os




# 判断是否为 URL 地址


def validate_image(path: str, root_path: str):
    """验证图片地址

    Args:
        path (str): 图片地址(URL / path)

    Raises:
        Exception: 发生的错误情况

    Returns:
        str: 本地缓存的地址
    """
    # * 网络地址

    if re.search(REGEX_URL, path):
        
        print("URL 地址", path)

        # 校验白名单
        is_white_domain = False
        for white_domain in DOMAIN_WHITELIST:
            if path.find(white_domain) != -1:
                is_white_domain = True
                break
        if not is_white_domain:
            
            raise Exception(ErrorMessages.URL_NOT_IN_WHITELIST)
            
        # 下载图片

        image_in = get_url_image(path, root_path)

        if image_in == None:
            # 404 not found

            raise Exception(ErrorMessages.URL_ASSET_NOT_FOUND)

        img_path = os.getcwd() + TEMP_IMAGE_FILE
        
        return img_path

    # * 本地文件 (当前目录下)
    else:

        # 文件地址为空
        if not path:
            raise Exception(ErrorMessages.FILE_PATH_EMPTY)

        # 去除路径开头 /
        if path[0] == "/":
            path = path[1:]

        file_full_path = os.path.join(root_path, path)

        # 地址为空 或 不合法
        if not os.path.exists(file_full_path):
            raise Exception(file_full_path)

        # 文件类型不支持
        if not os.path.splitext(file_full_path)[-1] in FILE_ACCEPTED_TYPES_LIST:
            raise Exception(
                ErrorMessages.FILE_TYPE_NOT_CORRECT + ErrorMessages.FILE_ACCEPTED_TYPES
            )

        return file_full_path
