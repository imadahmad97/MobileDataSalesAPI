import csv
import base64


async def parse_binary_text_to_dict(contents: bytes) -> dict:
    base64_string = contents.decode("utf-8")
    text = base64.b64decode(base64_string).decode("utf-8")
    data = {}
    for line in text.split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            data[key.lower().replace(" ", "_")] = value.strip()
    return data


def binary_to_string(binary_str: str) -> str:
    return "".join([chr(int(b, 2)) for b in binary_str.split()])


def parse_csv_to_dicts(file_path: str) -> list[dict]:
    with open(file_path, "r") as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]

    decoded_data = []
    for row in data:
        decoded_row = {binary_to_string(k): binary_to_string(v) for k, v in row.items()}
        decoded_data.append(decoded_row)
    return decoded_data
