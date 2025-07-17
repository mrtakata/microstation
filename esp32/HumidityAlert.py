from machine import Pin, PWM
from time import sleep
from dht import DHT11
import _thread
LIGHT_ON = 1
LIGHT_OFF = 0

DEFAULT_RED_PIN = 25
DEFAULT_GREEN_PIN = 26
DEFAULT_BLUE_PIN = 27
DEFAULT_DHT_PIN = 5
DEFAULT_FREQUENCY = 1000  # Default frequency for PWM
DEFAULT_READ_TIME = 5  # Default read time in seconds
LOW_HUMIDITY_THRESHOLD = 40  # Threshold for low humidity alert
HIGH_HUMIDITY_THRESHOLD = 65  # Threshold for high humidity alert
FULL_BRIGHTNESS = 65535  # Maximum duty cycle for 16-bit PWM
HALF_BRIGHTNESS = FULL_BRIGHTNESS // 2  # Half brightness for smoother transitions

DEFAULT_COLOR = 'green'  # Default color for the LED


class RGBLED:
    def __init__(self, red_pin=DEFAULT_RED_PIN, green_pin=DEFAULT_GREEN_PIN, blue_pin=DEFAULT_BLUE_PIN):
        self.pwms = {
            'red': PWM(Pin(red_pin)),
            'green': PWM(Pin(green_pin)),
            'blue': PWM(Pin(blue_pin))
        }
        for color, pwm in self.pwms.items():
            pwm.freq(DEFAULT_FREQUENCY)

    def set_color(self, red, green, blue):
        self.pwms['red'].duty_u16(red)
        self.pwms['green'].duty_u16(green)
        self.pwms['blue'].duty_u16(blue)

    def turn_off(self):
        self.set_color(0, 0, 0)
        sleep(0.1)

    # Deinitialize PWM on all pins
    def deinit_pwm_pins(self):
        self.pwms['red'].deinit()
        self.pwms['green'].deinit()
        self.pwms['blue'].deinit()
    
    def blink_color_gradually(self, color):
        if color not in self.pwms:
            raise ValueError("Invalid color. Choose from 'red', 'green', or 'blue'.")
        
        self.turn_off()  # Ensure all LEDs are off before starting  
        # Gradually increase brightness
        step = 256  # Adjust step size for smoother transition
        for duty_value in range(0, FULL_BRIGHTNESS, step):
            self.pwms[color].duty_u16(duty_value)
            sleep(0.001)

        # Gradually decrease brightness
        for duty_value in range(FULL_BRIGHTNESS, 0, -step):
            self.pwms[color].duty_u16(duty_value)
            sleep(0.001)


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


class HumidityAlert:
    led = RGBLED()
    sensor = TemperatureHumiditySensor()
    humidity_value = 0 # Global variable to store humidity value
    lock = _thread.allocate_lock()


    @staticmethod
    def get_blink_color():
      color = DEFAULT_COLOR
      with HumidityAlert.lock:
        if HumidityAlert.humidity_value < LOW_HUMIDITY_THRESHOLD:
          color = 'red'
        elif HumidityAlert.humidity_value >= HIGH_HUMIDITY_THRESHOLD:
          color = 'blue'
        else:
          color = 'green'
        print(f"Current humidity: {HumidityAlert.humidity_value}%, LED color: {color}")
      return color
    
    def blink_led(self):
        while True:
          sleep(DEFAULT_READ_TIME)  # Adjust sleep time as needed
          color = HumidityAlert.get_blink_color()
          should_blink = color == 'red' or color == 'blue'
          if should_blink:
            HumidityAlert.led.blink_color_gradually(color)
          

    def read_sensor(self):
      while True:
        reads = HumidityAlert.sensor.read()
        if reads is not None: 
          print(f'Temperature: {reads['temp']:3.1f}C  |  Humidity: {reads['humidity']:3.1f}%')
          with HumidityAlert.lock:
            HumidityAlert.humidity_value = reads['humidity']
        sleep(DEFAULT_READ_TIME)  # Adjust sleep time as needed


if __name__ == "__main__":
  app = HumidityAlert()
  HumidityAlert.led.turn_off()  # Ensure LEDs are off at start
  print("Starting Humidity Alert System...")
  print("Press Ctrl+C to exit.")

  try:
    _thread.start_new_thread(app.read_sensor, ())
    app.blink_led()
  except KeyboardInterrupt:
    print("Program interrupted. Cleaning up...")
    HumidityAlert.led.deinit_pwm_pins()
    print("Cleanup done. Exiting.")