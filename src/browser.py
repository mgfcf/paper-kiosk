from io import BytesIO
import time
from selenium import webdriver
import cv2
from config import *
import logging
import numpy


class BrowserRenderer:
    """Renders a browser window with a given URL."""

    def __init__(self, url, *, width=800, height=600):
        self.url = url
        self.browser = None
        self.width = width
        self.height = height
        self.offset_width = 0  # Account for browser borders
        self.offset_height = 0  # Account for browser borders
        self.upscale_factor = 1  # Some sizes may be too small for the browser to render, so we render the image at a higher scale and have to downscale it afterwards

        self._calibrate()

    def _get_screenshot(self) -> numpy.ndarray:
        self._apply_size()
        self.browser.get(self.url)
        time.sleep(config[PAGE_LOAD_DELAY])
        screenshot_binary = self.browser.get_screenshot_as_png()
        screenshot_image = cv2.imdecode(
            numpy.frombuffer(screenshot_binary, numpy.uint8), cv2.IMREAD_UNCHANGED
        )

        # Downscale screenshot if needed
        if self.upscale_factor > 1:
            screenshot_image = cv2.resize(
                screenshot_image,
                (int(screenshot_image.shape[1] / self.upscale_factor),
                 int(screenshot_image.shape[0] / self.upscale_factor)),
                interpolation=cv2.INTER_AREA,
            )

        return screenshot_image

    def _apply_size(self):
        self.browser.set_window_size(int(self.width * self.upscale_factor) + self.offset_width,
                                     int(self.height * self.upscale_factor) + self.offset_height)

    def render(self):
        try:
            self.browser = webdriver.Firefox()
            return self._get_screenshot()
        finally:
            self.browser.quit()

    def _calibrate(self):
        # Open browser, adjust size, load URL, wait for page to load and take a screenshot
        self.browser = webdriver.Firefox()

        try:
            # Initial calibration screenshot
            image = self._get_screenshot()

            # Adjust upscale factor if needed
            factors = [numpy.ceil(image.shape[0] / self.height), numpy.ceil(image.shape[1] / self.width)]
            biggest_factor = max(factors)
            if biggest_factor > 1:
                self.upscale_factor = biggest_factor
                logging.info("Upscaling factor set to " + str(self.upscale_factor))

            # Make sure screenshot has desired size. Browser borders can cause the screenshot to be smaller than the desired size.
            if image.shape[0] < self.height or image.shape[1] < self.width:
                self.offset_width = self.width - image.shape[1]
                self.offset_height = self.height - image.shape[0]
        finally:
            self.browser.quit()
