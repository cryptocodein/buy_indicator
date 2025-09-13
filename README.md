
Небольшой скрипт на Python для:
	•	запроса исторических свечей с OKX (endpoint /api/v5/market/history-candles);
	•	расчёта SMA (Simple Moving Average) по последним 20 свечам;
	•	расчёта ATR (Average True Range) по методу Уайлдера (RMA) на основе 21 свечи (для TR нужен предыдущий close).

Что внутри
	•	fetch_okx_candles(inst_id: str, bar: str, limit: int = 21) -> dict
Запрашивает свечи на OKX и возвращает словарь вида {0: {...}, 1: {...}, ...} в хронологическом порядке (от старых к новым).
	•	calculate_sma(candles: dict, price_type: str = "close", length: int = 20) -> float
Считает SMA по выбранному типу цены (по умолчанию close) на последних length значениях.
	•	calculate_atr_rma(candles: dict, length: int = 20) -> float | None
Считает ATR по Уайлдеру. Для периода length требуется минимум length+1 свечей (в нашем примере — 21 свеча).

В __main__ приводится пример: запрашиваем 21 свечу ETH-USDT-SWAP на таймфрейме 1H, затем считаем SMA(20) и ATR(20).


Учтите, что на OKX можно получить 100 свечей за один запрос. Если нужно больше - используйте пагинацию.
