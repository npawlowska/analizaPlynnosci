import pandas as pd

def calculate_zero1(data):
    """
    Oblicza ZERO1 jako procent dni z zerową stopą zwrotu.
    """
    print("Debug - Dane wejściowe do ZERO1:")
    print(data[['data', 'stopa_zwrotu']].head())

    if 'stopa_zwrotu' not in data.columns:
        raise ValueError("Kolumna 'stopa_zwrotu' musi znajdować się w danych wejściowych")

    if data['stopa_zwrotu'].isnull().all():
        raise ValueError("Wszystkie wartości w kolumnie 'stopa_zwrotu' są puste (NaN)")

    zero_return_days = len(data[data['stopa_zwrotu'].abs() < 1e-8])

    # Całkowita liczba dni
    total_days = len(data)
    print(f"Debug - ZERO1: zero_return_days = {zero_return_days}, total_days = {total_days}")

    # Obliczanie procentu dni z zerową stopą zwrotu
    return (zero_return_days / total_days) if total_days > 0 else 0


def calculate_zero2(data):
    """
    Oblicza ZERO2 jako procent dni z zerową stopą zwrotu (stopa_zwrotu == 0) i dodatnim wolumenem.
    """
    print("Debug - Dane wejściowe do ZERO2:")
    print(data[['data', 'stopa_zwrotu', 'wolumen']].head())

    # Filtrujemy dane, gdzie stopa_zwrotu == 0 i wolumen > 0
    filtered_data = data[(data['stopa_zwrotu'] == 0) & (data['wolumen'] > 0)]
    print("Debug - Filtrowane dane dla ZERO2 (stopa_zwrotu == 0 i wolumen > 0):")
    print(filtered_data[['data', 'stopa_zwrotu', 'wolumen']])

    # Liczba dni spełniających warunki
    zero_return_positive_volume_days = len(filtered_data)

    # Całkowita liczba dni
    total_days = len(data)
    print(f"Debug - ZERO2: zero_return_positive_volume_days = {zero_return_positive_volume_days}, total_days = {total_days}")

    # Obliczanie procentu dni spełniających warunki
    zero2 = (zero_return_positive_volume_days / total_days) if total_days > 0 else 0
    print(f"Debug - Wynik ZERO2: {zero2}")
    return zero2


def calculate_liquidity(data):
    """
    Oblicza wskaźniki płynności na podstawie danych.
    """
    # Sprawdzenie, czy dane są DataFrame
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Dane wejściowe muszą być w formacie pandas.DataFrame")

    # Sprawdzenie, czy wymagane kolumny istnieją
    required_columns = {'data', 'stopa_zwrotu', 'wolumen', 'symbol', 'liczba_akcji'}
    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(f"Dane muszą zawierać następujące kolumny: {missing_columns}")

    print("Debug - Dane wejściowe do obliczeń:")
    print(data.head())  # Debugowanie: wyświetlenie danych wejściowych

    # Obliczamy wskaźniki płynności
    rv_series = data['wolumen'] / data['liczba_akcji']  # Relative Volume jako seria
    rv = rv_series.mean() if not rv_series.empty else 0  # Średnia RV (lub 0, jeśli brak danych)
    print(f"Debug - RV (średnia): {rv}")

    zero1 = calculate_zero1(data)  # ZERO1
    print(f"Debug - ZERO1: {zero1}")

    zero2 = calculate_zero2(data)  # ZERO2
    print(f"Debug - ZERO2: {zero2}")

    # Debugowanie wyników końcowych
    print(f"Final Results - RV: {rv}, ZERO1: {zero1}, ZERO2: {zero2}")

    # Zwracanie wyników
    return {
        "Relative Volume (RV)": rv,
        "ZERO1": zero1,
        "ZERO2": zero2,
    }
