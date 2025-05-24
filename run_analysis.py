import os
import importlib
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

analysis_scripts = [
    "scripts.1a_screen_time_by_age",
    "scripts.1b_age_screen_time_correlation",
    "scripts.2a_awareness_behavior_change",
    "scripts.2b_smartphone_waking_regulation",
    "scripts.3a_gaming_screen_time",
    "scripts.3b_work_screen_time",
    "scripts.4a_young_adults_social_media",
]


def run_all_analyses():
    """Exécute tous les scripts d'analyse et collecte les résultats."""
    results = {}

    print("Exécution de toutes les analyses...")

    if not os.path.exists("graphs"):
        os.makedirs("graphs")

    for script in analysis_scripts:
        print(f"\nExécution de {script}.py...")

        module = importlib.import_module(script)

        analysis_function = None
        for item_name in dir(module):
            if item_name.startswith("analyze_"):
                analysis_function = getattr(module, item_name)
                break

        if analysis_function:
            try:
                script_results = analysis_function()
                results[script] = script_results
                print(f"✓ Analyse {script} terminée avec succès.")
            except Exception as e:
                print(f"✗ Erreur lors de l'exécution de {script}: {str(e)}")
                results[script] = {"error": str(e)}
        else:
            print(f"✗ Impossible de trouver la fonction d'analyse dans {script}.py")

    return results


if __name__ == "__main__":
    results = run_all_analyses()

    print("\nAnalyse terminée.")
