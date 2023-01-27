from ics import Calendar, Event
from datetime import date, datetime
from source import source

calendar = Calendar()


def parse_start_or_end(timestamp: str):
    timestamp = timestamp.replace("UTC", "").strip()

    if timestamp == "None":
        return

    if " - " in timestamp:
        return datetime.strptime(timestamp.replace(" - ", " ") + " 2023", "%B %d %M:%S %Y")

    return datetime.strptime(timestamp + " 2023", "%B %d %Y")


def parse_timestamp(timestamp: str):
    start, end = timestamp.split(" to ")
    return parse_start_or_end(start), parse_start_or_end(end)


def main():
    for timestamp, details in source.items():
        start, end = parse_timestamp(timestamp)
        name, description = details
        event = Event(name, start, description=description)
        if end is not None:
            event.end = end
        calendar.events.add(event)

    with open("calendar.ics", "w") as file:
        file.writelines(calendar.serialize_iter())


main()
