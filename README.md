
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

⸻

Требования
	•	Python 3.10+
	•	Библиотека: requests

Установка зависимостей:

pip install requests


⸻

Быстрый старт

Запуск из папки с файлом:

python buy_indicator.py

Ожидаемый вывод в консоль:

SMA 20: <число>
ATR 20: <число>


⸻

Параметры запроса свечей

Функция:

candles = fetch_okx_candles(
    inst_id="ETH-USDT-SWAP",  # инструмент
    bar="1H",                 # таймфрейм (например: 1m, 5m, 15m, 1H, 4H, 1D)
    limit=21                  # количество свечей (для ATR(20) нужно минимум 21)
)

Важно: для ATR(20) нужно 21 свеча.
SMA(20) считается по последним 20 свечам из этих данных.

⸻

Формат данных свечи

Каждая свеча приводится к словарю:

{
  "ts":   "<timestamp_ms>",  // метка времени в миллисекундах (строка из OKX ответа)
  "open": "<price_open>",
  "high": "<price_high>",
  "low":  "<price_low>",
  "close":"<price_close>",
  "volume":"<base_volume>"
}

Скрипт уже разворачивает массив OKX так, чтобы индексы 0…N шли от старых к новым.

⸻

Примеры использования функций

Импорт в другом модуле:

from buy_indicator import fetch_okx_candles, calculate_sma, calculate_atr_rma

candles = fetch_okx_candles("ETH-USDT-SWAP", "1H", 21)

sma20 = calculate_sma(candles, price_type="close", length=20)
atr20 = calculate_atr_rma(candles, length=20)

print("SMA(20):", sma20)
print("ATR(20):", atr20)

Смена инструмента и ТФ:

candles = fetch_okx_candles("BTC-USDT-SWAP", "4H", 21)


⸻

Частые ошибки и проверки
	•	Недостаточно свечей для ATR:
calculate_atr_rma вернёт None, если len(candles) < length + 1. Убедитесь, что limit >= length + 1.
	•	Сеть/доступ к API:
При проблеме с запросом requests.get(...).raise_for_status() выбросит исключение. Проверьте интернет/прокси/частоту запросов (rate limits OKX).
	•	Типы данных:
Значения цен и объёма приходят строками из API. В расчётах они приводятся к float внутри функций.

⸻

Заметки
	•	Используется эндпоинт history-candles (исторические свечи). Он возвращает массив от новых к старым, скрипт переупорядочивает его в хронологический вид (от старых к новым).
	•	Для других метрик добавляйте новые функции по аналогии, используя словарь candles.

⸻

Лицензия

Свободное использование в учебных и исследовательских целях. Если планируете коммерческое применение — проверьте условия и лимиты API OKX на вашей стороне.
