from DesignEntity import DesignEntity
from TextDesign import TextDesign
from Assets import colors

font_size = 20


class TechnicalDataDesign(DesignEntity):
    '''Prints data about the current loop ontop of the panel'''

    def __init__(self, size, start, stop):
        super(TechnicalDataDesign, self).__init__(size, mask=True)
        self.start = start
        self.stop = stop

    def __finish_image__(self):
        data = self.__get_data__()

        txt = TextDesign(self.size, text=data, fontsize=font_size)
        txt.color = colors["fg"]
        txt.pos = (0, 0)
        self.draw_design(txt)

        txt = TextDesign(self.size, text=data, fontsize=font_size)
        txt.color = colors["hl"]
        txt.pos = (1, 1)
        self.draw_design(txt)

        txt = TextDesign(self.size, text=data, fontsize=font_size)
        txt.color = colors["fg"]
        txt.pos = (2, 2)
        self.draw_design(txt)

    def __get_data__(self):
        data = "START: "
        data += str(self.start)
        data += "\nDURATION BEFORE RENDER: "
        dur = self.stop - self.start
        data += str(dur)
        data += "\nSTOP: "
        data += str(self.stop)
        return data
