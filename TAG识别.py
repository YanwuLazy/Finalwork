import sensor, image, time , pyb
from pyb import UART
import ustruct
thresholds = [(0, 57, -64, 57, -128, 44) ]# black
sensor.reset() #初始化设置
sensor.set_pixformat(sensor.RGB565) #设置为彩色
sensor.set_framesize(sensor.QQVGA) #设置清晰度
sensor.set_windowing(150,200)
sensor.skip_frames(time = 2000) #跳过前2000ms的图像
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock() #创建一个clock便于计算FPS
sensor.set_auto_gain(False) # 关闭自动自动增益。默认开启
sensor.set_auto_whitebal(False) #关闭白平衡。
uart = UART(3, 115200)
uart.init(115200)
def send_data_packet(x):
    temp = bytearray([x,0x0d,0x0a])
    uart.write(temp)                           #串口发送
Messages = [1,2,3]

while(True):
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(): # 默认为TAG36H11。
        img.draw_rectangle(tag.rect(), color = (255, 0, 0)) # 在识别到的AprilTag 上面画框和十字
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        #print(tag.id()) # 打印 AprilTag 的 ID
        message = tag.id()
        for Message in Messages:
                if Message == message:
                    result = Message
                    send_data_packet(result)
                    print(f"发送成功，发送数据为{result}")
                    time.sleep_ms(1000) #每秒读取一次
