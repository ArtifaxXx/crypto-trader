import ccxt


def get_exchange_data(exchange_name, ticker, resolution='1h'):
    """
    this function will return current exchange data on demand
    :param exchange_name: string that identifies the exchange
    :param ticker: string that identifies the pair
    :param resolution: string that identifies frequency of candle data
    :return: a dict of objects
    """
    exchange = getattr(ccxt, exchange_name)()
    result = dict()
    if exchange.has['fetchOHLCV']:
        result['candle_data'] = exchange.fetch_ohlcv(ticker, resolution)
    result['ticker'] = exchange.fetch_ticker(ticker)
    result['trades'] = exchange.fetch_trades(ticker)
    print(result)
    return result

