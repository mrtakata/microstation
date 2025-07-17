import time
from machine import Pin,PWM

FULL_BRIGHTNESS = 65535  # Maximum duty cycle for 16-bit PWM
DEFAULT_FREQUENCY = 1000  # Default frequency for PWM

class RGBLED:
    def __init__(self, red_pin=25, green_pin=26, blue_pin=27):
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
        time.sleep(0.1)

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
            time.sleep(0.001)

        # Gradually decrease brightness
        for duty_value in range(FULL_BRIGHTNESS, 0, -step):
            self.pwms[color].duty_u16(duty_value)
            time.sleep(0.001)

# main function
def main():
    rgb_led = RGBLED()
    colors = ['red', 'green', 'blue']
    while True:
        rgb_led.blink_color_gradually('red')
            
if __name__ == "__main__":
    main()