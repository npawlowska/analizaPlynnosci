import pandas as pd

def filter_data_by_period(data, period):
    """
    Funkcja filtrująca dane w zależności od okresu.
    """
    # Konwertujemy dane do pandas DataFrame
    data_df = pd.DataFrame(data)
    if 'data' not in data_df.columns:
        raise KeyError("Kolumna 'data' nie istnieje w danych wejściowych: {}".format(data_df.columns))

    # Konwertujemy kolumnę 'data' na datetime
    data_df['data'] = pd.to_datetime(data_df['data'], errors='coerce')

    if period == "przed pandemią COVID-19 (styczeń 2017 - luty 2020)":
        start_date = pd.to_datetime("2017-01-01")
        end_date = pd.to_datetime("2020-02-28")
    elif period == "w czasie okresu pandemii COVID-19 (marzec 2020 - kwiecień 2023)":
        start_date = pd.to_datetime("2020-03-01")
        end_date = pd.to_datetime("2023-04-30")
    elif period == "cała próba statystyczna (styczeń 2017 - wrzesień 2024)":
        start_date = pd.to_datetime("2017-01-01")
        end_date = pd.to_datetime("2024-09-30")
    else:
        raise ValueError(f"Nieznany okres: {period}")

    # Debugowanie zakresu dat
    print(f"Debug - Zakres dat dla okresu '{period}': {start_date} - {end_date}")

    # Debugowanie danych przed filtrowaniem
    print(f"Debug - Liczba rekordów przed filtrowaniem: {len(data_df)}")
    print(data_df[['data']].drop_duplicates().sort_values(by='data').head(10))  # Wyświetl unikalne daty

    # Filtrujemy dane na podstawie okresu
    filtered_data = data_df[(data_df['data'] >= start_date) & (data_df['data'] <= end_date)]

    # Dodanie debugowania
    print(f"Okres: {period}")
    print(f"Data początkowa: {start_date}, Data końcowa: {end_date}")
    print(f"Liczba dni w okresie: {len(filtered_data)}")
    print(f"Przykładowe dane po filtrowaniu: {filtered_data.head()}")
    return filtered_data
