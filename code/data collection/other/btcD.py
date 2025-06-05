import requests

# Fetch Bitcoin dominance from CoinGecko
url = "https://api.coingecko.com/api/v3/global"
response = requests.get(url)
data = response.json()

# Extract Bitcoin dominance
btc_dominance = data['data']['market_cap_percentage']['btc']
print(f"Bitcoin Dominance: {btc_dominance}%")
