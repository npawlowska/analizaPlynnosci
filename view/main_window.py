import tkinter as tk
from view.graphs import generate_comparison_chart
from database.database import load_data_for_company_and_date, get_companies
from controller.calculate_liquidity import calculate_liquidity
from controller.data_controller import filter_data_by_period


# Kolorystyka aplikacji
BACKGROUND_COLOR = "#D8E2DC"
BUTTON_COLOR = "#FEC89A"
BUTTON_HOVER_COLOR = "#FFE5D9"
TEXT_COLOR = "#333333"
TITLE_COLOR = "#6B4F4F"

# Czcionki
FONT_MAIN = ("Poppins", 14)
FONT_SMALLER = ("Poppins", 17)
FONT_TITLE = ("Poppins", 22, "bold")

# Funkcja tworzenia głównego okna aplikacji
def create_main_window():
    root = tk.Tk()
    root.title("Aplikacja wspomagająca analizy płynności")
    root.geometry("900x700")
    root.configure(bg=BACKGROUND_COLOR)

    def show_calculation_menu():
        """
        Wyświetla menu wyboru opcji obliczeń i wykresów.
        """
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text="Aplikacja wspomagająca analizy płynności spółek giełdowych", font=FONT_TITLE, fg=TITLE_COLOR, bg=BACKGROUND_COLOR).pack(pady=30)
        tk.Label(root, text="Witaj!\n\nWybierz działanie", font=FONT_SMALLER, fg=TITLE_COLOR, bg=BACKGROUND_COLOR).pack(pady=20)
        tk.Button(root, text="Przejdź do obliczeń", font=FONT_MAIN, bg="#FEC89A", activebackground=BUTTON_HOVER_COLOR, command=show_comparison_menu).pack(pady=10)
        tk.Button(root, text="Wyjście z aplikacji", font=FONT_MAIN, bg="#FFD7BA", activebackground=BUTTON_HOVER_COLOR, command=root.quit).pack(pady=10)

    def show_comparison_menu():
        """
        Wyświetla ekran wyboru między porównaniem wskaźników między spółkami i wszystkimi wskaźnikami w jednej spółce.
        """
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text="Wybierz opcję porównania", font=FONT_TITLE, fg=TITLE_COLOR, bg=BACKGROUND_COLOR).pack(pady=20)
        tk.Button(root, text="Porównaj wskaźnik między spółkami", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=show_company_comparison_screen).pack(pady=10)
        tk.Button(root, text="Porównaj wszystkie wskaźniki w jednej spółce", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=show_all_metrics_comparison_screen).pack(pady=10)
        tk.Button(root, text="Powrót do menu głównego", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=show_calculation_menu).pack(pady=10)

    def show_company_comparison_screen():
        """
        Wyświetla ekran porównania jednego wskaźnika między spółkami dla dwóch okresów.
        """
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text="Porównaj wskaźniki między spółkami", font=FONT_TITLE, fg=TITLE_COLOR, bg=BACKGROUND_COLOR).pack(pady=20)

        companies_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        companies_frame.pack(pady=10)

        company_vars = []
        periods = ["przed COVID", "w trakcie COVID", "po COVID", "cały okres"]
        metric_var = tk.StringVar(root, value="Relative Volume (RV)")
        period1_var = tk.StringVar(root, value=periods[0])
        period2_var = tk.StringVar(root, value=periods[1])

        def add_company_row():
            """
            Dodaje nowy wiersz wyboru spółki.
            """
            frame = tk.Frame(companies_frame, bg=BACKGROUND_COLOR)
            frame.pack(pady=5)

            company_var = tk.StringVar(root, value=get_companies()[0])
            tk.Label(frame, text="Spółka:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT)

            # Tworzenie OptionMenu z kolorami
            company_menu = tk.OptionMenu(frame, company_var, *get_companies())
            company_menu.config(bg="#FEC89A", fg="#333333", font=("Poppins", 12))  # Kolor przycisku
            company_menu["menu"].config(bg="#ECE4DB", fg="#333333")  # Kolor rozwijanego menu
            company_menu.pack(side=tk.LEFT)

            company_vars.append(company_var)

        # Dodajemy pierwszy wiersz wyboru spółki
        add_company_row()
        tk.Button(root, text="Dodaj spółkę", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR,
                  command=add_company_row).pack(pady=10)

        # Frame dla wyboru okresów
        period_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        period_frame.pack(pady=10)

        tk.Label(period_frame, text="Okres 1:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT,
                                                                                                         padx=5)

        # OptionMenu dla Okres 1
        period1_menu = tk.OptionMenu(period_frame, period1_var, *periods)
        period1_menu.config(bg="#FEC89A", fg="#333333", font=("Poppins", 12))  # Kolor przycisku
        period1_menu["menu"].config(bg="#ECE4DB", fg="#333333")  # Kolor rozwijanego menu
        period1_menu.pack(side=tk.LEFT, padx=5)

        tk.Label(period_frame, text="Okres 2:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT,
                                                                                                         padx=5)

        # OptionMenu dla Okres 2
        period2_menu = tk.OptionMenu(period_frame, period2_var, *periods)
        period2_menu.config(bg="#FEC89A", fg="#333333", font=("Poppins", 12))  # Kolor przycisku
        period2_menu["menu"].config(bg="#ECE4DB", fg="#333333")  # Kolor rozwijanego menu
        period2_menu.pack(side=tk.LEFT, padx=5)

        # Frame dla wyboru wskaźnika
        metric_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        metric_frame.pack(pady=10)

        # Definicja dostępnych wskaźników
        metrics = ["Relative Volume (RV)", "Illiquidity Measure (ILLIQ)", "ZERO1", "ZERO2"]

        tk.Label(metric_frame, text="Wskaźnik:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT,
                                                                                                          padx=5)

        # OptionMenu dla wyboru wskaźnika
        metric_menu = tk.OptionMenu(metric_frame, metric_var, *metrics)
        metric_menu.config(bg="#FEC89A", fg="#333333", font=("Poppins", 12))  # Kolor przycisku
        metric_menu["menu"].config(bg="#ECE4DB", fg="#333333")  # Kolor rozwijanego menu
        metric_menu.pack(side=tk.LEFT, padx=5)

        def generate_company_comparison_chart():
            selected_companies = [var.get() for var in company_vars]
            period1 = period1_var.get()
            period2 = period2_var.get()
            selected_metric = metric_var.get()

            results = {}
            for company in selected_companies:
                raw_data = load_data_for_company_and_date(company, "2017-01-01", "2024-09-30")
                data1 = filter_data_by_period(raw_data, period1)
                data2 = filter_data_by_period(raw_data, period2)

                if not data1.empty and not data2.empty:
                    metrics1 = calculate_liquidity(data1)
                    metrics2 = calculate_liquidity(data2)
                    results[company] = {
                        period1: metrics1.get(selected_metric, 0.0),
                        period2: metrics2.get(selected_metric, 0.0),
                    }

            if results:
                generate_comparison_chart(root, results, [period1, period2], background_color=BACKGROUND_COLOR)

        tk.Button(root, text="Generuj wykres", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=generate_company_comparison_chart).pack(pady=10)
        tk.Button(root, text="Powrót", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=show_comparison_menu).pack(pady=10)

    def show_all_metrics_comparison_screen():
        """
        Wyświetla ekran porównania wszystkich wskaźników w jednej spółce dla dwóch okresów.
        """
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text="Porównaj wszystkie wskaźniki w jednej spółce", font=FONT_TITLE, fg=TITLE_COLOR, bg=BACKGROUND_COLOR).pack(pady=20)

        company_var = tk.StringVar(root, value=get_companies()[0])
        periods = ["przed COVID", "w trakcie COVID", "po COVID", "cały okres"]
        period1_var = tk.StringVar(root, value=periods[0])
        period2_var = tk.StringVar(root, value=periods[1])

        company_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        company_frame.pack(pady=10)

        tk.Label(company_frame, text="Spółka:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT,padx=5)
        company_menu = tk.OptionMenu(company_frame, company_var, *get_companies())
        company_menu.config(bg="#FEC89A", fg="#333333", font=("Poppins", 12))  # Kolor przycisku
        company_menu["menu"].config(bg="#ECE4DB", fg="#333333")  # Kolor rozwijanego menu
        company_menu.pack(side=tk.LEFT, padx=5)

        period_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        period_frame.pack(pady=10)

        tk.Label(period_frame, text="Okres 1:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=5)
        period1_menu = tk.OptionMenu(period_frame, period1_var, *periods)
        period1_menu.config(bg="#FEC89A", fg="#333333", font=("Poppins", 12))  # Kolor przycisku
        period1_menu["menu"].config(bg="#ECE4DB", fg="#333333")  # Kolor rozwijanego menu
        period1_menu.pack(side=tk.LEFT, padx=5)

        tk.Label(period_frame, text="Okres 2:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=5)
        period2_menu = tk.OptionMenu(period_frame, period2_var, *periods)
        period2_menu.config(bg="#FEC89A", fg="#333333", font=("Poppins", 12))  # Kolor przycisku
        period2_menu["menu"].config(bg="#ECE4DB", fg="#333333")  # Kolor rozwijanego menu
        period2_menu.pack(side=tk.LEFT, padx=5)

        def generate_all_metrics_chart():
            selected_company = company_var.get()
            period1 = period1_var.get()
            period2 = period2_var.get()

            raw_data = load_data_for_company_and_date(selected_company, "2017-01-01", "2024-09-30")
            data1 = filter_data_by_period(raw_data, period1)
            data2 = filter_data_by_period(raw_data, period2)

            if not data1.empty and not data2.empty:
                metrics1 = calculate_liquidity(data1)
                metrics2 = calculate_liquidity(data2)

                # Przygotowanie danych do wykresu
                results = {metric: {period1: metrics1[metric], period2: metrics2[metric]} for metric in metrics1.keys()}
                generate_comparison_chart(root, results, [period1, period2], background_color=BACKGROUND_COLOR)

        tk.Button(root, text="Generuj wykres", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=generate_all_metrics_chart).pack(pady=10)
        tk.Button(root, text="Powrót", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=show_comparison_menu).pack(pady=10)

    show_calculation_menu()
    root.mainloop()
