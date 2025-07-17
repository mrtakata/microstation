from machine import Pin, ADC


class SoundSensor:
  def __init__(self, pin):
    self.mic = ADC(Pin(pin))  # Must be ADC1 pin
    self.mic.atten(ADC.ATTN_11DB)  # Full range (0–3.3V)

  def read(self):
    sound_level = self.mic.read()  # 0–4095
    return sound_level