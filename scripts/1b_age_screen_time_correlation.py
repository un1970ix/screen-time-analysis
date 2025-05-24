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
)
from scipy import stats


def analyze_age_screen_time_correlation():
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

    correlation, p_value = stats.pearsonr(
        data["Age_Numeric"], data["Temps_Ecran_Numeric"]
    )

    spearman_corr, spearman_p = stats.spearmanr(
        data["Age_Numeric"], data["Temps_Ecran_Numeric"]
    )

    plt.figure(figsize=(12, 8))

    sns.regplot(
        x="Age_Numeric",
        y="Temps_Ecran_Numeric",
        data=data,
        scatter_kws={"alpha": 0.5},
        line_kws={"color": "red"},
    )

    save_figure(
        plt,
        "1b_age_screen_time_correlation",
        "Corrélation entre l'âge et le temps d'écran quotidien",
        "Âge (années)",
        "Temps d'écran moyen (heures/jour)",
    )

    result = {
        "pearson_correlation": correlation,
        "pearson_p_value": p_value,
        "spearman_correlation": spearman_corr,
        "spearman_p_value": spearman_p,
        "inverse_correlation": correlation < 0 and p_value < 0.05,
    }

    return result


if __name__ == "__main__":
    results = analyze_age_screen_time_correlation()
    print("Analyse 1.b terminée avec succès.")
