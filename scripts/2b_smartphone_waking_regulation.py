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


def analyze_smartphone_waking_regulation():
    df = load_data("responses.csv")

    columns = [
        "Allez-vous directement sur votre smartphone dès le réveil ?",
        "Combien d'heures par jour passez-vous en moyenne devant vos écrans ?",
    ]

    data = df[columns].copy()

    data.columns = ["Smartphone_Reveil", "Temps_Ecran"]

    data["Temps_Ecran_Numeric"] = data["Temps_Ecran"].apply(map_screen_time_to_numeric)

    reveil_smartphone = data[data["Smartphone_Reveil"] == "Oui"]
    non_reveil_smartphone = data[data["Smartphone_Reveil"] == "Non"]

    reveil_screen_time = reveil_smartphone["Temps_Ecran_Numeric"].mean()
    non_reveil_screen_time = non_reveil_smartphone["Temps_Ecran_Numeric"].mean()

    fig, ax = plt.subplots(figsize=(10, 6))

    categories = ["Smartphone dès le réveil", "Pas de smartphone au réveil"]
    values = [reveil_screen_time, non_reveil_screen_time]

    bars = ax.bar(categories, values, color=sns.color_palette("viridis", 2))

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.1,
            format_hours(height),
            ha="center",
            va="bottom",
        )

    ax.set_ylabel("Temps d'écran moyen (heures/jour)")
    ax.set_title("Temps d'écran moyen selon l'utilisation du smartphone au réveil")

    save_figure(
        plt,
        "2b_smartphone_waking_regulation_screentime",
        "Temps d'écran moyen selon l'utilisation du smartphone au réveil",
        "",
        "Temps d'écran moyen (heures/jour)",
    )

    total_respondents = len(data.dropna(subset=["Smartphone_Reveil"]))
    reveil_count = len(reveil_smartphone)
    non_reveil_count = len(non_reveil_smartphone)
    reveil_percentage = (reveil_count / total_respondents) * 100
    non_reveil_percentage = (non_reveil_count / total_respondents) * 100

    result = {
        "reveil_smartphone_percentage": reveil_percentage,
        "non_reveil_smartphone_percentage": non_reveil_percentage,
        "reveil_screen_time": reveil_screen_time,
        "non_reveil_screen_time": non_reveil_screen_time,
        "difference": reveil_screen_time - non_reveil_screen_time,
    }

    return result


if __name__ == "__main__":
    results = analyze_smartphone_waking_regulation()
    print("Analyse 2.b terminée avec succès.")
