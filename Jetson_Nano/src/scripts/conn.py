from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time
import os

username = "199050418"  # 修改为自己
password = "max1ndex"  # 修改为自己


now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# result = os.system('ping www.baidu.com -c 2')
result = True
if result:
    print(now_time + " ping fail")
    try:
        opt = webdriver.FirefoxOptions()
        opt.add_argument("--headless")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--no-sandbox")  # root用户不加这条会无法运行,同时访问一些不安全的网站时，容易受到威胁
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("blink-settings=imagesEnabled=false")
        driver = webdriver.Firefox(
            options=opt
        )

        driver.get("http://10.8.8.8/srun_portal_pc?ac_id=1")
        driver.find_element_by_xpath(
            '//*[@id="login-form"]/div[1]/div/input'
        ).send_keys(username)
        driver.find_element_by_xpath(
            '//*[@id="login-form"]/div[2]/div/input'
        ).send_keys(password)
        driver.find_element_by_xpath(
            '//*[@id="login-form"]/div[3]/div[1]/button'
        ).click()
        time.sleep(5)
        driver.quit()
        print(now_time + " login success")
    except Exception as e:
        print(e)
        print(now_time + " login error")
else:
    print(now_time + " ping success")
