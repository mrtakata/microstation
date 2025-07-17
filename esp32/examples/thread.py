import _thread
import time
from machine import Pin, ADC
from dht import DHT11


DEFAULT_DHT_PIN = 5
class TemperatureHumiditySensor:
  def __init__(self, pin=DEFAULT_DHT_PIN):
    self.sensor = DHT11(Pin(pin))

  def read(self):
    measurements = None
    try:
      self.sensor.measure()
      measurements = {
        "temp": self.sensor.temperature(),
        "humidity": self.sensor.humidity()
      }
    except OSError as e:
      print('Sensor Reading Failed')
    return measurements
  

# Shared variable
shared_sensor_value = 0

# Lock for synchronizing access
lock = _thread.allocate_lock()

led = Pin(2, Pin.OUT)
sensor = TemperatureHumiditySensor()

# Sensor monitoring task
def monitor_sensor():
    global shared_sensor_value
    while True:
        reads = sensor.read()
        with lock:  # Lock during write
            shared_sensor_value = reads['humidity'] if reads else 0
        time.sleep(1)

# LED task reads the shared variable
def blink_led():
    global shared_sensor_value
    while True:
        led.value(not led.value())
        with lock:  # Lock during read
            print("Shared sensor value:", shared_sensor_value)
        time.sleep(0.5)

# Start sensor thread
_thread.start_new_thread(monitor_sensor, ())

# Run LED task in main thread
blink_led()
