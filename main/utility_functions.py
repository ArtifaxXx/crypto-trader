import ccxt


def get_exchange_data(exchange_name, ticker, frequency='1h'):
    """
    this function will return current exchange data on demand
    :param exchange_name: string that identifies the exchange
    :param ticker: string that identifies the pair
    :param frequency: string that identifies frequency of candle data
    :return: a dict of objects
    """
    exchange = getattr(ccxt, exchange_name)()
    result = dict()
    if exchange.has['fetchOHLCV']:
        '''
        1504541580000, // UTC timestamp in milliseconds, integer
        4235.4,        // (O)pen price, float
        4240.6,        // (H)ighest price, float
        4230.0,        // (L)owest price, float
        4230.7,        // (C)losing price, float
        37.72941911    // (V)olume (in terms of the base currency), float
        '''
        result['candle_data'] = exchange.fetch_ohlcv(ticker, frequency)

    result['ticker'] = exchange.fetch_ticker(ticker)
    result['trades'] = exchange.fetch_trades(ticker)
    return result


def recalculate_casino_bot_sell_price(previous_tokens_purchased,
                                      previous_average_price,
                                      new_token_purchased,
                                      new_price,
                                      profit_margin,
                                      commission):
    new_average_price = (previous_tokens_purchased * previous_average_price + new_token_purchased * new_price) / \
                        (previous_tokens_purchased + new_token_purchased)
    new_sell_price = new_average_price * (1 + profit_margin + commission)

    return new_average_price, new_sell_price
