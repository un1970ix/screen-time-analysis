import pandas as pd
import os


def load_data(file_path="responses.csv"):
    df = pd.read_csv(file_path, sep=",")

    if not os.path.exists("graphs"):
        os.makedirs("graphs")

    return df


def map_age_to_numeric(age_category):
    age_mapping = {
        "10-14 ans": 12,
        "15-19 ans": 17,
        "20-29 ans": 25,
        "30-39 ans": 35,
        "40-49 ans": 45,
        "50-59 ans": 55,
        "60-70 ans": 65,
        "Plus de 70 ans": 75,
    }
    return age_mapping.get(age_category, None)


def map_screen_time_to_numeric(screen_time):
    time_mapping = {
        "Moins de 1 heure": 0.5,
        "1-2 heures": 1.5,
        "2-3 heures": 2.5,
        "3-4 heures": 3.5,
        "4-5 heures": 4.5,
        "5-6 heures": 5.5,
        "Plus de 6 heures": 6.5,
    }
    return time_mapping.get(screen_time, None)


def map_social_media_time_to_numeric(social_time):
    time_mapping = {
        "Moins de 30 minutes": 0.25,
        "30 minutes à 1 heure": 0.75,
        "1 à 2 heures": 1.5,
        "2 à 3 heures": 2.5,
        "3 à 4 heures": 3.5,
        "Plus de 4 heures": 4.5,
    }
    return time_mapping.get(social_time, None)


def filter_neuchatel_data(df):
    return df[df["Quel est votre canton de résidence ?"] == "NE"]


def format_hours(hours):
    hours_part = int(hours)
    minutes_part = int((hours - hours_part) * 60)
    return f"{hours_part}h{minutes_part:02d}m"


def save_figure(plt, filename, title=None, xlabel=None, ylabel=None):
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)

    plt.tight_layout()
    plt.savefig(f"graphs/{filename}.png", dpi=300)
    plt.close()
