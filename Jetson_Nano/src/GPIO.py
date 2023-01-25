import time
import Jetson.GPIO as GPIO

# 蜂鸣器 

# 33 5V GDN

whizz_io = 33

GPIO.setmode(GPIO.BOARD)

GPIO.setup(whizz_io, GPIO.OUT)

GPIO.output(whizz_io, GPIO.HIGH)

time.sleep(1)

GPIO.cleanup(whizz_io)
