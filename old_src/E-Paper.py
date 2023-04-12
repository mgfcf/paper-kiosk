#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
E-Paper Software (main script) for the 3-colour and 2-Colour E-Paper display
A full and detailed breakdown for this code can be found in the wiki.
If you have any questions, feel free to open an issue at Github.

Copyright by aceisace
"""
from datetime import datetime
from time import sleep
from Assets import path
from LoopTimer import LoopTimer
import locale
from DebugConsole import DebugConsole
from settings import datetime_encoding, language, render_to_display, render_to_file, display_colours, location, api_key, owm_paid_subscription, choosen_design, ical_urls, highlighted_ical_urls, rss_feeds, update_interval, calibrate_hours, crypto_coins, max_loop_count, run_on_hour
from MonthOvPanel import MonthOvPanel
from DayListPanel import DayListPanel
from DayViewPanel import DayViewPanel
from DayFocusListPanel import DayFocusListPanel
from MonthViewPanel import MonthViewPanel
from AgendaListPanel import AgendaListPanel
from ImageFramePanel import ImageFramePanel
import OwmForecasts
import IcalEvents
import RssParserPosts
import GeckoCrypto

all_locales = locale.locale_alias
if language.lower() not in all_locales.keys():
    raise Exception(
        "The locale for \"%s\" is currently not supported! If you need support, please open an issue on github." % language)
locale.setlocale(locale.LC_ALL, "%s.%s" % (
    all_locales[language.lower()].split('.')[0], datetime_encoding))

debug = DebugConsole()
output_adapters = []

if render_to_file:
    import ImageFileAdapter
    epd = ImageFileAdapter.ImageFileAdapter(path)
    output_adapters.append(epd)

if render_to_display:
    if display_colours == "bwr":
        import Epd7in5bAdapter
        epd = Epd7in5bAdapter.Epd7in5bAdapter()
        output_adapters.append(epd)
    elif display_colours == "bw":
        import Epd7in5Adapter
        epd = Epd7in5Adapter.Epd7in5Adapter()
        output_adapters.append(epd)

available_panels = {
    "day-list": DayListPanel,
    "month-overview": MonthOvPanel,
    "day-view": DayViewPanel,
    "day-focus-list": DayFocusListPanel,
    "agenda-list": AgendaListPanel,
    "month-view": MonthViewPanel,
    "image-frame": ImageFramePanel,
}

loop_timer = LoopTimer(
    update_interval, run_on_hour=run_on_hour, max_loop_count=max_loop_count)

"""Main loop starts from here"""


def main():
    owm = OwmForecasts.OwmForecasts(
        location, api_key, paid_api=owm_paid_subscription)
    events_cal = IcalEvents.IcalEvents(ical_urls, highlighted_ical_urls)
    rss = RssParserPosts.RssParserPosts(rss_feeds)
    crypto = GeckoCrypto.GeckoCrypto(crypto_coins)

    while True:
        loop_timer.begin_loop()
        start_time = loop_timer.get_current()[0]

        if start_time.hour in calibrate_hours and loop_timer.is_new_hour_loop():
            debug.print_line("Calibrating outputs")
            for output in output_adapters:
                output.calibrate()

        if choosen_design in available_panels.keys():
            design = available_panels[choosen_design]((epd.width, epd.height))
        else:
            raise ImportError(
                "choosen_design must be valid (" + choosen_design + ")")

        debug.print_line("Fetching weather information from open weather map")
        owm.reload()
        design.add_weather(owm)

        debug.print_line('Fetching events from your calendar')
        events_cal.reload()
        design.add_calendar(events_cal)

        debug.print_line('Fetching posts from your rss-feeds')
        rss.reload()
        design.add_rssfeed(rss)

        debug.print_line('Fetching crypto prices from coin gecko')
        crypto.reload()
        design.add_crypto(crypto)

        debug.print_line("\nStarting to render")
        for i, output in enumerate(output_adapters):
            try:
                output.render(design)
                debug.print_line(str(i + 1) + " of " +
                                 str(len(output_adapters)) + " rendered")
            except BaseException as ex:
                debug.print_err(ex, "Failed to render output " +
                                str(i + 1) + " of " + str(len(output_adapters)))

        debug.print_line("=> Finished rendering" + "\n")

        loop_timer.end_loop()

        if loop_timer.was_last_loop():
            debug.print_line("Maximum loop count " +
                             str(loop_timer.loop_count) + " reached, exiting.")
            return

        sleep_time = loop_timer.time_until_next()
        debug.print_line("This loop took " +
                         str(loop_timer.get_last_duration()) + " to execute.")
        debug.print_line("Sleeping " + str(sleep_time) + " until next loop.")
        sleep(sleep_time.total_seconds())


if __name__ == '__main__':
    main()
