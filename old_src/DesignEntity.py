from PIL import Image, ImageOps, ImageDraw
from Assets import colors

masking_threshold = 200


class DesignEntity (object):
    """General entity that can be drawn on to a panel design or
    other design entities."""

    def __init__(self, size, mask=False, invert_mask=False, color_key=False):
        self.size = size
        # Are dimensions >= 0?
        if self.size[0] < 0:
            self.size = (0, self.size[1])
        if self.size[1] < 0:
            self.size = (self.size[0], 0)
        
        self.pos = (0, 0)
        self.mask = mask
        self.invert_mask = invert_mask
        self.__init_image__()
        self.__finished_image__ = False
        self.color_key = color_key

    def __init_image__(self, color=colors["bg"]):
        rounded_size = (int(self.size[0]), int(self.size[1]))
        self.__image__ = Image.new('RGBA', rounded_size, color=color)

    def get_image(self):
        if self.__finished_image__ is False:
            self.__finish_image__()
            self.__finished_image__ = True
        return self.__image__

    def draw(self, subimage, pos, mask=False, invert_mask=False, color_key=False):
        rounded_pos = (int(pos[0]), int(pos[1]))
        img_mask = None
        if mask:
            img_mask = self.__get_mask__(
                subimage, invert_mask=invert_mask, color_key=color_key)
        self.__image__.paste(subimage, rounded_pos, mask=img_mask)

    def draw_design(self, entity):
        self.draw(entity.get_image(), entity.pos, entity.mask,
                  entity.invert_mask, entity.color_key)

    def draw_image(self, path, pos):
        self.draw(Image.open(path), pos)

    def __finish_image__(self):
        pass

    def __get_mask__(self, image, invert_mask, color_key):
        mask = image.convert('L')
        if color_key:
            mask = mask.point(lambda p: 0 if p <
                              masking_threshold else 255, '1').convert('L')
        if invert_mask:
            mask = ImageOps.invert(mask)
        return ImageOps.invert(mask)
