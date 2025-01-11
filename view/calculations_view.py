import tkinter as tk
from tkinter import filedialog
import pandas as pd

# Stałe dla stylu
FONT_MAIN = ("Poppins", 12)
FONT_TITLE = ("Poppins", 16, "bold")
TITLE_COLOR = "#6B4F4F"
TEXT_COLOR = "#333333"
BACKGROUND_COLOR = "#D8E2DC"
HEADER_COLOR = "#FFD7BA"

def save_results_to_excel(results):
    """
    Zapisuje wyniki obliczeń do pliku Excel (.xlsx).
    """
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Pliki Excel", "*.xlsx")],
        title="Zapisz wyniki jako..."
    )
    if not file_path:
        return  # Użytkownik anulował zapis

    # Konwersja wyników do DataFrame
    data = []
    for label, periods in results.items():
        row = {"Wskaźnik/Spółka": label}
        row.update(periods)
        data.append(row)

    df = pd.DataFrame(data)

    # Zapis do pliku Excel
    try:
        df.to_excel(file_path, index=False, engine="openpyxl")
        print(f"Wyniki zapisano do pliku: {file_path}")
    except Exception as e:
        print(f"Błąd podczas zapisu do Excela: {e}")
def save_results_to_txt(results):
    """
    Zapisuje wyniki obliczeń do pliku .txt.
    """
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Pliki tekstowe", "*.txt")],
        title="Zapisz wyniki jako..."
    )
    if not file_path:
        return  # Użytkownik anulował zapis

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("Wyniki obliczeń:\n\n")
        for label, periods in results.items():
            file.write(f"Spółka/Wskaźnik: {label}\n")
            for period, value in periods.items():
                file.write(f"  {period}: {value:.2f}\n")
            file.write("----------------------\n")
    print(f"Wyniki zapisano do pliku: {file_path}")

def show_calculations(root, results):
    """
    Wyświetla wyniki obliczeń w nowym oknie i umożliwia ich eksport do pliku .txt.
    """
    calculations_window = tk.Toplevel(root)
    calculations_window.title("Wyniki obliczeń")
    calculations_window.geometry("600x400")
    calculations_window.configure(bg=BACKGROUND_COLOR)

    tk.Label(
        calculations_window,
        text="Wyniki obliczeń",
        font=FONT_TITLE,
        fg=TITLE_COLOR,
        bg=BACKGROUND_COLOR
    ).pack(pady=10)

    frame = tk.Frame(calculations_window, bg="#D8E2DC")
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Nagłówki tabeli
    headers = ["Wskaźnik/Spółka"] + list(results[list(results.keys())[0]].keys())
    for col, header in enumerate(headers):
        tk.Label(
            frame,
            text=header,
            font=FONT_MAIN,
            bg=HEADER_COLOR,
            fg=TEXT_COLOR,
            relief="ridge",
            padx=5,
            pady=5,
        ).grid(row=0, column=col, sticky="nsew")

    # Dane wynikowe
    for row, (label, periods) in enumerate(results.items(), start=1):
        tk.Label(
            frame,
            text=label,
            font=FONT_MAIN,
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            relief="ridge",
            padx=5,
            pady=5,
        ).grid(row=row, column=0, sticky="nsew")
        for col, (period, value) in enumerate(periods.items(), start=1):
            tk.Label(
                frame,
                text=f"{value:.7f}",
                font=FONT_MAIN,
                bg="#FFFFFF",
                fg=TEXT_COLOR,
                relief="ridge",
                padx=5,
                pady=5,
            ).grid(row=row, column=col, sticky="nsew")

    # Przycisk zapisu do pliku .txt
    tk.Button(
        calculations_window,
        text="Eksportuj do .txt",
        font=FONT_MAIN,
        bg=HEADER_COLOR,
        activebackground="#FFB6C1",
        command=lambda: save_results_to_txt(results)
    ).pack(pady=10)

    # Przycisk zapisu do pliku .xlsx
    tk.Button(
        calculations_window,
        text="Eksportuj do Excela",
        font=FONT_MAIN,
        bg="#FFD7BA",
        activebackground="#FFB6C1",
        command=lambda: save_results_to_excel(results)
    ).pack(pady=5)

    # Przycisk zamknięcia
    tk.Button(
        calculations_window,
        text="Zamknij",
        font=FONT_MAIN,
        bg=HEADER_COLOR,
        activebackground="#FFB6C1",
        command=calculations_window.destroy
    ).pack(pady=10)
