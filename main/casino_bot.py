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

    # Initialize entry parameters
    deposit = initial_deposit
    tokens = 0

    # Get exchange data and extract candles
    exchange_data = get_exchange_data(exchange, ticker, his_data_frequency)
    candle_list = exchange_data['candle_data'][-batch_size:]

    # Get market price and execute the order
    initial_price = candle_list[0][4]
    deposit_spent = entry_commitment + entry_commitment * commission
    tokens_bought = entry_commitment / initial_price

    # Set average and sell price and update initial parameters
    average_price, initial_sell_price = recalculate_casino_bot_sell_price(0,
                                                                          0,
                                                                          tokens_bought,
                                                                          initial_price,
                                                                          profit_margin,
                                                                          commission)
    deposit -= deposit_spent
    tokens += tokens_bought

    # Create buy order net
    buy_orders = create_casino_bot_simulation_buy_order_net(deposit,
                                                            entry_commitment,
                                                            buy_order_factor,
                                                            initial_price,
                                                            buy_order_spread)

    # Iterate over candles
    # Compare candle data with our orders and convert accordingly
    # Cases:
    #   if end of the candle data - loop will finish
    #   sell order has executed - exit, report results
    #   buy orders were executed - redo the sell
    #   if none, continue

    '''
            1504541580000, // UTC timestamp in milliseconds, integer
            4235.4,        // (O)pen price, float
            4240.6,        // (H)ighest price, float
            4230.0,        // (L)owest price, float
            4230.7,        // (C)losing price, float
            37.72941911    // (V)olume (in terms of the base currency), float
    '''
    sell_price = initial_sell_price
    for candle in candle_list[1:]:  # Starting from 2nd candle
        if candle[2] > sell_price:  # We have sold at our sell price, break cycle
            deposit += sell_price*tokens - sell_price*tokens*commission
            tokens -= tokens_bought
            break
        if candle[3] < buy_orders[0][1]:  # Lowest price hit bellow our highest order
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

    return deposit, tokens


def main():
    print(execute_casino_bot_simulation())


if __name__ == "__main__":
    main()
