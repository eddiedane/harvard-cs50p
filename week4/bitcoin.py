import sys
import requests

BPI_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"

try:
  n = float(sys.argv[1])
  res = requests.get(BPI_URL)
except ValueError:
  sys.exit("Invalid n")
except requests.RequestException:
  sys.exit("Request error")

btc_price = res.json()["bpi"]["USD"]["rate_float"]

print(f"${n * btc_price:,.4f}")