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

    if period == "przed COVID":
        start_date = pd.to_datetime("2017-01-02")
        end_date = pd.to_datetime("2020-02-28")
    elif period == "w trakcie COVID":
        start_date = pd.to_datetime("2020-03-02")
        end_date = pd.to_datetime("2023-04-30")
    elif period == "po COVID":
        start_date = pd.to_datetime("2023-05-04")
        end_date = pd.to_datetime("2024-09-30")
    else:  # całkowity okres
        start_date = pd.to_datetime("2017-01-02")
        end_date = pd.to_datetime("2024-09-30")

    # Debugowanie zakresu dat
    print(f"Debug - Zakres dat dla okresu '{period}': {start_date} - {end_date}")

    # Debugowanie danych przed filtrowaniem
    print(f"Debug - Liczba rekordów przed filtrowaniem: {len(data_df)}")
    print(data_df[['data']].drop_duplicates().sort_values(by='data').head(10))  # Wyświetl unikalne daty

    # Filtrujemy dane na podstawie okresu
    filtered_data = data_df[(data_df['data'] >= start_date) & (data_df['data'] <= end_date)]

    # Debugowanie wyników filtrowania
    print(f"Debug - Liczba rekordów po filtrowaniu dla okresu '{period}': {len(filtered_data)}")
    print(filtered_data[['data']].drop_duplicates().sort_values(by='data').head(10))  # Wyświetl unikalne daty

    print(f"Debug - Filtrowane dane przekazywane dalej dla okresu '{period}': {filtered_data.head(10)}")
    print(f"Debug - Filtrowane dane: {filtered_data.head(10)}")
    print(f"Debug - Final filtered data ready for processing: {filtered_data.head(10)}")
    print(f"Debug - Filtered data being returned: {filtered_data.head(10)}")
    print(f"Debug - Filtered data ready to use: {filtered_data.head(10)}")
    print(f"Debug - Filtered data (final return):{filtered_data.head(10)}")
    print("Debug - Filtered data (final return):")
    print(filtered_data.head(10))
    print("Debug - Filtered data (final return):")
    print(filtered_data.head(10))
    print(f"Debug - Filtered data before returning (rows: {len(filtered_data)}):")
    print(filtered_data.head(10))
    return filtered_data
