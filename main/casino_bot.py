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


def execute_casino_bot_simulation():
    # Inputs:
    #  price_list,
    #  exchange,
    #  ticker,
    #  length,
    #  deposit,
    #  profit margin param,
    #  buy order spread
    pass
