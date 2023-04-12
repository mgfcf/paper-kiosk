from settings import hours, language
from datetime import timedelta, datetime, timezone
from DictionaryMapper import get_text
from Dictionary import multiday_events, allday_events

first_occurrence_char = '['
middle_occurrence_char = '|'
last_occurrence_char = ']'
multiday_begin_character = ' >'
multiday_end_character = '< '
until_character = ' - '
allday_character = "•"
multiday_character = allday_character + allday_character


def time_str(dt):
    if hours is "12":
        return dt.strftime("%I:%M%p")
    elif hours is "24":
        return dt.strftime("%H:%M")
    else:
        return str(dt)


def event_prefix_str_md_dif(event, relative_date=None):
    if relative_date is None:
        relative_date = event.begin_datetime.date()

    if event.multiday is False:
        return event_time_summary(event)

    # Relative to
    # First day
    elif __equal__(event.begin_datetime, relative_date):
        return event_time_summary(event) + multiday_begin_character

    # Last day
    elif __equal__(event.end_datetime, relative_date) or \
            (__day_duration__(event.end_datetime) == timedelta(0) and __equal__(relative_date + timedelta(1), event.end_datetime)):
        return multiday_end_character + event_time_summary(event)

    # Some day
    else:
        event.allday = True
        return multiday_end_character + event_time_summary(event) + multiday_begin_character


def event_prefix_str(event, relative_date=None):
    if relative_date is None:
        relative_date = event.begin_datetime.date()

    if event.multiday:
        return get_text(multiday_events)
    else:
        return event_time_detailed(event)


def event_prefix_str_sum(event, relative_date=None):
    if relative_date is None:
        relative_date = event.begin_datetime.date()

    if event.multiday:
        return multiday_character
    else:
        return event_time_summary(event)


def event_time_summary(event):
    if event.allday:
        return allday_character
    else:
        return time_str(event.begin_datetime)


def event_time_detailed(event):
    if event.allday:
        return get_text(allday_events)
    else:
        return time_str(event.begin_datetime) + until_character + time_str(event.end_datetime)


def date_str(dt):
    return remove_leading_zero(dt.strftime('%d. %b'))


def remove_leading_zero(text):
    while text[0] is '0':
        text = text[1:]
    return text


def date_summary_str(dt):
    day = remove_leading_zero(dt.strftime("%d"))
    if language is "en":
        return dt.strftime('%a ' + day + '. %b')
    elif language is "de":
        return dt.strftime(day + '. %b., %a')
    else:
        return dt.strftime('%a ' + day + '. %b')


def __equal__(dt1, dt2):
    return dt1.day == dt2.day and \
        dt1.month == dt2.month and \
        dt1.year == dt2.year


def __day_duration__(dt):
    day_begin = datetime(dt.year, dt.month, dt.day, 0, 0, 0, 0, timezone.utc)
    return dt - day_begin
