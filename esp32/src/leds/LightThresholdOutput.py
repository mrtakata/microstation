from machine import Pin

LIGHT_OFF = 0
LIGHT_ON = 1


class LightThresholdOutput:
  def __init__(self, pin=2, initial_state=LIGHT_OFF, threshold=40):
    self.led = Pin(pin, Pin.OUT)
    self.state = initial_state
    self.threshold = threshold

  def set_state_based_on_threshold(self, value):
    if value < self.threshold:
      self.state = LIGHT_ON
    else:
      self.state = LIGHT_OFF
    self.led.value(self.state)
  
