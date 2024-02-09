from numb3rs import validate

def test_incomplete():
  assert validate("184") == False

def test_bad_chars():
  assert validate("197,43,22,9") == False

def test_range():
  assert validate("127.888.23.1") == False

def test_correct():
  assert validate("197.43.22.9") == True