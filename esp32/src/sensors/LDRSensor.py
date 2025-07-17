from machine import Pin, ADC


class LDRSensor:
  def __init__(self, pin):
    self.photosensor = Pin(pin)
    self.adc = ADC(self.photosensor)
    self.adc.atten(ADC.ATTN_11DB)  # Set attenuation for full range

  def read_light(self):
    raw_value = self.adc.read_u16()
    value = 100 - round((raw_value / 65535) * 100, 2)  # Scale to percentage
    return value
  
