from seasons import date_to_words
import pytest

def test_valid_date():
    assert date_to_words("2008-01-01") == "Eight million, two hundred forty-four thousand minutes"


def test_invalid_date():
    with pytest.raises(SystemExit):
        date_to_words("2000-02-31")


def test_invalid_format():
    with pytest.raises(SystemExit):
        date_to_words("March 25, 2000")