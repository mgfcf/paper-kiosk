from DesignEntity import DesignEntity
from Assets import path as application_path
from PIL import Image, ExifTags


class ImageDesign (DesignEntity):
    """Creates a TableDesign filled with rss post
    date and title"""

    # fill: "none" : original size, "stretch" : strech to fill, "scale" : scale to fill, "border" : scale until one side touches border
    def __init__(self, size, path, fill="none", color="RGBA", dither=None):
        super(ImageDesign, self).__init__(size)
        self.set_path(path)
        self.fill = fill
        self.color = color
        self.dither = dither

    def set_path(self, path):
        path = path.replace('\\', '/')
        if path[0] != '/' and ':' not in path[0:3]:
            path = application_path + '/' + path
        self.path = path

    def __finish_image__(self):
        img = Image.open(self.path)
        img = img.convert(self.color, dither=self.dither)

        img = self.__fix_orientation__(img)
        img = self.__resize_image__(img)
        pos = self.__get_centered_position__(img)

        self.__init_image__("#00000000")
        self.draw(img, pos)

    def __resize_image__(self, img):
        if self.fill is "none":
            return img

        if self.fill is "stretch":
            img = img.resize(self.size, resample=Image.LANCZOS)

        if self.fill is "scale":
            size = self.size
            img_proportions = img.width / img.height
            if img_proportions < size[0] / size[1]:
                size = (size[0], int(size[0] * (1 / img_proportions)))
            else:
                size = (int(size[1] * img_proportions), size[1])
            img = img.resize(size, resample=Image.LANCZOS)

        if self.fill is "border":
            size = self.size
            img_proportions = img.width / img.height
            if img_proportions < size[0] / size[1]:
                size = (int(size[1] * img_proportions), size[1])
            else:
                size = (size[0], int(size[0] * (1 / img_proportions)))
            img = img.resize(size, resample=Image.LANCZOS)

        return img

    def __get_centered_position__(self, img):
        screen_size = self.size
        img_size = img.size

        delta_size = [s - i for s, i in zip(screen_size, img_size)]
        delta_center_pos = [s / 2 for s in delta_size]

        return delta_center_pos

    def __fix_orientation__(self, img):
        if "parsed_exif" not in img.info.keys():
            return img

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = img.info["parsed_exif"]

        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
        return img
