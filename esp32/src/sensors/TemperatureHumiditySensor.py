from machine import Pin
from dht import DHT11


class TemperatureHumiditySensor:
  def __init__(self, pin):
    self.sensor = DHT11(Pin(pin))

  def read(self):
    measurements = None
    try:
      self.sensor.measure()
      measurements = {
        "temp": self.sensor.temperature(),
        "humidity": self.sensor.humidity()
      }
      temperature = self.sensor.temperature()
      humidity = self.sensor.humidity()
    except OSError as e:
      print('Sensor Reading Failed')
    return measurements

