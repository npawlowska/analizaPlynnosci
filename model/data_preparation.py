import pandas as pd


def prepare_data(raw_data):
    data = pd.DataFrame(raw_data)
    data['Return'] = data['zamkniecie'].pct_change()
    data['Is_Zero_Volume'] = data['wolumen'] == 0
    data['Is_Zero_Close_Change'] = data['zamkniecie'].diff() == 0
    return data


def validate_data(data):
    required_columns = {'zamkniecie', 'wolumen', 'data'}
    return required_columns.issubset(data.columns)


def summarize_data(data):
    return {
        "Liczba dni": len(data),
        "Średni wolumen": data['wolumen'].mean()
    }