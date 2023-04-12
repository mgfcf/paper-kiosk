from Assets import path, defaultfont
from PIL import ImageFont


def wrap_text_with_font(text, width, font):
    words = text.split(' ')
    result = ""
    for word in words:
        until_current = (result + " " + word).strip()
        txt_width, _ = font.getsize_multiline(until_current)
        if txt_width > width:
            result += '\n'
        else:
            result += ' '
        result += word
    return result.strip()


def wrap_text(text, width, font_size, font_family=defaultfont):
    return wrap_text_with_font(text, width, ImageFont.truetype(path + font_family, int(font_size)))
