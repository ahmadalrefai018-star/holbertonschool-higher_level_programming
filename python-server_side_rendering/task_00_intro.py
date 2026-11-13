#!/usr/bin/python3
"""Generate personalized invitation files from a text template."""

import logging


def generate_invitations(template, attendees):
    """Write one numbered invitation file for each attendee."""
    if not isinstance(template, str):
        logging.error("Invalid template type. Expected a string.")
        return

    if not isinstance(attendees, list) or not all(
        isinstance(attendee, dict) for attendee in attendees
    ):
        logging.error("Invalid attendees type. Expected a list of dictionaries.")
        return

    if not template:
        logging.error("Template is empty, no output files generated.")
        return

    if not attendees:
        logging.error("No data provided, no output files generated.")
        return

    fields = ("name", "event_title", "event_date", "event_location")

    for index, attendee in enumerate(attendees, start=1):
        values = {}
        for field in fields:
            value = attendee.get(field)
            values[field] = "N/A" if value is None else str(value)

        invitation = template.format_map(values)
        filename = f"output_{index}.txt"

        try:
            with open(filename, "x", encoding="utf-8") as output_file:
                output_file.write(invitation)
        except FileExistsError:
            logging.warning("%s already exists. Skipping it.", filename)
        except OSError as error:
            logging.error("Could not write %s: %s", filename, error)
