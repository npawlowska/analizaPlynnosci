import pandas as pd
import os

DATA_DIR = r"C:\Users\szamb\PycharmProjects\Plynnosc_Spolek_Gieldowych\data"

def get_companies():
    """Zwraca listę dostępnych spółek na podstawie plików CSV w folderze data."""
    files = os.listdir(DATA_DIR)
    companies = [f.split("_")[0].upper() for f in files if f.endswith(".csv")]
    return sorted(set(companies))  # Sortujemy i usuwamy duplikaty

def load_data_for_company_and_date(company, start_date, end_date):
    """Wczytuje dane spółki z pliku CSV i filtruje po dacie."""
    file_path = os.path.join(DATA_DIR, f"{company.lower()}_updated.csv")

    if not os.path.exists(file_path):
        print(f"❌ Brak pliku: {file_path}")
        return pd.DataFrame()  # Zwracamy pusty DataFrame, jeśli pliku nie ma

    df = pd.read_csv(file_path)

    # Zamiana nazw kolumn na małe litery (np. "Data" -> "data")
    df.columns = df.columns.str.strip().str.lower()

    # Upewniamy się, że kolumna 'data' istnieje
    if 'data' not in df.columns:
        print(f"❌ Kolumna 'data' nadal nie istnieje! Dostępne kolumny: {df.columns.tolist()}")
        return pd.DataFrame()

    # Konwersja 'data' na format daty
    df['data'] = pd.to_datetime(df['data'], errors='coerce')

    # Filtrowanie danych na podstawie zakresu dat
    df_filtered = df[(df['data'] >= start_date) & (df['data'] <= end_date)]

    return df_filtered


# TEST: Sprawdzenie czy działa
if __name__ == "__main__":
    print("✅ Lista dostępnych spółek:", get_companies())

    test_data = load_data_for_company_and_date("AGO", "2017-01-01", "2023-12-31")
    print("📌 Przykładowe dane spółki AGO:")
    print(test_data.head())
