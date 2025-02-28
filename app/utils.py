import io
import csv


async def parse_csv_rows_into_lists(contents: bytes) -> list[list[str]]:
    """
    Parses the contents of a csv file into a list of rows, where each row is a list of strings.
    """
    csv_text: io.StringIO = io.StringIO(contents.decode("utf-8"))
    reader: csv.reader = csv.reader(csv_text)
    parsed_rows: list[list[str]] = list(reader)

    return parsed_rows
