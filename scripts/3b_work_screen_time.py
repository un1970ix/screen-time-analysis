import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_loader import (
    load_data,
    map_screen_time_to_numeric,
    save_figure,
    format_hours,
)


def analyze_work_screen_time():
    df = load_data("responses.csv")

    columns = [
        "Utilisez-vous des écrans pour vos études ou votre travail ?",
        "Combien d'heures par jour utilisez-vous des écrans pour vos études/travail ?",
        "Combien d'heures par jour passez-vous en moyenne devant vos écrans ?",
    ]

    data = df[columns].copy()

    data.columns = ["Utilisation_Travail", "Temps_Ecran_Travail", "Temps_Ecran_Total"]

    data_work = data[data["Utilisation_Travail"] == "Oui"].copy()

    def map_work_time_to_numeric(work_time):
        time_mapping = {
            "Moins de 1 heure": 0.5,
            "1-2 heures": 1.5,
            "2-3 heures": 2.5,
            "3-4 heures": 3.5,
            "4-5 heures": 4.5,
            "5-6 heures": 5.5,
            "6-7 heures": 6.5,
            "7-8 heures": 7.5,
            "Plus de 8 heures": 8.5,
        }
        return time_mapping.get(work_time, None)

    data_work["Temps_Ecran_Travail_Numeric"] = data_work["Temps_Ecran_Travail"].apply(
        map_work_time_to_numeric
    )
    data_work["Temps_Ecran_Total_Numeric"] = data_work["Temps_Ecran_Total"].apply(
        map_screen_time_to_numeric
    )

    data_work = data_work.dropna(
        subset=["Temps_Ecran_Travail_Numeric", "Temps_Ecran_Total_Numeric"]
    )

    data_work["Temps_Ecran_Personnel"] = (
        data_work["Temps_Ecran_Total_Numeric"]
        - data_work["Temps_Ecran_Travail_Numeric"]
    )

    data_work["Temps_Ecran_Personnel"] = data_work["Temps_Ecran_Personnel"].clip(
        lower=0
    )

    mean_total = data_work["Temps_Ecran_Total_Numeric"].mean()
    mean_work = data_work["Temps_Ecran_Travail_Numeric"].mean()
    mean_personal = data_work["Temps_Ecran_Personnel"].mean()

    sum_parts = mean_work + mean_personal

    if sum_parts != mean_total and sum_parts > 0:
        scaling_factor = mean_total / sum_parts
        mean_work = mean_work * scaling_factor
        mean_personal = mean_personal * scaling_factor

    pct_work = (mean_work / mean_total) * 100
    pct_personal = (mean_personal / mean_total) * 100

    fig, ax = plt.subplots(figsize=(12, 10))

    labels = ["Professionnel", "Personnel"]
    sizes = [mean_work, mean_personal]

    ax.pie(
        sizes,
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("viridis", len(sizes)),
        wedgeprops=dict(width=0.5, edgecolor="w"),
    )

    legend_labels = [
        f"{labels[i]} ({format_hours(sizes[i])})" for i in range(len(labels))
    ]
    ax.legend(legend_labels, loc="upper right", bbox_to_anchor=(1.0, 0.9))

    ax.axis("equal")

    plt.title("Répartition du temps d'écran entre usage professionnel et personnel")

    save_figure(
        plt,
        "3b_work_screen_time_pie",
        "Répartition du temps d'écran entre usage professionnel et personnel",
        "",
        "",
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    categories = [
        "Temps d'écran total",
        "Temps d'écran professionnel",
        "Temps d'écran personnel",
    ]
    values = [mean_total, mean_work, mean_personal]

    bars = ax.bar(
        categories, values, color=sns.color_palette("viridis", len(categories))
    )

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.1,
            format_hours(height),
            ha="center",
            va="bottom",
        )

    ax.set_ylabel("Temps moyen (heures/jour)")
    ax.set_title("Répartition du temps d'écran quotidien")

    save_figure(
        plt,
        "3b_work_screen_time_bars",
        "Répartition du temps d'écran quotidien",
        "",
        "Temps moyen (heures/jour)",
    )

    work_less_than_half = (
        data_work["Temps_Ecran_Travail_Numeric"]
        / data_work["Temps_Ecran_Total_Numeric"]
        < 0.5
    ).sum()
    pct_work_less_than_half = (work_less_than_half / len(data_work)) * 100

    result = {
        "mean_total_screen_time": mean_total,
        "mean_work_screen_time": mean_work,
        "mean_personal_screen_time": mean_personal,
        "work_percentage": pct_work,
        "personal_percentage": pct_personal,
        "people_using_screens_for_work": len(data_work),
        "people_with_work_less_than_half": work_less_than_half,
        "percentage_with_work_less_than_half": pct_work_less_than_half,
        "work_is_minority": pct_work < 50,
    }

    return result


if __name__ == "__main__":
    results = analyze_work_screen_time()
    print("Analyse 3.b terminée avec succès.")
