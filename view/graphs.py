import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from view.calculations_view import show_calculations

def generate_comparison_chart(root, results, periods, background_color="#F5EBE0"):
    """
    Generuje wykres porównawczy na podstawie wyników i okresów.
    """
    if not results:  # Jeśli brak wyników
        print("Brak danych do wygenerowania wykresu.")
        return

    background_color = "#D8E2DC"

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(background_color)  # Kolor tła całej figury
    ax.set_facecolor(background_color)

    colors = ["#D6CCC2", "#D5BDAF", "#E3D5CA", "#8a817c", "#847577"]

    # Lista etykiet (spółki lub wskaźniki) i liczba okresów
    labels = list(results.keys())
    n_periods = len(periods)

    # Indeksy grup dla każdej etykiety
    x_indexes = np.arange(len(labels))
    width = 0.35  # Szerokość słupka

    for idx, period in enumerate(periods):
        # Pobieranie wartości dla danego okresu
        values = [results[label].get(period, 0) for label in labels]
        ax.bar(
            x_indexes + idx * width,  # Pozycje słupków przesunięte dla każdego okresu
            values,
            width=width,
            label=f"{period}",
            color=colors[idx % len(colors)],
            alpha=0.8,
        )
        # Dodanie wartości nad słupkami (jeśli mieszczą się w zakresie Y)
        for i, val in enumerate(values):
            if val <= 1.2 * max(values):  # Zapobiegamy wychodzeniu poza zakres
                ax.text(
                    x_indexes[i] + idx * width, val + 0.02, f"{val:.2f}",
                    ha='center', va='bottom', fontsize=10
                )

    # Tytuły i osie
    ax.set_title("Wykres porównawczy", fontsize=16, pad=20)
    ax.set_xlabel("Etykiety", fontsize=14, labelpad=10)
    ax.set_ylabel("Wartości", fontsize=14, labelpad=10)
    ax.set_xticks(x_indexes + width / 2 * (n_periods - 1))  # Wyśrodkowanie etykiet na osi X
    ax.set_xticklabels(labels, fontsize=12)
    ax.legend(loc="upper left", fontsize=10)

    # Dostosowanie zakresu osi Y (dodajemy trochę przestrzeni)
    max_value = max([max(results[label].values()) for label in results.keys()])
    ax.set_ylim(0, max_value * 1.2)  # Górny zakres Y = 120% najwyższej wartości

    # Dodanie legendy poniżej wykresu
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),  # Pozycja poniżej wykresu
        fontsize=10,
        ncol=n_periods,  # Liczba kolumn odpowiada liczbie okresów
        title="Okresy"
    )

    # Automatyczne dopasowanie elementów na wykresie
    plt.tight_layout(rect=[0, 0, 1, 0.9])  # Dopasowanie marginesów

    # Dodanie siatki
    ax.grid(True, linestyle="--", alpha=0.5)

    # Wyświetlanie w nowym oknie
    chart_window = tk.Toplevel(root)
    chart_window.title("Wykres porównawczy")
    chart_window.geometry("1000x800")
    chart_window.configure(bg=background_color)

    frame = tk.Frame(chart_window, bg="#D8E2DC")  # Tło ramki
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()
# Dodanie przycisku „Zobacz obliczenia”
    tk.Button(
        chart_window,
        text="Zobacz obliczenia",
        font=("Poppins", 12),
        bg="#FFD7BA",
        activebackground="#FFB6C1",
        command=lambda: show_calculations(chart_window, results)  # Wywołanie zewnętrznej funkcji
    ).pack(pady=10)

    tk.Button(
        chart_window,
        text="Zamknij",
        font=("Poppins", 12),
        bg="#FFD7BA",
        activebackground="#FFB6C1",
        command=chart_window.destroy
    ).pack(pady=10)