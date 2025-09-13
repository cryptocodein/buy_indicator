import requests


def fetch_okx_candles(inst_id: str, bar: str, limit: int = 21) -> dict:
    OKX_BASE = "https://www.okx.com"  # Базовый URL OKX
    CANDLES_EP = "/api/v5/market/history-candles"  # Эндпоинт исторических свечей
    url = OKX_BASE + CANDLES_EP
    params = {
        "instId": inst_id,  # Идентификатор инструмента
        "bar": bar,         # Таймфрейм
        "limit": str(limit) # Количество свечей
    }
    # Отправляем GET-запрос на сервер OKX
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    raw_data = resp.json().get("data", [])

    candles = {}
    # Переворачиваем массив, чтобы свечи шли от старых к новым
    for i, c in enumerate(reversed(raw_data)):
        candles[i] = {
            "ts": c[0],      # Временная метка
            "open": c[1],    # Цена открытия
            "high": c[2],    # Максимальная цена
            "low": c[3],     # Минимальная цена
            "close": c[4],   # Цена закрытия
            "volume": c[5]   # Объём
        }
    return candles


def calculate_sma(candles: dict, price_type: str = "close", length: int = 20) -> float:
    # Собираем значения выбранной цены из всех свечей
    prices = [float(c[price_type]) for c in candles.values() if price_type in c]
    # Оставляем только последние length значений
    recent_prices = prices[-length:]
    # Считаем среднее арифметическое
    sma = sum(recent_prices) / length
    return sma


def calculate_atr_rma(candles: dict, length: int = 20) -> float | None:
    # Сортируем свечи по времени (от старых к новым)
    ordered = sorted(candles.values(), key=lambda c: int(c["ts"]))
    # Проверяем, хватает ли свечей для расчёта ATR
    if len(ordered) < length + 1:
        return None
    # Берём только последние length+1 свечей (для TR нужно n+1 свеча)
    ordered = ordered[-(length + 1):]

    trs: list[float] = []
    # Считаем истинный диапазон (True Range, TR) для каждой свечи, начиная со второй
    for i in range(1, len(ordered)):
        high = float(ordered[i]["high"])         
        low = float(ordered[i]["low"])           
        prev_close = float(ordered[i - 1]["close"]) # Закрытие предыдущей свечи
        # TR — максимум из трех вариантов
        tr = max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close)
        )
        trs.append(tr)

    # Первое значение ATR — простое среднее TR за length периодов
    atr = sum(trs[:length]) / length
    # Дальнейшее сглаживание по методу Уайлдера (RMA)
    for tr in trs[length:]:
        atr = (atr * (length - 1) + tr) / length

    return atr


# Пример использования: загружаем 21 свечу, считаем SMA и ATR
if __name__ == "__main__":
    candles = fetch_okx_candles("ETH-USDT-SWAP", "1H", 21)
    sma_20 = calculate_sma(candles, price_type="close", length=20)
    atr_20 = calculate_atr_rma(candles, length=20)
    print(f"SMA 20: {sma_20}")
    print(f"ATR 20: {atr_20}")
