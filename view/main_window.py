import tkinter as tk
from view.graphs import generate_comparison_chart
from model.tests import load_data_for_company_and_date, get_companies
from controller.calculate_liquidity import calculate_liquidity
from controller.data_controller import filter_data_by_period

BACKGROUND_COLOR = "#D8E2DC"
BUTTON_COLOR = "#FEC89A"
BUTTON_HOVER_COLOR = "#FFE5D9"
TEXT_COLOR = "#333333"
TITLE_COLOR = "#6B4F4F"


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
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text="Aplikacja wspomagająca analizy płynności spółek giełdowych", font=FONT_TITLE, fg=TITLE_COLOR, bg=BACKGROUND_COLOR).pack(pady=30)
        tk.Label(root, text="Witaj!\n\nWybierz działanie", font=FONT_SMALLER, fg=TITLE_COLOR, bg=BACKGROUND_COLOR).pack(pady=20)
        tk.Button(root, text="Przejdź do obliczeń", font=FONT_MAIN, bg="#FEC89A", activebackground=BUTTON_HOVER_COLOR, command=show_comparison_menu).pack(pady=10)
        tk.Button(root, text="Wyjście z aplikacji", font=FONT_MAIN, bg="#FFD7BA", activebackground=BUTTON_HOVER_COLOR, command=root.quit).pack(pady=10)

    def show_comparison_menu():
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text="Wybierz opcję porównania", font=FONT_TITLE, fg=TITLE_COLOR, bg=BACKGROUND_COLOR).pack(pady=20)
        tk.Button(root, text="Porównaj wskaźnik między spółkami", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=show_company_comparison_screen).pack(pady=10)
        tk.Button(root, text="Porównaj wskaźniki dla jednej spółki", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=show_all_metrics_comparison_screen).pack(pady=10)
        tk.Button(root, text="Powrót do menu głównego", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=show_calculation_menu).pack(pady=10)

    def show_company_comparison_screen():
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text="Porównaj wskaźniki między spółkami", font=FONT_TITLE, fg=TITLE_COLOR, bg=BACKGROUND_COLOR).pack(pady=20)

        companies_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        companies_frame.pack(pady=10)

        company_vars = []
        periods = ["przed pandemią COVID-19 (styczeń 2017 - luty 2020)", "w czasie okresu pandemii COVID-19 (marzec 2020 - kwiecień 2023)", "cała próba statystyczna (styczeń 2017 - wrzesień 2024)"]
        metric_var = tk.StringVar(root, value="Relative Volume (RV)")
        period1_var = tk.StringVar(root, value=periods[0])
        period2_var = tk.StringVar(root, value=periods[1])

        def add_company_row():
            frame = tk.Frame(companies_frame, bg=BACKGROUND_COLOR)
            frame.pack(pady=5)

            company_var = tk.StringVar(root, value=get_companies()[0])
            tk.Label(frame, text="Spółka:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT)

            company_menu = tk.OptionMenu(frame, company_var, *get_companies())
            company_menu.config(bg="#FEC89A", fg="#333333", font=("Poppins", 12))  # Kolor przycisku
            company_menu["menu"].config(bg="#ECE4DB", fg="#333333")  # Kolor rozwijanego menu
            company_menu.pack(side=tk.LEFT)

            tk.Button(
                frame,
                text="Usuń",
                font=FONT_MAIN,
                bg="#FEC89A",
                command=lambda: [frame.destroy(), company_vars.remove(company_var)]
            ).pack(side=tk.LEFT, padx=10)

            company_vars.append(company_var)

        add_company_row()
        tk.Button(root, text="Dodaj spółkę", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR,
                  command=add_company_row).pack(pady=10)

        period_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        period_frame.pack(pady=10)

        tk.Label(period_frame, text="Wybierz okresy:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT,
                                                                                                         padx=5)
        periods_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        periods_frame.pack(pady=10)

        period_vars = []
        periods = ["przed pandemią COVID-19 (styczeń 2017 - luty 2020)", "w czasie okresu pandemii COVID-19 (marzec 2020 - kwiecień 2023)", "cała próba statystyczna (styczeń 2017 - wrzesień 2024)"]

        def add_period_row():
            frame = tk.Frame(periods_frame, bg=BACKGROUND_COLOR)
            frame.pack(pady=5)

            period_var = tk.StringVar(root, value=periods[0])
            tk.Label(frame, text="Okres:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT)
            tk.OptionMenu(frame, period_var, *periods).pack(side=tk.LEFT)

            tk.Button(
                frame,
                text="Usuń",
                font=FONT_MAIN,
                bg="#FEC89A",
                command=lambda: [frame.destroy(), period_vars.remove(period_var)]
            ).pack(side=tk.LEFT, padx=10)

            period_vars.append(period_var)

        add_period_row()
        tk.Button(root, text="Dodaj okres", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR,
                  command=add_period_row).pack(pady=10)

        metric_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        metric_frame.pack(pady=10)

        metrics = ["Relative Volume (RV)", "ZERO1", "ZERO2"]
        tk.Label(metric_frame, text="Wskaźnik:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT,
                                                                                                          padx=5)
        tk.OptionMenu(metric_frame, metric_var, *metrics).pack(side=tk.LEFT, padx=5)

        def generate_company_comparison_chart():
            selected_companies = [var.get() for var in company_vars]
            selected_periods = [var.get() for var in period_vars]
            selected_metric = metric_var.get()

            if len(selected_periods) < 1:
                print("Musisz wybrać jakiś okres!")
                return

            results = {}
            for company in selected_companies:
                raw_data = load_data_for_company_and_date(company, "2017-01-02", "2024-09-30")
                company_results = {}
                for period in selected_periods:
                    filtered_data = filter_data_by_period(raw_data, period)
                    if not filtered_data.empty:
                        metrics = calculate_liquidity(filtered_data)
                        company_results[period] = metrics.get(selected_metric, 0.0)
                results[company] = company_results

            if results:
                generate_comparison_chart(root, results, selected_periods, background_color=BACKGROUND_COLOR)

        tk.Button(root, text="Generuj wykres", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=generate_company_comparison_chart).pack(pady=10)
        tk.Button(root, text="Powrót", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=show_comparison_menu).pack(pady=10)

    def show_all_metrics_comparison_screen():
        for widget in root.winfo_children():
            widget.destroy()

        tk.Label(root, text="Porównaj wskaźniki dla jednej spółki", font=FONT_TITLE, fg=TITLE_COLOR, bg=BACKGROUND_COLOR).pack(pady=20)
        company_var = tk.StringVar(root, value=get_companies()[0])
        periods = ["przed pandemią COVID-19 (styczeń 2017 - luty 2020)", "w czasie okresu pandemii COVID-19 (marzec 2020 - kwiecień 2023)", "cała próba statystyczna (styczeń 2017 - wrzesień 2024)"]

        # Ramka dla wyboru spółki
        company_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        company_frame.pack(pady=10)

        tk.Label(company_frame, text="Spółka:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT,
                                                                                                         padx=5)
        company_menu = tk.OptionMenu(company_frame, company_var, *get_companies())
        company_menu.config(bg="#FEC89A", fg="#333333", font=("Poppins", 12))
        company_menu["menu"].config(bg="#ECE4DB", fg="#333333")
        company_menu.pack(side=tk.LEFT, padx=5)

        period_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        period_frame.pack(pady=10)

        tk.Label(period_frame, text="Wybierz okresy:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(
            side=tk.LEFT, padx=5)

        periods_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        periods_frame.pack(pady=10)

        period_vars = []

        def add_period_row():
            frame = tk.Frame(periods_frame, bg=BACKGROUND_COLOR)
            frame.pack(pady=5)

            period_var = tk.StringVar(root, value=periods[0])
            tk.Label(frame, text="Okres:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT)
            tk.OptionMenu(frame, period_var, *periods).pack(side=tk.LEFT)

            tk.Button(
                frame,
                text="Usuń",
                font=FONT_MAIN,
                bg="#FEC89A",
                command=lambda: [frame.destroy(), period_vars.remove(period_var)]
            ).pack(side=tk.LEFT, padx=10)

            period_vars.append(period_var)

        add_period_row()

        tk.Button(root, text="Dodaj okres", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR,
                  command=add_period_row).pack(pady=10)

        metric_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        metric_frame.pack(pady=10)

        metrics = ["Relative Volume (RV)", "ZERO1", "ZERO2"]
        metric_vars = []

        def add_metric_row():
            frame = tk.Frame(metric_frame, bg=BACKGROUND_COLOR)
            frame.pack(pady=5)

            metric_var = tk.StringVar(root, value=metrics[0])
            tk.Label(frame, text="Wskaźnik:", bg=BACKGROUND_COLOR, font=FONT_MAIN, fg=TEXT_COLOR).pack(side=tk.LEFT)
            tk.OptionMenu(frame, metric_var, *metrics).pack(side=tk.LEFT)

            tk.Button(
                frame,
                text="Usuń",
                font=FONT_MAIN,
                bg="#FEC89A",
                command=lambda: [frame.destroy(), metric_vars.remove(metric_var)]
            ).pack(side=tk.LEFT, padx=10)

            metric_vars.append(metric_var)

        add_metric_row()

        tk.Button(root, text="Dodaj wskaźnik", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR,
                  command=add_metric_row).pack(pady=10)

        def generate_all_metrics_chart():
            selected_company = company_var.get()
            selected_periods = [var.get() for var in period_vars]
            selected_metrics = [var.get() for var in metric_vars]

            if len(selected_periods) < 1:
                print("Musisz wybrać chociaż jeden okres!")
                return

            raw_data = load_data_for_company_and_date(selected_company, "2017-01-02", "2024-09-30")

            print("Załadowane dane:", raw_data)

            results = {}

            for metric in selected_metrics:
                metric_results = {}
                for period in selected_periods:
                    filtered_data = filter_data_by_period(raw_data, period)
                    print(f"Debug - Dane dla okresu {period}:", filtered_data)

                    if not filtered_data.empty:
                        metrics = calculate_liquidity(filtered_data)
                        print(f"Debug - Wyniki dla okresu {period}:", metrics)
                        value = metrics.get(metric, 0.00000)
                        metric_results[period] = metrics.get(metric, 0.00000)
                    else:
                        metric_results[period] = "Brak danych"

                results[metric] = metric_results

                print("Debug - Wyniki przekazywane do wykresu:", results)

            if results:
                generate_comparison_chart(root, results, selected_periods, background_color=BACKGROUND_COLOR)

        tk.Button(root, text="Generuj wykres", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=generate_all_metrics_chart).pack(pady=10)
        tk.Button(root, text="Powrót", font=FONT_MAIN, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER_COLOR, command=show_comparison_menu).pack(pady=10)

    show_calculation_menu()
    root.mainloop()


