import cv2
from output.display_adapter import DisplayAdapter


class ImageFileAdapter(DisplayAdapter):
    """Saves design to an image file, can be used for debugging"""

    def __init__(self, file_path="", *, width: int = 384, height: int = 640):
        super(ImageFileAdapter, self).__init__(width=width, height=height)
        self.file_path = file_path
        if self.file_path == "":
            raise ValueError("File path must be specified")

    def render(self, frame_image):
        cv2.imwrite(self.file_path, frame_image)

    def calibrate(self):
        pass
