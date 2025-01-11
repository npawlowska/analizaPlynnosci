import mysql.connector
from mysql.connector import Error


def get_db_connection():
    """
    Funkcja łącząca się z bazą danych MySQL.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",          # Adres serwera bazy danych
            user="root",               # Nazwa użytkownika MySQL
            password="admin",          # Hasło użytkownika MySQL
            database="spolka_baza"     # Nazwa bazy danych
        )
        if conn.is_connected():
            print("Połączono z bazą danych.")
            return conn
    except Error as e:
        print(f"Błąd podczas połączenia z MySQL: {e}")
        return None


def load_data_for_company_and_date(company, start_date, end_date):
    """
    Pobiera dane dla wybranej spółki i zakresu dat.

    Args:
        company (str): Nazwa spółki.
        start_date (str): Data początkowa w formacie YYYY-MM-DD.
        end_date (str): Data końcowa w formacie YYYY-MM-DD.

    Returns:
        list: Lista słowników z wynikami zapytania.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT data, symbol, zamkniecie, wolumen, liczba_akcji, stopa_zwrotu
                FROM akcje
                WHERE symbol = %s AND data BETWEEN %s AND %s
            """
            cursor.execute(query, (company, start_date, end_date))
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Błąd podczas pobierania danych: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    else:
        print("Brak połączenia z bazą danych.")
        return []


def get_companies():
    """
    Pobiera listę unikalnych nazw spółek z bazy danych.

    Returns:
        list: Lista nazw spółek (str).
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT DISTINCT symbol FROM akcje"
            cursor.execute(query)
            result = [row[0] for row in cursor.fetchall() if row[0] is not None]
            return result
        except Error as e:
            print(f"Błąd podczas wykonywania zapytania: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    else:
        print("Brak połączenia z bazą danych.")
        return []


if __name__ == "__main__":
    # Test połączenia z bazą
    conn = get_db_connection()
    if conn:
        print("Test połączenia: Sukces!")
    else:
        print("Test połączenia: Nie udało się połączyć.")

    # Test pobierania spółek
    companies = get_companies()
    print(f"Lista spółek: {companies}")

