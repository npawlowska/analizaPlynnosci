import pandas as pd


def filter_data_by_period(data, period):
    """
    Funkcja filtrująca dane w zależności od okresu.
    """
    # Konwertujemy dane do pandas DataFrame
    data_df = pd.DataFrame(data)

    # Konwertujemy kolumnę 'data' na datetime
    data_df['data'] = pd.to_datetime(data_df['data'])

    if period == "przed COVID":
        start_date = pd.to_datetime("2017-01-01")
        end_date = pd.to_datetime("2020-02-29")
    elif period == "w trakcie COVID":
        start_date = pd.to_datetime("2020-03-01")
        end_date = pd.to_datetime("2023-04-30")
    elif period == "po COVID":
        start_date = pd.to_datetime("2023-05-01")
        end_date = pd.to_datetime("2024-09-30")
    else:  # całkowity okres
        start_date = pd.to_datetime("2017-01-01")
        end_date = pd.to_datetime("2024-09-30")

    # Filtrujemy dane na podstawie okresu
    filtered_data = data_df[(data_df['data'] >= start_date) & (data_df['data'] <= end_date)]

    return filtered_data
