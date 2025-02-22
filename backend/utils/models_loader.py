import os
import joblib
import tensorflow as tf
import logging
import subprocess

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Variable globale pour éviter de recharger les modèles plusieurs fois
_cached_models = None


def load_models(model_dir):
    """
    Charge les modèles d'imputation et de détection UNE SEULE FOIS.
    Vérifie si les modèles existent et tente de les récupérer avec DVC si absents.

    :param model_dir: Chemin vers le répertoire des modèles.
    :return: Dictionnaire contenant les modèles chargés.
    """
    global _cached_models
    if _cached_models is not None:
        return _cached_models  # Retourne les modèles en cache s'ils sont déjà chargés

    models = {}

    # 📌 Vérifier si le dossier des modèles existe et contient des fichiers
    if not os.path.exists(model_dir) or not os.listdir(model_dir):
        logging.warning("📥 Modèles absents. Tentative de récupération via DVC...")
        try:
            subprocess.run(["dvc", "pull"], check=True)
            logging.info("✅ Modèles récupérés avec succès via DVC !")
        except subprocess.CalledProcessError:
            logging.error("❌ Échec de la récupération des modèles avec DVC.")
            return models  # On retourne un dictionnaire vide si l’opération échoue

    model_files = os.listdir(model_dir)
    if not model_files:
        logging.warning(f"⚠️ Aucun fichier modèle trouvé dans {model_dir}.")
        return models

    # 🔹 Chargement des modèles `.pkl`
    for model_file in model_files:
        model_path = os.path.join(model_dir, model_file)

        if model_file.endswith(".pkl"):
            col_name = model_file.replace(".pkl", "")
            try:
                models[col_name] = joblib.load(model_path)
                logging.info(f"✅ Modèle chargé : {col_name}")
            except Exception as e:
                logging.error(f"❌ Erreur lors du chargement du modèle {model_file}: {e}")

    # 🔹 Chargement du modèle SAE (`sae_trained.keras`)
    sae_path = os.path.join(model_dir, "sae_trained.keras")
    if os.path.exists(sae_path):
        try:
            models["sae"] = tf.keras.models.load_model(sae_path)
            logging.info("✅ Modèle SAE chargé avec succès !")
        except Exception as e:
            logging.error(f"❌ Erreur lors du chargement du modèle SAE : {e}")

    # 🔹 Chargement du scaler (`scaler.pkl`)
    scaler_path = os.path.join(model_dir, "scaler.pkl")
    if os.path.exists(scaler_path):
        try:
            models["scaler"] = joblib.load(scaler_path)
            logging.info("✅ Scaler chargé avec succès !")
        except Exception as e:
            logging.error(f"❌ Erreur lors du chargement du Scaler : {e}")

    # 🔹 Chargement du seuil d'anomalie (`threshold_final.pkl`)
    threshold_path = os.path.join(model_dir, "threshold_final.pkl")
    if os.path.exists(threshold_path):
        try:
            models["threshold"] = joblib.load(threshold_path)
            logging.info(f"✅ Seuil d'anomalie chargé : {models['threshold']}")
        except Exception as e:
            logging.error(f"❌ Erreur lors du chargement du Seuil d'anomalie : {e}")

    _cached_models = models  # Stocke les modèles en cache pour éviter de les recharger plusieurs fois

    logging.info(f"📌 {len(models)} modèles chargés avec succès.")
    return models
