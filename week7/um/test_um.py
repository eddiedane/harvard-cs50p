from um import count

def test_substring():
  assert count("yummy, yummy pie") == 0

def test_um():
  assert count("um, this is the coolest") == 1

def test_combine():
  assert count("Um, thanks for the album") == 1