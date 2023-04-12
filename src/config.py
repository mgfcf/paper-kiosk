import json

DEFAULT_HEADER = "PaperKiosk"

URL = "url"
UPDATE_DELAY = "update_delay"   # minutes
RUN_ON_HOUR = "run_on_hour"
FILE_RENDER = "file_render"
DISPLAY_RENDER = "display_render"
DISPLAY_COLORS = "display_colors"   # bw, bwr
FILE_PATH = "file_path"
DISPLAY_HEIGHT = "display_height"
DISPLAY_WIDTH = "display_width"
PAGE_LOAD_DELAY = "page_load_delay"  # seconds


class ConfigReader:
    def __init__(self, config_file: str):
        with open(config_file, "r") as f:
            self.config = json.load(f)

    def __getitem__(self, item):
        return self.config[item]


config = ConfigReader("config.json")
