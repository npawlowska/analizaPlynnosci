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
    data['Return'] = (data['zamkniecie'] - data['zamkniecie'].shift(1)) / data['zamkniecie'].shift(1)
    data['Return'].fillna(0, inplace=True)  # Wypełnia wartość NaN (pierwszy dzień) zerem
    print("Debug - Dane po dodaniu 'Return':")
    print(data.head())
    return data

def calculate_relative_volume(data):
    """
    Oblicza Relative Volume (RV) na podstawie danych w formacie DataFrame.
    """
    if 'wolumen' not in data.columns or 'liczba_akcji' not in data.columns:
        raise ValueError("Kolumna 'wolumen' i 'liczba_akcji' musi znajdować się w danych wejściowych")

    data['wolumen'] = pd.to_numeric(data['wolumen'], errors='coerce')
    data['liczba_akcji'] = pd.to_numeric(data['liczba_akcji'], errors='coerce')

    print("Debug - Dane wejściowe do RV:")
    print(data[['wolumen', 'liczba_akcji']].head())

    # Sprawdzenie, czy liczba akcji jest poprawna
    if data['liczba_akcji'].isnull().any() or (data['liczba_akcji'] <= 0).any():
        raise ValueError("Kolumna 'liczba_akcji' zawiera nieprawidłowe wartości (null lub <= 0)")

    # Obliczenie RV
    data['RV'] = data['wolumen'] / data['liczba_akcji']
    print("Debug - RV obliczone dla poszczególnych dni:")
    print(data[['RV']].head())

    return data['RV']


def calculate_zero1(data):
    """
    Oblicza ZERO1 jako procent dni z zerowym wolumenem.
    """
    print("Debug - Dane wejściowe do ZERO1:")
    print(data[['data', 'Return']].head())

    if 'Return' not in data.columns:
        raise ValueError("Kolumna 'Return' musi znajdować się w danych wejściowych")

    if data['Return'].isnull().all():
        raise ValueError("Wszystkie wartości w kolumnie 'Return' są puste (NaN)")

    zero_return_days = len(data[data['Return'].abs() < 1e-8])

    # Całkowita liczba dni
    total_days = len(data)
    print(f"Debug - ZERO1: zero_return_days = {zero_return_days}, total_days = {total_days}")

    # Obliczanie procentu dni z zerową stopą zwrotu
    return (zero_return_days / total_days) if total_days > 0 else 0

def calculate_zero2(data):
    """
        Oblicza ZERO2 jako procent dni z zerową stopą zwrotu (Return == 0) i dodatnim wolumenem (wolumen > 0).
        """
    print("Debug - Dane wejściowe do ZERO2:")
    print(data[['data', 'Return', 'wolumen']].head())

    # Filtrujemy dane, gdzie Return == 0 i wolumen > 0
    filtered_data = data[(data['Return'] == 0) & (data['wolumen'] > 0)]
    print("Debug - Filtrowane dane dla ZERO2 (Return == 0 i wolumen > 0):")
    print(filtered_data[['data', 'Return', 'wolumen']])

    # Liczba dni spełniających warunki
    zero_return_positive_volume_days = len(filtered_data)

    # Całkowita liczba dni
    total_days = len(data)
    print(
        f"Debug - ZERO2: zero_return_positive_volume_days = {zero_return_positive_volume_days}, total_days = {total_days}")

    # Obliczanie procentu dni spełniających warunki
    zero2 = (zero_return_positive_volume_days / total_days) if total_days > 0 else 0
    print(f"Debug - Wynik ZERO2: {zero2}")
    return zero2

def calculate_liquidity(data):
    """
    Oblicza wskaźniki płynności na podstawie danych.
    """
    # Sprawdzenie, czy dane są DataFrame
    if isinstance(data, list):
        data = pd.DataFrame(data)

    # Sprawdzenie, czy wymagane kolumny istnieły
    required_columns = {'data', 'zamkniecie', 'wolumen', 'spolka', 'liczba_akcji'}
    if not required_columns.issubset(data.columns):
       raise ValueError(f"Dane muszą zawierać kolumny: {required_columns}")

    print("Debug - Dane wejściowe do obliczeń:")
    print(data.head())  # Debugowanie: wyświetlenie danych wejściowych

    # Dodajemy kolumnę 'Return' na podstawie zmiany ceny zamknięcia
    data = add_returns_to_data(data)

    # Obliczamy wskaźniki płynności
    rv_series = calculate_relative_volume(data)  # Relative Volume jako seria
    rv = rv_series.mean()  # Agregacja: średnia RV dla całego okresu
    print(f"Debug - RV (średnia): {rv}")  # Sprawdzenie RV

    zero1 = calculate_zero1(data)  # ZERO1
    print(f"Debug - ZERO1: {zero1}")
    zero2 = calculate_zero2(data)  # ZERO2
    print(f"Debug - Wynik ZERO2: {zero2}")

    # Debugowanie wyników końcowych
    print(f"Final Results - RV: {rv}, ZERO1: {zero1}, ZERO2: {zero2}")

    # Zwracanie wyników
    return {
        "Relative Volume (RV)": rv,
        "ZERO1": zero1,
        "ZERO2": zero2,
    }

