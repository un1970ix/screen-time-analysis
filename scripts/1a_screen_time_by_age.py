import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_loader import (
    load_data,
    map_age_to_numeric,
    map_screen_time_to_numeric,
    save_figure,
    format_hours,
)
import numpy as np
from scipy import stats


def analyze_screen_time_by_age():
    df = load_data("responses.csv")

    data = df[
        [
            "Quel est votre âge ?",
            "Combien d'heures par jour passez-vous en moyenne devant vos écrans ?",
        ]
    ].copy()

    data.columns = ["Age", "Temps_Ecran"]

    data["Age_Numeric"] = data["Age"].apply(map_age_to_numeric)
    data["Temps_Ecran_Numeric"] = data["Temps_Ecran"].apply(map_screen_time_to_numeric)

    data = data.dropna()

    age_groups = (
        data.groupby("Age")
        .agg({"Temps_Ecran_Numeric": ["mean", "std", "count"]})
        .reset_index()
    )

    age_groups.columns = ["Age", "Moyenne", "Ecart_Type", "Nombre"]

    age_groups["Erreur_Standard"] = age_groups["Ecart_Type"] / np.sqrt(
        age_groups["Nombre"]
    )

    age_order = [
        "10-14 ans",
        "15-19 ans",
        "20-29 ans",
        "30-39 ans",
        "40-49 ans",
        "50-59 ans",
        "60-70 ans",
        "Plus de 70 ans",
    ]

    age_order = [age for age in age_order if age in age_groups["Age"].values]

    plt.figure(figsize=(12, 8))
    ax = sns.barplot(
        x="Age",
        y="Moyenne",
        data=age_groups,
        order=age_order,
        palette="viridis",
        errorbar=("ci", 95),
    )

    for i, p in enumerate(ax.patches):
        height = p.get_height()
        ax.text(
            p.get_x() + p.get_width() / 2.0,
            height + 0.1,
            format_hours(height),
            ha="center",
        )

    groups = [
        data[data["Age"] == age]["Temps_Ecran_Numeric"].values for age in age_order
    ]
    f_val, p_val = stats.f_oneway(*groups)

    plt.title("Temps d'écran moyen par tranche d'âge")
    plt.xlabel("Tranche d'âge")
    plt.ylabel("Temps d'écran moyen (heures/jour)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    save_figure(
        plt,
        "1a_screen_time_by_age",
        "Temps d'écran moyen par tranche d'âge",
        "Tranche d'âge",
        "Temps d'écran moyen (heures/jour)",
    )

    result = {
        "f_statistic": f_val,
        "p_value": p_val,
        "significant_difference": p_val < 0.05,
        "age_groups": age_groups.to_dict(),
    }

    return result


if __name__ == "__main__":
    results = analyze_screen_time_by_age()
    print("Analyse 1.a terminée avec succès.")
