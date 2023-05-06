import ccxt

binance_exchange = ccxt.binance({
        'apiKey': "",
        'secret': ""
    })

kraken_exchange = ccxt.kraken({
        'apiKey': "",
        'secret': ""
    })

bybit_exchange = ccxt.bybit({
        'apiKey': "",
        'secret': ""
    })

okx_exchange = ccxt.okx({
        'apiKey': "",
        'secret': ""
    })

bitget_exchange = ccxt.bitget({
        'apiKey': "",
        'secret': ""
    })

kucoin_exchange = ccxt.kucoin({
        'apiKey': "",
        'secret': ""
    })

coinex_exchange = ccxt.coinex({
        'apiKey': "",
        'secret': ""
    })

poloniex_exchange = ccxt.poloniex({
        'apiKey': "",
        'secret': ""
    })

base_asset = "USDT"
profit_limit = 1.5

def check_symbol_exchange(id, exchange, symbol, ask_price, bid_price):
    if exchange.id.lower() == "kraken":
        symbol = symbol.replace("USDT", "USD")

    try:
        ticker = exchange.fetch_ticker(symbol)

        if exchange.id.lower() == "poloniex":
            exchange_ask_price = float(ticker['info']['bid'])
            exchange_bid_price = float(ticker['info']['ask'])
        else:
            exchange_ask_price = float(ticker['bid'])
            exchange_bid_price = float(ticker['ask'])

        if ask_price != 0 and exchange_bid_price != 0 and exchange_bid_price < bid_price and exchange_bid_price < ask_price:
            diff = ask_price - exchange_bid_price

            percentage = round((diff / exchange_bid_price) * 100, 3)

            if percentage >= float(profit_limit) and percentage < 100:
                print("Nueva oportunidad de Arbitraje.")
                print("")
                print(f"Compra en {exchange.id} {symbol}: {exchange_bid_price}")
                print(f"Vende en {id} {symbol}: {ask_price}")
                print(f"Oportunidad del {percentage} %\n")

        if bid_price != 0 and exchange_ask_price != 0 and bid_price < exchange_bid_price and bid_price < exchange_ask_price:
            diff = exchange_ask_price - bid_price

            percentage = round((diff / bid_price) * 100, 3)

            if percentage >= float(profit_limit) and percentage < 100:
                print("Nueva oportunidad de Arbitraje.")
                print("")
                print(f"Compra en {id} {symbol}: {bid_price}")
                print(f"Vende en {exchange.id} {symbol}: {exchange_ask_price}")
                print(f"Oportunidad del {percentage} %\n")

    except ccxt.ExchangeError:
        return

def search(exchange, search_exchange):
    print(f"\033[33mSearching in {exchange.id} > {search_exchange.id}...\n")
    try:
        exchange.load_time_difference()

        markets = exchange.load_markets()

        symbols = list(markets.keys())

        for symbol in symbols:
            if symbol == base_asset.upper() or symbol.endswith(base_asset.upper()) or symbol.startswith(base_asset.upper()):
                if exchange.id == "bybit":
                    recv_window = 10000
                    ticker = exchange.fetch_ticker(symbol, recv_window=recv_window)
                else:
                    ticker = exchange.fetch_ticker(symbol)

                bid_price = float(ticker['ask'])
                ask_price = float(ticker['bid'])

                if exchange.id.lower() == "kraken" and symbol.endswith("/USD"):
                    symbol = symbol.replace("/USD", "/USDT")

                check_symbol_exchange(exchange.id, search_exchange, symbol, bid_price, ask_price)

    except ccxt.ExchangeError as e:
        return

def main():
    try:
        global base_asset
        base_asset = input("What currency do you want to search? ") or "USDT"
        global profit_limit
        profit_limit = input("What profit margin? ") or 1.5

        print(f"\nSearching {base_asset} with {profit_limit} % limit...\n")

        #search(binance_exchange, poloniex_exchange)
        search(binance_exchange, kraken_exchange)
        search(binance_exchange, bitget_exchange)
        search(binance_exchange, kucoin_exchange)
        search(binance_exchange, coinex_exchange)
        search(binance_exchange, bybit_exchange)
        search(binance_exchange, okx_exchange)

        #search(kraken_exchange, poloniex_exchange)
        search(kraken_exchange, bitget_exchange)
        search(kraken_exchange, kucoin_exchange)
        search(kraken_exchange, coinex_exchange)
        search(kraken_exchange, bybit_exchange)
        search(kraken_exchange, okx_exchange)

        search(bitget_exchange, kucoin_exchange)
        search(bitget_exchange, coinex_exchange)
        search(bitget_exchange, bybit_exchange)
        search(bitget_exchange, okx_exchange)
        #search(bitget_exchange, poloniex_exchange)

        search(kucoin_exchange, coinex_exchange)
        search(kucoin_exchange, bitget_exchange)
        search(kucoin_exchange, okx_exchange)
        #search(kucoin_exchange, poloniex_exchange)

        search(bitget_exchange, coinex_exchange)
        search(bitget_exchange, okx_exchange)
        #search(bitget_exchange, poloniex_exchange)

        search(coinex_exchange, okx_exchange)
        #search(coinex_exchange, poloniex_exchange)

        #search(okx_exchange, poloniex_exchange)
    except KeyboardInterrupt:
        print("Exit")

main()