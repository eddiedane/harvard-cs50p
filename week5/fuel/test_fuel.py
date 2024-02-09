import fuel as f
import pytest

def test_75():
  assert f.convert("3/4") == 75

def test_zero_division_error():
  with pytest.raises(ZeroDivisionError):
    f.convert("3/0")

def test_value_error():
  with pytest.raises(ValueError):
    f.convert("3/1")

def test_e():
    assert f.gauge(1) == "E"

def test_percentage():
   assert f.gauge(50) == "50%"

def test_f():
   assert f.gauge(99) == "F"