import time
import RPi.GPIO as GPIO


class OnkyoRI:
    def __init__(self, pin: int):
        self.output_pin = pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.output_pin, GPIO.OUT)
        GPIO.output(self.output_pin, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()

    def send(self, command):
        self.write_header()

        for i in range(12):
            level = (command & 0x800) != 0
            command <<= 1
            self.write_bit(level)

        self.write_footer()

    def write_header(self):
        GPIO.output(self.output_pin, GPIO.HIGH)
        self.delay_microseconds(3000)
        GPIO.output(self.output_pin, GPIO.LOW)
        self.delay_microseconds(1000)

    def write_bit(self, level):
        GPIO.output(self.output_pin, GPIO.HIGH)
        self.delay_microseconds(1000)
        GPIO.output(self.output_pin, GPIO.LOW)

        if level:
            self.delay_microseconds(2000)
        else:
            self.delay_microseconds(1000)

    def write_footer(self):
        GPIO.output(self.output_pin, GPIO.HIGH)
        self.delay_microseconds(1000)
        GPIO.output(self.output_pin, GPIO.LOW)
        time.sleep(0.02)

    @staticmethod
    def delay_microseconds(microseconds):
        seconds = microseconds / 1000000.0
        time.sleep(seconds)


if __name__ == "__main__":
    conn = OnkyoRI(pin=8)
    conn.send(0x4)
