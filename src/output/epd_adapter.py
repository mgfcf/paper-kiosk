from output.display_adapter import DisplayAdapter
import spidev
import RPi.GPIO as GPIO
import time

RST_PIN = 17
DC_PIN = 25
CS_PIN = 8
BUSY_PIN = 24

# Commands
PANEL_SETTING = 0x00
POWER_SETTING = 0x01
POWER_OFF = 0x02
POWER_OFF_SEQUENCE_SETTING = 0x03
POWER_ON = 0x04
POWER_ON_MEASURE = 0x05
BOOSTER_SOFT_START = 0x06
DEEP_SLEEP = 0x07
DATA_START_TRANSMISSION_1 = 0x10
DATA_STOP = 0x11
DISPLAY_REFRESH = 0x12
IMAGE_PROCESS = 0x13
LUT_FOR_VCOM = 0x20
LUT_BLUE = 0x21
LUT_WHITE = 0x22
LUT_GRAY_1 = 0x23
LUT_GRAY_2 = 0x24
LUT_RED_0 = 0x25
LUT_RED_1 = 0x26
LUT_RED_2 = 0x27
LUT_RED_3 = 0x28
LUT_XON = 0x29
PLL_CONTROL = 0x30
TEMPERATURE_SENSOR_COMMAND = 0x40
TEMPERATURE_CALIBRATION = 0x41
TEMPERATURE_SENSOR_WRITE = 0x42
TEMPERATURE_SENSOR_READ = 0x43
VCOM_AND_DATA_INTERVAL_SETTING = 0x50
LOW_POWER_DETECTION = 0x51
TCON_SETTING = 0x60
TCON_RESOLUTION = 0x61
SPI_FLASH_CONTROL = 0x65
REVISION = 0x70
GET_STATUS = 0x71
AUTO_MEASUREMENT_VCOM = 0x80
READ_VCOM_VALUE = 0x81
VCM_DC_SETTING = 0x82


class EpdAdapter (DisplayAdapter):
    """Generalized adapter for epd7in5 and epd7in5b"""

    def __init__(self, width, height):
        super(EpdAdapter, self).__init__(width, height)

        self.reset_pin = RST_PIN
        self.dc_pin = DC_PIN
        self.busy_pin = BUSY_PIN

        self.epd_init()

    def display_frame(self, frame_buffer):
        raise NotImplementedError("Functions needs to be implemented")

    def get_frame_buffer(self, image):
        raise NotImplementedError("Functions needs to be implemented")

    def render(self, design):
        self.init_render()
        time.sleep(5)

        print('Converting image to data and sending it to the display')
        print('This may take a while...' + '\n')
        prepared_image = design.get_image().rotate(270, expand=1).convert("RGB")
        self.display_frame(self.get_frame_buffer(prepared_image))

        # Powering off the E-Paper until the next loop
        self.sleep()
        print('Data sent successfully')
        print('Powering off the E-Paper until the next loop' + '\n')

    def init_render(self):
        if (self.epd_init() != 0):
            return -1
        self.reset()

        self.send_command(POWER_SETTING)
        self.send_data(0x37)
        self.send_data(0x00)

        self.send_command(PANEL_SETTING)
        self.send_data(0xCF)
        self.send_data(0x08)

        self.send_command(BOOSTER_SOFT_START)
        self.send_data(0xc7)
        self.send_data(0xcc)
        self.send_data(0x28)

        self.send_command(POWER_ON)
        self.wait_until_idle()

        self.send_command(PLL_CONTROL)
        self.send_data(0x3c)

        self.send_command(TEMPERATURE_CALIBRATION)
        self.send_data(0x00)

        self.send_command(VCOM_AND_DATA_INTERVAL_SETTING)
        self.send_data(0x77)

        self.send_command(TCON_SETTING)
        self.send_data(0x22)

        self.send_command(TCON_RESOLUTION)
        self.send_data(0x02)  # source 640
        self.send_data(0x80)
        self.send_data(0x01)  # gate 384
        self.send_data(0x80)

        self.send_command(VCM_DC_SETTING)
        self.send_data(0x1E)  # decide by LUT file

        self.send_command(0xe5)  # FLASH MODE
        self.send_data(0x03)

    def digital_write(self, pin, value):
        GPIO.output(pin, value)

    def digital_read(self, pin):
        return GPIO.input(pin)

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_transfer(self, data):
        self.SPI.writebytes(data)

    def epd_init(self):
        # SPI device, bus = 0, device = 0
        self.SPI = spidev.SpiDev(0, 0)
        #self.SPI.no_cs = True

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(RST_PIN, GPIO.OUT)
        GPIO.setup(DC_PIN, GPIO.OUT)
        GPIO.setup(CS_PIN, GPIO.OUT)
        GPIO.setup(BUSY_PIN, GPIO.IN)
        self.SPI.max_speed_hz = 2000000
        self.SPI.mode = 0b00
        return 0

    def sleep(self):
        self.send_command(POWER_OFF)
        self.wait_until_idle()
        self.send_command(DEEP_SLEEP)
        self.send_data(0xa5)

    def wait_until_idle(self, max_wait_seconds=60):
        wait_ms = 100
        count = 0
        while(self.digital_read(self.busy_pin) == 0 and wait_ms * count < max_wait_seconds * 1000):      # 0: busy, 1: idle
            self.delay_ms(wait_ms)
            count += 1
        if wait_ms * count >= max_wait_seconds * 1000:
            print("Skipped idle confirmation")

    def reset(self):
        self.digital_write(self.reset_pin, GPIO.LOW)         # module reset
        self.delay_ms(200)
        self.digital_write(self.reset_pin, GPIO.HIGH)
        self.delay_ms(200)

    def send_command(self, command):
        self.digital_write(self.dc_pin, GPIO.LOW)
        # the parameter type is list but not int
        # so use [command] instead of command
        self.spi_transfer([command])

    def send_data(self, data):
        self.digital_write(self.dc_pin, GPIO.HIGH)
        # the parameter type is list but not int
        # so use [data] instead of data
        self.spi_transfer([data])
