import mysql.connector
from mysql.connector import Error

print("⚡ Skrypt database.py został uruchomiony!")

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1", # Adres serwera bazy danych
            port='3306',
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

