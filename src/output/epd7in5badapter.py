from output.epd_adapter import EpdAdapter, DISPLAY_REFRESH, DATA_START_TRANSMISSION_1
from PIL import Image, ImageDraw
import numpy as np


class Epd7in5bAdapter(EpdAdapter):
    def display_frame(self, frame_buffer):
        self.send_command(DATA_START_TRANSMISSION_1)
        for i in range(0, int(self.height / 4 * self.width)):
            # the above line had to be modified due to python2 -> python3
            # the issue lies in division, which returns integers in python2
            # but floats in python3
            temp1 = frame_buffer[i]
            j = 0
            while (j < 4):
                if ((temp1 & 0xC0) == 0xC0):
                    temp2 = 0x03
                elif ((temp1 & 0xC0) == 0x00):
                    temp2 = 0x00
                else:
                    temp2 = 0x04
                temp2 = (temp2 << 4) & 0xFF
                temp1 = (temp1 << 2) & 0xFF
                j += 1
                if ((temp1 & 0xC0) == 0xC0):
                    temp2 |= 0x03
                elif ((temp1 & 0xC0) == 0x00):
                    temp2 |= 0x00
                else:
                    temp2 |= 0x04
                temp1 = (temp1 << 2) & 0xFF
                self.send_data(temp2)
                j += 1
        self.send_command(DISPLAY_REFRESH)
        self.delay_ms(100)
        self.wait_until_idle()

    def get_frame_buffer(self, image):
        buf = [0x00] * int(self.height * self.width / 4)
        imwidth, imheight = image.size
        if imwidth != self.height or imheight != self.width:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).'.format(self.height, self.width))

        image_buf = self.__prepare_image__(image)
        for x in range(self.width):
            for y in range(self.height):
                # Set the bits for the column of pixels at the current
                # position.
                if image_buf[x, y, 1] == 255:  # White
                    buf[int((y + x * self.height) / 4)] |= 0xC0 >> (y % 4 * 2)
                elif image_buf[x, y, 0] == 0:  # Black
                    buf[int((y + x * self.height) / 4)
                    ] &= ~(0xC0 >> (y % 4 * 2))
                else:  # Red
                    buf[int((y + x * self.height) / 4)
                    ] &= ~(0xC0 >> (y % 4 * 2))
                    buf[int((y + x * self.height) / 4)] |= 0x40 >> (y % 4 * 2)
        return buf

    def __prepare_image__(self, image):
        buffer = np.array(image)
        r, g = buffer[:, :, 0], buffer[:, :, 1]
        buffer[np.logical_and(r > 220, g > 220)] = [255, 255, 255]
        buffer[r > g] = [255, 0, 0]
        buffer[r != 255] = [0, 0, 0]
        return buffer

    def calibrate(self):
        for _ in range(2):
            self.init_render()
            black = Image.new('RGB', (self.height, self.width), 'black')
            print('calibrating black...')
            ImageDraw.Draw(black)
            self.display_frame(self.get_frame_buffer(black))

            red = Image.new('RGB', (self.height, self.width), 'red')
            ImageDraw.Draw(red)
            print('calibrating red...')
            self.display_frame(self.get_frame_buffer(red))

            white = Image.new('RGB', (self.height, self.width), 'white')
            ImageDraw.Draw(white)
            print('calibrating white...')
            self.display_frame(self.get_frame_buffer(white))
            self.sleep()
        print('Calibration complete')
