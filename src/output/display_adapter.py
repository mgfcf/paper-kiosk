class DisplayAdapter(object):
    """Interface for CalendarDesign output channels."""

    def __init__(self, *, width: int = 384, height: int = 640):
        self.width = width
        self.height = height

    def render(self, frame_image):
        raise NotImplementedError("Functions needs to be implemented")

    def calibrate(self):
        raise NotImplementedError("Functions needs to be implemented")
