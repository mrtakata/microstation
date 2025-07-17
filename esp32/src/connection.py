
from machine import Pin
import time
import network


ssid = 
password = 
def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.WLAN.IF_STA)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    return sta_if.isconnected()

connect_wifi(ssid, password)
led = Pin(2, Pin.OUT)


while True:
    led.value(not led.value())
    print(led.value())
    time.sleep(1)