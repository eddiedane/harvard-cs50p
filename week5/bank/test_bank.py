from bank import value

def test_hello():
  assert value("hello") == 0

def test_hey():
  assert value("Hey") == 20

def test_sup():
  assert value("sup") == 100

