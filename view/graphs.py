import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def generate_comparison_chart(root, results, periods, background_color="#F5EBE0"):
    """
    Generuje wykres porównawczy na podstawie wyników i okresów.
    """
    if not results:  # Jeśli brak wyników
        print("Brak danych do wygenerowania wykresu.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#9C6644", "#7F5539", "#B08968", "#CB997E", "#CEBEBE",
              "#A26769", "#5E3023", "#701C1C", "#FFB4A2", "#B5838D"]

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
        # Dodanie wartości nad słupkami
        for i, val in enumerate(values):
            ax.text(
                x_indexes[i] + idx * width, val + 0.02, f"{val:.2f}",
                ha='center', va='bottom', fontsize=10
            )

    # Tytuły i osie
    ax.set_title("Wykres porównawczy", fontsize=16, pad=20)
    ax.set_xlabel("Etykiety (Spółki lub Wskaźniki)", fontsize=14, labelpad=10)
    ax.set_ylabel("Wartości", fontsize=14, labelpad=10)
    ax.set_xticks(x_indexes + width / 2 * (n_periods - 1))  # Wyśrodkowanie etykiet na osi X
    ax.set_xticklabels(labels, fontsize=12)
    ax.legend(loc="upper left", fontsize=10)

    # Dodanie siatki
    ax.grid(True, linestyle="--", alpha=0.5)

    # Wyświetlanie w nowym oknie
    chart_window = tk.Toplevel(root)
    chart_window.title("Wykres porównawczy")
    chart_window.geometry("900x700")
    chart_window.configure(bg=background_color)

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()
