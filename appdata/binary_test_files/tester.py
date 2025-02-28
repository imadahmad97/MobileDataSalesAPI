def _parse_binary_file(contents: bytes) -> dict:
    """
    Parses the contents of a binary file and returns the data as a dictionary.
    This method only extracts data; validation is handled separately.
    """
    parsed_data = {}

    for line_number, line in enumerate(contents.split("\n"), start=1):
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.lower().replace(" ", "_").strip()
        value = value.strip()

        parsed_data[key] = value

    errors = MobileDataPurchaseRequest._validate_parsed_data(parsed_data)

    if errors:
        raise HTTPException(status_code=400, detail={"errors": errors})

    return parsed_data
