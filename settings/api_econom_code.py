import requests

def get_tiker_shares(name):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={name}&apikey=*'
    r = requests.get(url)
    data = r.json()
    result = []
    for match in data['bestMatches']:
        temp = {'symbol': match['1. symbol'], 'name': match['2. name']}
        result.append(temp)

    result_str = ""
    
    for item in result:
        result_str += "Tiker: {} | Company: {}\n".format(item["symbol"], item["name"])
    return result_str
    
def check_tiker(ticker):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey=*'
    r = requests.get(url)
    data = r.json()
    result = []
    for match in data['bestMatches']:
        temp = {'symbol': match['1. symbol'], 'name': match['2. name']}
        result.append(temp)

    for match in result:
        if match['symbol'] == ticker.upper():
            return match['symbol']
    return "Такого тикера не найдено"

def get_data_shares(name):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={name}&outputsize=compact&apikey=*'
    r = requests.get(url)
    data = r.json()
    
    daily_data = data['Time Series (Daily)']
    averages = []

    for date, values in daily_data.items():
        o, h, l, c = float(values['1. open']), float(values['2. high']), float(values['3. low']), float(values['4. close'])
        avg = round((o + h + l + c) / 4, 2)
        averages.append(avg)

    return averages
