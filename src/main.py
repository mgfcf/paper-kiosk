from time import sleep
from browser import BrowserRenderer
from looper import Looper
from config import *
import logging

logging.getLogger().setLevel(logging.DEBUG)

output_adapters = []

print(config[FILE_RENDER] is True)
if config[FILE_RENDER]:
    from output.image_file_adapter import ImageFileAdapter

    epd = ImageFileAdapter(config[FILE_PATH], width=config[DISPLAY_WIDTH], height=config[DISPLAY_HEIGHT])
    output_adapters.append(epd)

if config[DISPLAY_RENDER]:
    if config[DISPLAY_COLORS] == "bwr":
        from output.epd7in5badapter import Epd7in5bAdapter

        output_adapters.append(Epd7in5bAdapter(width=config[DISPLAY_WIDTH], height=config[DISPLAY_HEIGHT]))
    elif config[DISPLAY_COLORS] == "bw":
        from output.epd7in5adapter import Epd7in5Adapter

        output_adapters.append(Epd7in5Adapter(width=config[DISPLAY_WIDTH], height=config[DISPLAY_HEIGHT]))

loop_timer = Looper(config[UPDATE_DELAY], run_on_hour=config[RUN_ON_HOUR])


def main():
    """Main loop starts from here"""
    while True:
        loop_timer.begin_loop()

        # TODO: Calibrate outputs
        # if start_time.hour in calibrate_hours and loop_timer.is_new_hour_loop():
        #     logging.info("Calibrating outputs")
        #     for output in output_adapters:
        #         output.calibrate()

        logging.info("Starting to render web page")

        browser = BrowserRenderer(config[URL], height=config[DISPLAY_HEIGHT], width=config[DISPLAY_WIDTH])
        frame_image = browser.render()

        logging.info("Starting to output")
        for i, output in enumerate(output_adapters):
            try:
                output.render(frame_image)
                logging.info(
                    str(i + 1) + " of " + str(len(output_adapters)) + " rendered"
                )
            except BaseException as ex:
                logging.error(
                    str(ex)
                    + " | Failed to render output "
                    + str(i + 1)
                    + " of "
                    + str(len(output_adapters)),
                )

        logging.info("=> Finished loop" + "\n")

        loop_timer.end_loop()

        if loop_timer.was_last_loop():
            logging.info(
                "Maximum loop count "
                + str(loop_timer.loop_count)
                + " reached, exiting."
            )
            return

        sleep_time = loop_timer.time_until_next()
        logging.info(
            "This loop took " + str(loop_timer.get_last_duration()) + " to execute."
        )
        logging.info("Sleeping " + str(sleep_time) + " until next loop.")
        sleep(sleep_time.total_seconds())


if __name__ == "__main__":
    main()
