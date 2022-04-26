import random
import time
import  sys
from  Adafruit_IO import  MQTTClient

AIO_FEED_ID = "bbc_pump"
AIO_USERNAME = "luongduy2001"
AIO_KEY = ""

def  connected(client):
    print("Ket noi thanh cong...")
    client.subscribe(AIO_FEED_ID)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong...")

def  disconnected(client):
    print("Ngat ket noi...")
    sys.exit (1)

def  message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
def post(n):
    #ở đây các bạn thay value bằng giá trị trả về của hàm nhận diện khuôn mặt
    #nếu người quen thì cho value = 2 và nếu người lạ cho value = 3.
    client.publish("bbc-pump", n)
