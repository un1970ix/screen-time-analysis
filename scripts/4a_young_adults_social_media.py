import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_loader import (
    load_data,
    map_social_media_time_to_numeric,
    save_figure,
    format_hours,
)
from scipy import stats
import numpy as np


def analyze_young_adults_social_media():
    df = load_data("responses.csv")

    columns = [
        "Quel est votre âge ?",
        "Combien de temps passez-vous quotidiennement sur les réseaux sociaux ?",
        "Quels réseaux sociaux utilisez-vous le plus régulièrement ?",
    ]

    data = df[columns].copy()

    data.columns = ["Age", "Temps_Reseaux_Sociaux", "Reseaux_Utilises"]

    data["Temps_Reseaux_Numeric"] = data["Temps_Reseaux_Sociaux"].apply(
        map_social_media_time_to_numeric
    )

    def categorize_age(age):
        if age in ["10-14 ans", "15-19 ans"]:
            return "Adolescents (10-19 ans)"
        elif age == "20-29 ans":
            return "Jeunes adultes (20-29 ans)"
        elif age in ["30-39 ans", "40-49 ans"]:
            return "Adultes (30-49 ans)"
        elif age in ["50-59 ans", "60-70 ans", "Plus de 70 ans"]:
            return "Seniors (50+ ans)"
        else:
            return None

    data["Categorie_Age"] = data["Age"].apply(categorize_age)

    data = data.dropna(subset=["Categorie_Age", "Temps_Reseaux_Numeric"])

    age_stats = (
        data.groupby("Categorie_Age")["Temps_Reseaux_Numeric"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )

    age_stats["erreur_standard"] = age_stats["std"] / np.sqrt(age_stats["count"])

    age_order = [
        "Adolescents (10-19 ans)",
        "Jeunes adultes (20-29 ans)",
        "Adultes (30-49 ans)",
        "Seniors (50+ ans)",
    ]

    age_order = [age for age in age_order if age in age_stats["Categorie_Age"].values]

    groups = [
        data[data["Categorie_Age"] == age]["Temps_Reseaux_Numeric"].values
        for age in age_order
    ]
    f_val, p_val = stats.f_oneway(*groups)

    if p_val < 0.05:
        posthoc_data = data[data["Categorie_Age"].isin(age_order)].copy()

        from statsmodels.stats.multicomp import pairwise_tukeyhsd

        tukey = pairwise_tukeyhsd(
            posthoc_data["Temps_Reseaux_Numeric"],
            posthoc_data["Categorie_Age"],
            alpha=0.05,
        )

        tukey_df = pd.DataFrame(
            data=tukey._results_table.data[1:], columns=tukey._results_table.data[0]
        )

        young_adult_comparisons = tukey_df[
            (tukey_df["group1"] == "Jeunes adultes (20-29 ans)")
            | (tukey_df["group2"] == "Jeunes adultes (20-29 ans)")
        ]
    else:
        young_adult_comparisons = None

    plt.figure(figsize=(12, 8))

    ax = sns.barplot(
        x="Categorie_Age",
        y="mean",
        data=age_stats,
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

    plt.title("Temps moyen passé sur les réseaux sociaux par catégorie d'âge")
    plt.xlabel("Catégorie d'âge")
    plt.ylabel("Temps moyen sur les réseaux sociaux (heures/jour)")
    plt.xticks(rotation=45)

    save_figure(
        plt,
        "4a_young_adults_social_media",
        "Temps moyen passé sur les réseaux sociaux par catégorie d'âge",
        "Catégorie d'âge",
        "Temps moyen sur les réseaux sociaux (heures/jour)",
    )

    network_counts = {}

    for age_cat in age_order:
        age_data = data[data["Categorie_Age"] == age_cat]

        networks = []
        for networks_str in age_data["Reseaux_Utilises"].dropna():
            networks.extend([network.strip() for network in networks_str.split(";")])

        count = pd.Series(networks).value_counts()
        normalized = (count / len(age_data)) * 100

        network_counts[age_cat] = normalized

    network_df = pd.DataFrame(network_counts)

    network_df = network_df.fillna(0)

    top_networks = network_df.mean(axis=1).nlargest(6).index
    network_df_filtered = network_df.loc[top_networks]

    plt.figure(figsize=(14, 10))

    sns.heatmap(
        network_df_filtered,
        annot=True,
        fmt=".1f",
        cmap="viridis",
        linewidths=0.5,
        cbar_kws={"label": "% d'utilisation"},
    )

    plt.title("Utilisation des réseaux sociaux par catégorie d'âge")
    plt.ylabel("Réseau social")
    plt.xlabel("Catégorie d'âge")

    save_figure(
        plt,
        "4a_social_media_usage_by_age",
        "Utilisation des réseaux sociaux par catégorie d'âge",
        "Catégorie d'âge",
        "Réseau social",
    )

    young_adults_mean = (
        age_stats[age_stats["Categorie_Age"] == "Jeunes adultes (20-29 ans)"][
            "mean"
        ].values[0]
        if "Jeunes adultes (20-29 ans)" in age_stats["Categorie_Age"].values
        else None
    )

    other_groups_mean = (
        age_stats[age_stats["Categorie_Age"] != "Jeunes adultes (20-29 ans)"][
            "mean"
        ].mean()
        if "Jeunes adultes (20-29 ans)" in age_stats["Categorie_Age"].values
        else None
    )

    result = {
        "age_stats": age_stats.to_dict(),
        "anova_f": f_val,
        "anova_p": p_val,
        "young_adults_mean": young_adults_mean,
        "other_groups_mean": other_groups_mean,
        "difference": young_adults_mean - other_groups_mean
        if young_adults_mean and other_groups_mean
        else None,
        "significant_difference": p_val < 0.05,
        "young_adult_comparisons": young_adult_comparisons.to_dict()
        if young_adult_comparisons is not None
        else None,
    }

    return result


if __name__ == "__main__":
    results = analyze_young_adults_social_media()
    print("Analyse 4.a terminée avec succès.")
