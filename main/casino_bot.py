from exchange_data import get_exchange_data

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
                                  batch_size=500,  # number of historic data points, 500 per page
                                  his_data_frequency='1h',  # frequency of historic data
                                  initial_deposit=1000,
                                  profit_margin=0.01,  # how much do we want our initial spread to be
                                  buy_order_spread=0.01,  # how far apart are we putting buy orders
                                  buy_order_factor=2):  # by what factor we increase the stake at each iteration
    exchange_data = get_exchange_data(exchange, ticker, his_data_frequency)
    return exchange_data


# TODO: Move this to a console command
def main():
    print(execute_casino_bot_simulation())


if __name__ == "__main__":
    main()
