from post_generator import get_length_str


def test_get_length_str_short():
    assert get_length_str("Short") == "1 to 5 lines"


def test_get_length_str_medium():
    assert get_length_str("Medium") == "6 to 10 lines"


def test_get_length_str_long():
    assert get_length_str("Long") == "11 to 15 lines"


def test_get_length_str_invalid():
    assert get_length_str("Invalid") is None