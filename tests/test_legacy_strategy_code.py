from main.legacy_strategy_code import main
from main.exchange_data import get_exchange_data


def test_code_runs():
    main()


def test_exchange_data():
    result = get_exchange_data('binance', 'TRX/BNB', '1d')
    assert len(result['candle_data']) == 500
    assert result['ticker']
    assert result['trades']
