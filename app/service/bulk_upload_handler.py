import csv


def extract_data_from_csv(file_path):
    """
    Extracts data from a CSV file and returns a list of dictionaries.

    :param file_path: The path to the CSV file.
    :return: A list of dictionaries containing the data from the CSV file.
    """
    with open(file_path, "r") as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]

    return data
