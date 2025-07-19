from time import sleep
import _thread
from config import *
from lib.outputs.RGBLED import RGBLED
from lib.sensors.DHTSensor import DHTSensor
from lib.outputs.OLED import SSD1306_I2C


class MicroStation:
    led = RGBLED(DEFAULT_RED_PIN, DEFAULT_GREEN_PIN, DEFAULT_BLUE_PIN)
    sensor = DHTSensor(DEFAULT_DHT_PIN)
    screen = SSD1306_I2C(width=DEFAULT_OLED_WIDTH, height=DEFAULT_OLED_HEIGHT, scl_pin=DEFAULT_OLED_SCL_PIN, sda_pin=DEFAULT_OLED_SDA_PIN)
    humidity_value = 0 # Global variable to store humidity value
    lock = _thread.allocate_lock()


    @staticmethod
    def get_blink_color():
      color = DEFAULT_COLOR
      with MicroStation.lock:
        if MicroStation.humidity_value < LOW_HUMIDITY_THRESHOLD:
          color = 'red'
        elif MicroStation.humidity_value >= HIGH_HUMIDITY_THRESHOLD:
          color = 'blue'
        else:
          color = 'green'
      return color
    
    def blink_led(self):
        MicroStation.led.turn_off()  # Ensure LEDs are off at start
        sleep(1)
        while True:
          color = MicroStation.get_blink_color()
          should_blink = color == 'red' or color == 'blue'
          if should_blink:
            MicroStation.led.blink_color_gradually(color)
          else:
            MicroStation.led.turn_off()
          sleep(0.1)
          

    def read_sensor(self):
      while True:
        reads = MicroStation.sensor.read()
        if reads is not None: 
          print(f"Temperature: {reads['temp']:3.1f}C  |  Humidity: {reads['humidity']:3.1f}%")            
          MicroStation.screen.text(f"T: {reads['temp']:3.1f}C", 0, 0)      
          MicroStation.screen.text(f"H: {reads['humidity']:3.1f}%", 0, 20)   
          MicroStation.screen.show()
          with MicroStation.lock:
            MicroStation.humidity_value = reads['humidity']
        sleep(DEFAULT_READ_TIME)  # Adjust sleep time as needed


if __name__ == "__main__":
  app = MicroStation()
  print("Starting Humidity Alert System...")
  print("Press Ctrl+C to exit.")

  try:
    _thread.start_new_thread(app.read_sensor, ())
    app.blink_led()
  except KeyboardInterrupt:
    print("Program interrupted. Cleaning up...")
    MicroStation.led.deinit_pwm_pins()
    print("Cleanup done. Exiting.")


