from plates import is_valid

def test_with_num():
  assert is_valid("CS50")

def test_without_num():
  assert is_valid("NRVOUS")

def test_mid_zero():
  assert not is_valid("CS05")

def test_num_end():
  assert not is_valid("CS50P2")

def test_special_chars():
  assert not is_valid("PI3.14")

def test_short():
  assert not is_valid("678489")

def test_long():
  assert not is_valid("OUTATIME")