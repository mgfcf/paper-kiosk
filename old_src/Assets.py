#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageFont
from settings import font_boldness, font_size
import os
im_open = Image.open

path = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
if path != "" and path[-1] != "/":
    path += "/"

wpath = path+'weather-icons/'
opath = path+'other/'
fpath = 'fonts/'

tempicon = im_open(opath+'temperature.jpeg')
humicon = im_open(opath+'humidity.jpeg')
no_response = im_open(opath+'cloud-no-response.jpeg')
sunriseicon = im_open(opath+'wi-sunrise.jpeg')
sunseticon = im_open(opath+'wi-sunset.jpeg')
windicon = im_open(opath+'wi-strong-wind.jpeg')

fonts = {
    "extralight": fpath + "Assistant-ExtraLight.otf",
    "light": fpath + "Assistant-Light.otf",
    "regular": fpath + "Assistant-Regular.otf",
    "semibold": fpath + "Assistant-SemiBold.otf",
    "bold": fpath + "Assistant-Bold.otf",
    "extrabold": fpath + "Assistant-ExtraBold.otf"
}

defaultfont = fonts[font_boldness]
defaultfontsize = int(font_size)

weathericons = {
    '01d': 'wi-day-sunny', '02d': 'wi-day-cloudy', '03d': 'wi-cloudy',
    '04d': 'wi-cloudy-windy', '09d': 'wi-showers', '10d': 'wi-rain',
    '11d': 'wi-thunderstorm', '13d': 'wi-snow', '50d': 'wi-fog',
    '01n': 'wi-night-clear', '02n': 'wi-night-cloudy',
    '03n': 'wi-night-cloudy', '04n': 'wi-night-cloudy',
    '09n': 'wi-night-showers', '10n': 'wi-night-rain',
    '11n': 'wi-night-thunderstorm', '13n': 'wi-night-snow',
    '50n': 'wi-night-alt-cloudy-windy'}

colors = {
    "hl": "red",
    "fg": "black",
    "bg": "white"
}

supported_img_formats = [
    "BMP",
    "DIB",
    "EPS",
    "GIF",
    "ICNS",
    "ICO",
    "IM",
    "JPG",
    "JPEG",
    "J2K",
    "J2P",
    "JPX",
    "MSP",
    "PCX",
    "PNG",
    "PPM",
    "SGI",
    "SPI",
    "TGA",
    "TIFF",
    "WEBP",
    "XBM",
    "BLP",
    "CUR",
    "DCX",
    "DDS",
    "FLI",
    "FLC",
    "FPX",
    "FTEX",
    "GBR",
    "GD",
    "IMT",
    "IPTC",
    "NAA",
    "MCIDAS",
    "MIC",
    "MPO",
    "PCD",
    "PIXAR",
    "PSD",
    "WAL",
    "XPM",
]
