from utility_functions import get_exchange_data, recalculate_casino_bot_sell_price, create_casino_bot_simulation_buy_order_net


def execute_casino_bot():
    # Inputs:
    #  exchange,
    #  ticker,
    #  percentage of deposit to use,
    #  profit margin parameter,
    #  buy order spread
    # Bot is triggered by the call of the function
    # It connects to the designated exchange and finds out the balance
    # it executes the following strategy:
    # 1. Place a buy order for the selected pair (hit market value for immediate purchase)
    # 2. Generate buy orders net with specified params
    # 3. Generate sell order for the bought amount
    # 4. On sell order trigger finish the execution and report results
    # 5. On buy order hit - cancel sell order and recalculate new sell order price
    # 6. On exhaustion of buy orders report result and exit
    pass


def execute_casino_bot_simulation(exchange='binance',
                                  ticker='TRX/BNB',
                                  commission=0.001,  # exchange commission per operation
                                  batch_size=500,  # number of historic data points, 500 per page
                                  his_data_frequency='1h',  # frequency of historic data
                                  initial_deposit=1000,
                                  entry_commitment=1,  # units used for initial purchase
                                  profit_margin=0.01,  # how much do we want our initial spread to be
                                  buy_order_spread=0.01,  # how far apart are we putting buy orders
                                  buy_order_factor=2):  # by what factor we increase the stake at each iteration

    print('Bot initialisation')
    # Initialize entry parameters
    deposit = initial_deposit
    tokens = 0

    # Get exchange data and extract candles
    print('Getting exchange data')
    exchange_data = get_exchange_data(exchange, ticker, his_data_frequency)
    candle_list = exchange_data['candle_data'][-batch_size:]

    # Get market price and execute the order
    print('Executing initial buy order')
    initial_price = candle_list[0][4]
    deposit_spent = entry_commitment + entry_commitment * commission
    tokens_bought = entry_commitment / initial_price

    # Set average and sell price and update initial parameters
    print('Setting initial average and sell prices')
    average_price, sell_price = recalculate_casino_bot_sell_price(0,
                                                                  0,
                                                                  tokens_bought,
                                                                  initial_price,
                                                                  profit_margin,
                                                                  commission)
    deposit -= deposit_spent
    tokens += tokens_bought

    # Create buy order net
    print('Creating buy order net')
    buy_orders = create_casino_bot_simulation_buy_order_net(deposit,
                                                            entry_commitment,
                                                            buy_order_factor,
                                                            initial_price,
                                                            buy_order_spread)
    # iterating over historical data
    print('Starting iteration cycle')
    cycles = 0
    for candle in candle_list[1:]:  # Starting from 2nd candle
        cycles += 1
        if candle[2] > sell_price:  # We have sold at our sell price, break cycle
            deposit += sell_price*tokens - sell_price*tokens*commission
            tokens -= tokens_bought
            print('Sell executed. Terminating')
            break
        if candle[3] < buy_orders[0][1]:  # Lowest price hit bellow our highest order
            print('Executing buy orders')
            orders_executed = 0
            for order in buy_orders:  # Check which orders got executed
                if candle[3] < order[1]:  # if order executed
                    tokens += order[0]  # add tokens bought
                    deposit -= (order[0]*order[1] + order[0]*order[1]*commission)  # subtract deposit spent
                    orders_executed += 1  # increment executed orders number
                    # For every executed order we recalculate our sell price
                    average_price, sell_price = recalculate_casino_bot_sell_price(tokens,
                                                                                  average_price,
                                                                                  order[0],
                                                                                  order[1],
                                                                                  profit_margin,
                                                                                  commission)
            buy_orders = buy_orders[orders_executed:]  # remove executed orders from buy_orders list
            print('%i buy orders executed' % orders_executed)
    print('%i cycles executed' % cycles)

    # returning results
    profit = deposit - initial_deposit + tokens*exchange_data['ticker']['last']
    return deposit, tokens, profit


def main():
    print(execute_casino_bot_simulation(his_data_frequency='1m', profit_margin=0.01, ticker='KAVA/BNB'))


if __name__ == "__main__":
    main()
