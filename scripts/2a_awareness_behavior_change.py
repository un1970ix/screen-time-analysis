import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from utils.data_loader import load_data, save_figure


def analyze_awareness_behavior_change():
    df = load_data("responses.csv")

    columns = [
        "Pensez-vous que votre temps d'écran a un impact sur votre :",
        "Avez-vous déjà essayé de réduire votre temps d'écran ?",
        "Pensez-vous que votre temps d'écran est trop élevé ?",
        "Quelles stratégies utilisez-vous actuellement pour réguler votre temps d'écran ?",
    ]

    data = df[columns].copy()

    data.columns = [
        "Impact_Percu",
        "Tentative_Reduction",
        "Conscience_Temps_Eleve",
        "Strategies_Regulation",
    ]

    has_impact = data["Impact_Percu"].notna() & (data["Impact_Percu"] != "")
    concerned_about_time = data["Conscience_Temps_Eleve"] == "Oui"

    aware_of_issues = has_impact | concerned_about_time

    attempted_reduction = data["Tentative_Reduction"].str.contains("Oui", na=False)
    unsuccessful_reduction = data["Tentative_Reduction"] == "Oui, sans succès"
    no_strategy = data["Strategies_Regulation"].isin(["Aucune stratégie", ""])

    aware_count = aware_of_issues.sum()
    total_count = len(data)
    aware_percentage = (aware_count / total_count) * 100

    aware_and_tried = aware_of_issues & attempted_reduction
    aware_and_unsuccessful = aware_of_issues & unsuccessful_reduction
    aware_and_no_strategy = aware_of_issues & no_strategy

    aware_tried_percentage = (
        (aware_and_tried.sum() / aware_count) * 100 if aware_count > 0 else 0
    )
    aware_unsuccessful_percentage = (
        (aware_and_unsuccessful.sum() / aware_count) * 100 if aware_count > 0 else 0
    )
    aware_no_strategy_percentage = (
        (aware_and_no_strategy.sum() / aware_count) * 100 if aware_count > 0 else 0
    )

    failed_among_tried = (
        unsuccessful_reduction.sum() / attempted_reduction.sum()
        if attempted_reduction.sum() > 0
        else 0
    )

    fig = plt.figure(figsize=(16, 10))

    gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, 0])
    awareness_labels = ["Conscients des\nproblèmes", "Non conscients"]
    awareness_values = [aware_percentage, 100 - aware_percentage]
    ax1.pie(
        awareness_values,
        labels=awareness_labels,
        autopct="%1.1f%%",
        colors=["#3498db", "#e74c3c"],
        wedgeprops=dict(width=0.5, edgecolor="w"),
    )
    ax1.set_title("Conscience des problèmes liés aux écrans")

    ax2 = fig.add_subplot(gs[0, 1])
    attempt_labels = ["Ont essayé\nde réduire", "N'ont pas\nessayé"]
    attempt_values = [aware_tried_percentage, 100 - aware_tried_percentage]
    ax2.pie(
        attempt_values,
        labels=attempt_labels,
        autopct="%1.1f%%",
        colors=["#2ecc71", "#f39c12"],
        wedgeprops=dict(width=0.5, edgecolor="w"),
    )
    ax2.set_title("Tentatives de réduction\n(parmi les conscients)")

    ax3 = fig.add_subplot(gs[1, 0])
    failure_rate = failed_among_tried * 100
    success_rate = 100 - failure_rate
    success_labels = ["Avec succès", "Sans succès"]
    success_values = [success_rate, failure_rate]
    ax3.pie(
        success_values,
        labels=success_labels,
        autopct="%1.1f%%",
        colors=["#27ae60", "#c0392b"],
        wedgeprops=dict(width=0.5, edgecolor="w"),
    )
    ax3.set_title("Taux de succès\n(parmi ceux qui ont essayé)")

    ax4 = fig.add_subplot(gs[1, 1])
    strategy_labels = ["Ont une\nstratégie", "Sans\nstratégie"]
    strategy_values = [100 - aware_no_strategy_percentage, aware_no_strategy_percentage]
    ax4.pie(
        strategy_values,
        labels=strategy_labels,
        autopct="%1.1f%%",
        colors=["#9b59b6", "#f1c40f"],
        wedgeprops=dict(width=0.5, edgecolor="w"),
    )
    ax4.set_title("Utilisation de stratégies\n(parmi les conscients)")

    plt.suptitle(
        "Conscience des problèmes liés aux écrans et difficulté à modifier les comportements",
        fontsize=16,
        y=0.98,
    )

    save_figure(
        plt,
        "2a_awareness_behavior_change",
        "Conscience des problèmes liés aux écrans et difficulté à modifier les comportements",
        "",
        "",
    )

    result = {
        "aware_of_issues_percentage": aware_percentage,
        "attempted_reduction_percentage": aware_tried_percentage,
        "unsuccessful_reduction_percentage": aware_unsuccessful_percentage,
        "no_strategy_percentage": aware_no_strategy_percentage,
        "failure_rate_among_those_who_tried": failed_among_tried * 100,
    }

    return result


if __name__ == "__main__":
    results = analyze_awareness_behavior_change()
    print("Analyse 2.a terminée avec succès.")
