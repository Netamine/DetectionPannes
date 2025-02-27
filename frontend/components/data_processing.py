import pandas as pd
from tqdm import tqdm

def adjust_last_digit_of_seconds(timestamp):
    """Ajuste uniquement le dernier chiffre des secondes du timestamp pour le rendre multiple de 10."""
    seconds = timestamp.second
    last_digit = seconds % 10

    if 1 <= last_digit <= 5:
        adjustment = -last_digit
    elif last_digit > 5:
        adjustment = 10 - last_digit
    else:
        adjustment = 0

    return timestamp + pd.Timedelta(seconds=adjustment)

def fill_missing_timestamps(df):
    """Ordonne les timestamps et ajoute les observations manquantes avec des NaN pour les features."""
    # Convertir en datetime et trier
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.sort_values(by='timestamp').reset_index(drop=True)

    # Ajustement des timestamps avec tqdm pour suivi du processus
    tqdm.pandas(desc="🔄 Ajustement des timestamps")
    df['timestamp'] = df['timestamp'].progress_apply(adjust_last_digit_of_seconds)

    print("✅ Vérification des timestamps après ajustement :")
    print(df['timestamp'].head())

    # Générer tous les timestamps attendus
    min_time, max_time = df['timestamp'].min(), df['timestamp'].max()
    all_timestamps = pd.date_range(start=min_time, end=max_time, freq='10s')

    # Création du DataFrame complet
    df_full = pd.DataFrame({'timestamp': all_timestamps})

    #  Fusion avec le DataFrame existant
    df_merged = df_full.merge(df, on='timestamp', how='left')

    print("\n✅ Vérification des données manquantes après correction :")
    missing_count = df_merged.isnull().sum().sum()
    print(f"🔍 Nombre total de valeurs manquantes créées : {missing_count}")

    return df_merged