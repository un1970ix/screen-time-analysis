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
from scipy import stats
import numpy as np


def analyze_gaming_screen_time():
    df = load_data("responses.csv")

    columns = [
        "Jouez-vous aux jeux vidéo ?",
        "Combien d'heures par jour passez-vous en moyenne devant vos écrans ?",
        "Combien d'heures en moyenne par jour passez-vous devant les jeux vidéos ?",
    ]

    data = df[columns].copy()

    data.columns = ["Joue_Jeux_Video", "Temps_Ecran", "Temps_Jeux_Video"]

    data["Temps_Ecran_Numeric"] = data["Temps_Ecran"].apply(map_screen_time_to_numeric)

    gamers = data[data["Joue_Jeux_Video"] == "Oui"].copy()
    non_gamers = data[data["Joue_Jeux_Video"] == "Non"].copy()

    gamer_screen_time = gamers["Temps_Ecran_Numeric"].dropna()
    non_gamer_screen_time = non_gamers["Temps_Ecran_Numeric"].dropna()

    gamer_mean = gamer_screen_time.mean()
    non_gamer_mean = non_gamer_screen_time.mean()

    gamer_std = gamer_screen_time.std()
    non_gamer_std = non_gamer_screen_time.std()

    t_stat, p_value = stats.ttest_ind(
        gamer_screen_time, non_gamer_screen_time, equal_var=False
    )

    pooled_std = np.sqrt(
        (
            (len(gamer_screen_time) - 1) * gamer_std**2
            + (len(non_gamer_screen_time) - 1) * non_gamer_std**2
        )
        / (len(gamer_screen_time) + len(non_gamer_screen_time) - 2)
    )

    cohen_d = (gamer_mean - non_gamer_mean) / pooled_std if pooled_std > 0 else 0

    fig, ax = plt.subplots(figsize=(10, 6))

    categories = ["Joueurs de jeux vidéo", "Non-joueurs"]
    values = [gamer_mean, non_gamer_mean]
    errors = [
        gamer_std / np.sqrt(len(gamer_screen_time)),
        non_gamer_std / np.sqrt(len(non_gamer_screen_time)),
    ]

    bars = ax.bar(
        categories,
        values,
        yerr=errors,
        capsize=10,
        color=sns.color_palette("viridis", 2),
    )

    colors = sns.color_palette("viridis", 2)
    legend_elements = [
        plt.Rectangle(
            (0, 0),
            1,
            1,
            fc=colors[i],
            label=f"{categories[i]}: {format_hours(values[i])}",
        )
        for i in range(len(categories))
    ]
    ax.legend(handles=legend_elements, loc="upper right")

    ax.set_ylabel("Temps d'écran moyen (heures/jour)")
    ax.set_title("Temps d'écran moyen selon la pratique des jeux vidéo")

    save_figure(
        plt,
        "3a_gaming_screen_time",
        "Temps d'écran moyen selon la pratique des jeux vidéo",
        "",
        "Temps d'écran moyen (heures/jour)",
    )

    total_respondents = len(data.dropna(subset=["Joue_Jeux_Video"]))
    gamer_count = len(gamers)
    non_gamer_count = len(non_gamers)
    gamer_percentage = (gamer_count / total_respondents) * 100
    non_gamer_percentage = (non_gamer_count / total_respondents) * 100

    result = {
        "gamer_percentage": gamer_percentage,
        "non_gamer_percentage": non_gamer_percentage,
        "gamer_mean_screen_time": gamer_mean,
        "non_gamer_mean_screen_time": non_gamer_mean,
        "difference": gamer_mean - non_gamer_mean,
        "t_statistic": t_stat,
        "p_value": p_value,
        "cohen_d": cohen_d,
        "significant_difference": p_value < 0.05,
    }

    return result


if __name__ == "__main__":
    results = analyze_gaming_screen_time()
    print("Analyse 3.a terminée avec succès.")
