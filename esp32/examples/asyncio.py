import uasyncio as asyncio
from machine import Pin
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
      temperature = self.sensor.temperature()
      humidity = self.sensor.humidity()
    except OSError as e:
      print('Sensor Reading Failed')
    return measurements
  

led = Pin(2, Pin.OUT)
sensor = TemperatureHumiditySensor()

async def blink_led():
    while True:
        led.value(not led.value())
        await asyncio.sleep(0.5)


async def monitor_sensor():
    while True:
        readings = sensor.read()
        if readings is not None:
            print(f"Temperature: {readings['temp']}°C, Humidity: {readings['humidity']}%")
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(
        blink_led(),
        monitor_sensor()
    )

asyncio.run(main())