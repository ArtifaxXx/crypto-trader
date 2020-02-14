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
                                      previous_price,
                                      new_token_purchased,
                                      new_price,
                                      profit_margin,
                                      commission):
    # TODO: @phoenixkr to review the logic here
       required_profit = (previous_tokens_purchased * previous_price + new_token_purchased * new_price) * \
                      (1 + profit_margin + commission)
    new_sell_price = required_profit / (previous_tokens_purchased + new_token_purchased)
    return new_sell_price
 """previous_price - это прошлая цена? Но ведь она не является средней ценой покупки всех токенов на предыдущих этапах?! 
    Я, может, просто не правильно понял значение переменной previous_price: Если были покупки по 100, 99, 98, 97, а
    сейчас покупаем по 96, то previous_price 97 же? Тогда мы не учитываем предыдущие покупки получается.
    Думаю, что нужна average_price - средняя цена покупки всех токенов, на которую мы и накинем наш profit_margin
       
       На первом этапе:
       average_price = initial_price            # initial_price - это цена первой покупки у тебя, так ведь?
       
       На следующих этапах:
       total_token_purchased = total_token_purchased + new_token_purchased #всего куплено токенов
       average_price = (average_price * total_tokens_purchased + new_price * new_token_purchased) / 
       (total_token_purchased)
       new_sell_price = average_price *(1 + profit_margin + comission)          
       
       Например, купили 1 за 100 и 2 за 99 
       initial_price = 100
       average_price = 100
       total_token_purchased = 1 + 2 = 3
       average_price = (100 * 1 + 99 * 2) / (3) = 99,333333
       new_sell_price = 99,33333 * (1 + 0,01 + 0,001) = 100,42599663
       
       У тебя получится тоже самое на первых двух этапах, но немного странно считаешь, как будто наоборот, откуда взялась переменная
       required_profit? При том же рассчёте получается required_profit = (1 * 100 + 2 * 99) * (1 + 0.01 + 0.001) = 301,278
       Нам нужен профит 301,278... чего?... цены, токенов? Я не понял.
       Но тем не менее, признаю, что new_sell_price = 301,278 / (1 + 2) = 100,426
       ИТОГО: можно и твоё оставить, если твоя previous_price = average_price  и  previous_tokens_purchased = total_tokens_purchased
       Но считаешь ты, как бы сказать, необычно... Голосую за мои переменные и мой вариант!
       """
