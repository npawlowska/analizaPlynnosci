import pandas as pd

def add_returns_to_data(data):
    """
    Dodaje kolumnę 'Return' na podstawie zmiany ceny zamknięcia.
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Dane wejściowe muszą być w formacie pandas.DataFrame")

    if 'zamkniecie' not in data.columns:
        raise ValueError("Kolumna 'zamkniecie' musi znajdować się w danych wejściowych")

    # Konwersja kolumny 'zamkniecie' na float
    data['zamkniecie'] = pd.to_numeric(data['zamkniecie'], errors='coerce')

    # Obliczanie procentowej zmiany cen zamknięcia
    data['Return'] = data['zamkniecie'].pct_change()
    data['Return'].fillna(0, inplace=True)  # Wypełnia wartość NaN (pierwszy dzień) zerem
    return data


def calculate_relative_volume(data):
    """
    Oblicza Relative Volume (RV) na podstawie danych w formacie DataFrame.
    """
    if 'wolumen' not in data.columns:
        raise ValueError("Kolumna 'wolumen' musi znajdować się w danych wejściowych")

    # Konwersja kolumny 'wolumen' na float
    data['wolumen'] = pd.to_numeric(data['wolumen'], errors='coerce')

    # Obliczanie średniego wolumenu
    avg_volume = data['wolumen'].mean()
    if avg_volume == 0:
        return 0

    relative_volumes = data['wolumen'] / avg_volume
    return relative_volumes.mean()


def calculate_illiquidity(data):
    """
    Oblicza Illiquidity Measure (ILLIQ).
    """
    valid_data = data[data['wolumen'] > 0]  # Filtrowanie dni z zerowym wolumenem

    if valid_data.empty:
        return 0  # Brak danych do obliczeń

    # Konwersja kolumn do typu float
    valid_data['Return'] = pd.to_numeric(valid_data['Return'], errors='coerce')
    valid_data['wolumen'] = pd.to_numeric(valid_data['wolumen'], errors='coerce')

    illiq_values = valid_data['Return'].abs() / valid_data['wolumen']
    return illiq_values.mean() * 1e6  # Normalizacja przez mnożenie przez 1e6


def calculate_zero1(data):
    """
    Oblicza ZERO1 jako procent dni z zerowym wolumenem.
    """
    zero_volume_days = len(data[data['wolumen'] == 0])
    total_days = len(data)
    return (zero_volume_days / total_days) * 100 if total_days > 0 else 0


def calculate_zero2(data):
    """
    Oblicza ZERO2 jako procent dni z zerową zmianą cen zamknięcia.
    """
    zero_return_days = len(data[data['Return'] == 0])
    total_days = len(data)
    return (zero_return_days / total_days) * 100 if total_days > 0 else 0


def calculate_liquidity(data):
    """
    Oblicza wskaźniki płynności na podstawie danych.
    """
    # Sprawdzenie, czy dane są DataFrame
    if isinstance(data, list):
        data = pd.DataFrame(data)

    # Sprawdzenie, czy wymagane kolumny istnieją
    required_columns = {'data', 'zamkniecie', 'wolumen'}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Dane muszą zawierać kolumny: {required_columns}")

    print("Dane wejściowe do obliczeń:")
    print(data.head())  # Debugowanie: wyświetlenie danych wejściowych

    # Dodajemy kolumnę 'Return' na podstawie zmiany ceny zamknięcia
    data = add_returns_to_data(data)

    # Obliczamy wskaźniki płynności
    rv = calculate_relative_volume(data)  # Relative Volume
    illiq = calculate_illiquidity(data)  # Illiquidity Measure
    zero1 = calculate_zero1(data)  # ZERO1
    zero2 = calculate_zero2(data)  # ZERO2

    # Debugowanie wyników końcowych
    print(f"Final Results - RV: {rv}, ILLIQ: {illiq}, ZERO1: {zero1}, ZERO2: {zero2}")

    # Zwracanie wyników
    return {
        "Relative Volume (RV)": rv,
        "Illiquidity Measure (ILLIQ)": illiq,
        "ZERO1": zero1,
        "ZERO2": zero2,
    }