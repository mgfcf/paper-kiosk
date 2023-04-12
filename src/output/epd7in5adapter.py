from output.epd_adapter import EpdAdapter, DISPLAY_REFRESH, DATA_START_TRANSMISSION_1
from PIL import Image, ImageDraw


class Epd7in5Adapter(EpdAdapter):
    def display_frame(self, frame_buffer):
        self.send_command(DATA_START_TRANSMISSION_1)
        for i in range(0, 30720):
            temp1 = frame_buffer[i]
            j = 0
            while (j < 8):
                if (temp1 & 0x80):
                    temp2 = 0x03
                else:
                    temp2 = 0x00
                temp2 = (temp2 << 4) & 0xFF
                temp1 = (temp1 << 1) & 0xFF
                j += 1
                if (temp1 & 0x80):
                    temp2 |= 0x03
                else:
                    temp2 |= 0x00
                temp1 = (temp1 << 1) & 0xFF
                self.send_data(temp2)
                j += 1
        self.send_command(DISPLAY_REFRESH)
        self.delay_ms(100)
        self.wait_until_idle()

    def get_frame_buffer(self, image):
        buf = [0x00] * int(self.height * self.width / 8)
        # Set buffer to value of Python Imaging Library image.
        # Image must be in mode 1.
        image_monocolor = image.convert('L')  # with ot withour dithering?
        imwidth, imheight = image_monocolor.size
        if imwidth != self.height or imheight != self.width:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).'.format(self.height, self.width))

        pixels = image_monocolor.load()
        for y in range(self.width):
            for x in range(self.height):
                # Set the bits for the column of pixels at the current position.
                if pixels[x, y] >= 240:  # White
                    buf[int((x + y * self.height) / 8)] |= 0x80 >> (x % 8)
        return buf

    def calibrate(self):
        for _ in range(2):
            self.init_render()
            black = Image.new('1', (self.height, self.width), 'black')
            print('calibrating black...')
            ImageDraw.Draw(black)
            self.display_frame(self.get_frame_buffer(black))

            white = Image.new('1', (self.height, self.width), 'white')
            ImageDraw.Draw(white)
            print('calibrating white...')
            self.display_frame(self.get_frame_buffer(white))
            self.sleep()
        print('Calibration complete')
