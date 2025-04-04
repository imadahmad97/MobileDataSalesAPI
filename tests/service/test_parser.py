from app.service.parser import parse_csv_content, parse_text_from_binary


def test_parse_text_from_binary():
    content = b"header1,header2\nvalue1,value2\n"
    expected_result = [["header1", "header2"], ["value1", "value2"]]

    result = parse_text_from_binary(content)

    assert result == expected_result
