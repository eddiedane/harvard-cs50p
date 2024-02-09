from twttr import shorten

def test_twitter():
  assert shorten("twitter.com") == "twttr.cm"

def test_vowels():
  assert shorten("aeiouAEIOU") == ""

def test_number():
  assert shorten("12") == "12"

def test_special_chars():
  assert shorten("?") == "?"