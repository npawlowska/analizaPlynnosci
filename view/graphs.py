import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from view.calculations_view import show_calculations


def generate_comparison_chart(root, results, periods, background_color="#F5EBE0"):
    if not results:
        print("Brak danych do wygenerowania wykresu.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    colors = ["#D6CCC2", "#D5BDAF", "#E3D5CA", "#8a817c", "#847577"]
    labels = list(results.keys())
    n_periods = len(periods)
    x_indexes = np.arange(len(labels))
    width = 0.8 / n_periods

    for idx, period in enumerate(periods):
        values = [results[label].get(period, 0) for label in labels]
        ax.bar(
            x_indexes + idx * width,
            values,
            width=width,
            label=f"{period}",
            color=colors[idx % len(colors)],
            alpha=0.8,
        )

    ax.set_title("Wykres porównawczy", fontsize=16, pad=20)
    ax.set_xlabel("Etykiety", fontsize=14, labelpad=10)
    ax.set_ylabel("Wartości", fontsize=14, labelpad=10)
    ax.set_xticks(x_indexes + width / 2 * (n_periods - 1))
    ax.set_xticklabels(labels, fontsize=12)

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        fontsize=10,
        ncol=n_periods,
        title="Okresy"
    )

    plt.tight_layout(rect=[0, 0, 1, 1])
    ax.grid(True, linestyle="--", alpha=0.5)

    chart_window = tk.Toplevel(root)
    chart_window.title("Wykres porównawczy")
    chart_window.geometry("1000x800")
    chart_window.configure(bg="#FFFFFF")

    frame = tk.Frame(chart_window, bg="#FFFFFF")
    frame.pack(fill=tk.BOTH, expand=True)
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

    tk.Button(
        chart_window,
        text="Zobacz obliczenia",
        font=("Poppins", 12),
        bg="#FFD7BA",
        activebackground="#FFB6C1",
        command=lambda: show_calculations(chart_window, results)
    ).pack(pady=10)

    tk.Button(
        chart_window,
        text="Zamknij",
        font=("Poppins", 12),
        bg="#FFD7BA",
        activebackground="#FFB6C1",
        command=chart_window.destroy
    ).pack(pady=10)
