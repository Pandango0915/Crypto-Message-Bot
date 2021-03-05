import requests
import time #make a delay in code

# global variables
api_key = '2255c494-cce0-417c-88be-db0539aefe84'
bot_token = '1499191929:AAGlm0a3g_OTL4Xk2t8nS1qo2G2cPlRiNXs'
chat_id = '1632647478'
bitcoin_threshold1 = 30000
bitcoin_threshold2 = 40000
ethereum_threshold1 = 1300
ethereum_threshold2 = 2000
litecoin_threshold1 = 100
litecoin_threshold2 = 170
time_interval = 5 * 60 # in seconds

def get_crypto_prices():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    # make a request to the coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()
# extract the bitcoin price from the json data
    btc_price = response_json['data'][0]
    btc = btc_price['quote']['USD']['price']
# extract the ethereum price from the json data
    eth_price = response_json['data'][1]
    eth = eth_price['quote']['USD']['price']
# extract the litecoin price from json data, single out litecoin's dictionary
    ltc_price = next(item for item in response_json['data'] if item["name"] == "Litecoin")
    ltc = ltc_price['quote']['USD']['price']

    return [btc, eth, ltc]

# fn to send_message through telegram
def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"
# send the msg
    requests.get(url)


def bitcoin_threshold_low():
    global bitcoin_threshold1
    bitcoin_threshold1 -= 5000

def bitcoin_threshold_high():
    global bitcoin_threshold2
    bitcoin_threshold2 += 5000

def ethereum_threshold_low():
    global ethereum_threshold1
    ethereum_threshold1 -= 200

def ethereum_threshold_high():
    global ethereum_threshold2
    ethereum_threshold2 += 200

def litecoin_threshold_low():
    global litecoin_threshold1
    litecoin_threshold1 -= 50

def litecoin_threshold_high():
    global litecoin_threshold2
    litecoin_threshold2 += 30

# main fn to call, includes previous fcns
def main():
    price_list_bitcoin = []
    price_list_ethereum = []
    price_list_litecoin = []
# infinite loop
    while True:
        prices = get_crypto_prices()
        price_list_bitcoin.append(prices[0])
        price_list_ethereum.append(prices[1])
        price_list_litecoin.append(prices[2])

    # if the price falls below threshold1, send an immediate msg
        if prices[0] < bitcoin_threshold1:
            send_message(chat_id=chat_id, msg=f'BTC Price Drop Alert: {prices[0]}')
            bitcoin_threshold_low()
    # if the price goes above threshold2, send an immediate msg
        if prices[0] > bitcoin_threshold2:
            send_message(chat_id=chat_id, msg=f'BTC Price Raise Alert: {prices[0]}')
            bitcoin_threshold_high()
    # if the price falls below threshold1, send an immediate msg
        if prices[1] < ethereum_threshold1:
            send_message(chat_id=chat_id, msg=f'ETH Price Drop Alert: {prices[1]}')
            ethereum_threshold_low()
    # if the price goes above threshold2, send an immediate msg
        if prices[1] > ethereum_threshold2:
            send_message(chat_id=chat_id, msg=f'ETH Price Raise Alert: {prices[1]}')
            ethereum_threshold_high()
    # if the price falls below threshold1, send an immediate msg
        if prices[2] < litecoin_threshold1:
            send_message(chat_id=chat_id, msg=f'LTC Price Drop Alert: {prices[2]}')
            litecoin_threshold_low()
    # if the price goes above threshold2, send an immediate msg
        if prices[2] > litecoin_threshold2:
            send_message(chat_id=chat_id, msg=f'LTC Price Raise Alert: {prices[2]}')
            litecoin_threshold_high()

    # fill array with last 30 btc price
        if len(price_list_bitcoin) >= 30:
            price_change_bitcoin = max(price_list_bitcoin) - min(price_list_bitcoin)
            if price_change_bitcoin >= 2000:
                send_message(chat_id=chat_id, msg=f'BTC Price: {prices[0]}')
                send_message(chat_id=chat_id, msg=f'BTC Price Change Alert: {price_change_bitcoin}')
                # empty the price_list
            price_list_bitcoin = []

        if len(price_list_ethereum) >= 30:
            price_change_ethereum = max(price_list_ethereum) - min(price_list_ethereum)
            if price_change_ethereum >= 500:
                send_message(chat_id=chat_id, msg=f'ETH Price: {prices[1]}')
                send_message(chat_id=chat_id, msg=f'ETH Price Change Alert: {price_change_ethereum}')
                # empty the price_list
            price_list_ethereum = []

        if len(price_list_litecoin) >= 30:
            price_change_litecoin = max(price_list_litecoin) - min(price_list_litecoin)
            if price_change_litecoin >= 50:
                send_message(chat_id=chat_id, msg=f'LTC Price: {prices[2]}')
                send_message(chat_id=chat_id, msg=f'LTC Price Change Alert: {price_change_litecoin}')
                # empty the price_list
            price_list_litecoin = []

# fetch the price for every dash minutes
        time.sleep(time_interval)

# fancy way to activate the main() function. if this is main program, python assigns to variable __name__ the string __main__
if __name__ == '__main__': #if this is true, run function main()
    main()
