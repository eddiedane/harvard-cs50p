from working import convert
import pytest


def test_format():
  with pytest.raises(ValueError):
    assert convert("9 AM 5 PM")


def test_empty():
  with pytest.raises(ValueError):
    assert convert("9:60 AM to 5:60 PM")


def test_am_to_pm():
  assert convert("9:00 AM to 5:00 PM") == "09:00 to 17:00"


def test_pm_to_am():
  assert convert("9:00 PM to 5:00 AM") == "21:00 to 05:00"