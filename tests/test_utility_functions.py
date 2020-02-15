import pytest
from main.utility_functions import get_exchange_data, recalculate_casino_bot_sell_price
from main.utility_functions import create_casino_bot_simulation_buy_order_net


def test_exchange_data():
    result = get_exchange_data('binance', 'TRX/BNB', '1d')
    assert len(result['candle_data']) == 500
    assert result['ticker']
    assert result['trades']


def test_recalculate_casino_bot_sell_price():
    with pytest.raises(Exception):
        assert recalculate_casino_bot_sell_price(0, 0, 0, 0, 0, 0)

    assert round(recalculate_casino_bot_sell_price(0, 0, 1, 1, 0, 0)[0]), \
        round(recalculate_casino_bot_sell_price(0, 0, 1, 1, 0, 0)[1]) == (1, 1)
    assert round(recalculate_casino_bot_sell_price(0, 0, 1, 1000, 0.1, 0.05)[0]), \
        round(recalculate_casino_bot_sell_price(0, 0, 1, 1000, 0.1, 0.05)[1]) == (1000, 1150)
    assert round(recalculate_casino_bot_sell_price(1, 10, 2, 5, 0.1, 0)[0], 1), \
        round(recalculate_casino_bot_sell_price(1, 10, 2, 5, 0.1, 0)[1], 1) == 6.9


def test_create_casino_bot_buy_order_net():
    assert create_casino_bot_simulation_buy_order_net(deposit=10,
                                                      entry_commitment=1,
                                                      buy_order_factor=2,
                                                      initial_price=1,
                                                      buy_order_spread=0.1) == [(2, 0.9), (4, 0.8)]

    assert create_casino_bot_simulation_buy_order_net(deposit=10,
                                                      entry_commitment=0.1,
                                                      buy_order_factor=2,
                                                      initial_price=1,
                                                      buy_order_spread=0.1) == [(0.2, 0.9),
                                                                                (0.4, 0.8),
                                                                                (0.8, 0.7),
                                                                                (1.6, 0.6),
                                                                                (3.2, 0.5)]

    assert create_casino_bot_simulation_buy_order_net(deposit=1000,
                                                      entry_commitment=0.1,
                                                      buy_order_factor=3,
                                                      initial_price=0.1,
                                                      buy_order_spread=0.01) == [(0.30000000000000004, 0.099),
                                                                                 (0.9, 0.098),
                                                                                 (2.7, 0.097),
                                                                                 (8.1, 0.096),
                                                                                 (24.3, 0.095),
                                                                                 (72.9, 0.094),
                                                                                 (218.70000000000002, 0.093),
                                                                                 (656.1, 0.092)]

