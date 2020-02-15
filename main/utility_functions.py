from itertools import count
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


def create_casino_bot_simulation_buy_order_net(deposit, entry_commitment, buy_order_factor, initial_price, buy_order_spread):
    buy_orders = []
    deposit_used = 0
    for i in count(0):  # this is an infinite loop
        next_order_commitment = entry_commitment * (buy_order_factor ** (i+1))  # i starts with 0
        deposit_used += next_order_commitment
        if deposit_used > deposit:  # Check that we are not overusing our funds, stop loop if we are
            break
        cur_buy_order_price = round(initial_price * (1 - buy_order_spread*(i+1)), 6)
        buy_orders.append((next_order_commitment, cur_buy_order_price))  # add an order entry
    return buy_orders


def casino_bot_cycle(candle_list, buy_orders, deposit, tokens, sell_price, average_price, commission, profit_margin):
    cycles = 1
    orders_executed = 0
    for candle in candle_list[1:]:  # Starting from 2nd candle
        cycles += 1
        if candle[2] > sell_price:  # We have sold at our sell price, break cycle
            deposit += sell_price * tokens - sell_price * tokens * commission
            tokens -= tokens
            print('Sell executed. Terminating')
            break
        if orders_executed == len(buy_orders):
            break
        if candle[3] < buy_orders[orders_executed][1]:  # Lowest price hit bellow our highest order
            print('Executing buy orders')
            for order in buy_orders[orders_executed:]:  # Check which orders got executed
                if candle[3] < order[1]:  # if order executed
                    tokens += order[0]  # add tokens bought
                    deposit -= (order[0] * order[1] + order[0] * order[1] * commission)  # subtract deposit spent
                    orders_executed += 1  # increment executed orders number
                    # For every executed order we recalculate our sell price
                    average_price, sell_price = recalculate_casino_bot_sell_price(tokens,
                                                                                  average_price,
                                                                                  order[0],
                                                                                  order[1],
                                                                                  profit_margin,
                                                                                  commission)
            print('%i buy orders executed' % orders_executed)

    return deposit, tokens, cycles
