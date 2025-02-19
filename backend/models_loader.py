import os
import joblib
import tensorflow as tf

# Variable globale pour éviter de recharger les modèles plusieurs fois
_cached_models = None

def load_models(model_dir):
    """Charge les modèles d'imputation et de détection UNE SEULE FOIS."""
    global _cached_models
    if _cached_models is not None:
        return _cached_models  # Retourner directement si les modèles sont déjà en mémoire

    models = {}
    if not os.path.exists(model_dir):
        print(f"❌ Le répertoire des modèles {model_dir} n'existe pas.")
        return models

    for model_file in os.listdir(model_dir):
        model_path = os.path.join(model_dir, model_file)

        if model_file.endswith('.pkl'):
            col_name = model_file.replace('.pkl', '')
            try:
                models[col_name] = joblib.load(model_path)
                print(f"✅ Modèle chargé : {col_name}")
            except Exception as e:
                print(f"❌ Erreur lors du chargement du modèle {model_file}: {e}")

    # 🔹 Charger le modèle SAE
    sae_path = os.path.join(model_dir, "sae_trained.keras")
    if os.path.exists(sae_path):
        try:
            models["sae"] = tf.keras.models.load_model(sae_path)
            print("✅ Modèle SAE chargé avec succès !")
        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle SAE : {e}")

    # 🔹 Charger le Scaler
    scaler_path = os.path.join(model_dir, "scaler.pkl")
    if os.path.exists(scaler_path):
        try:
            models["scaler"] = joblib.load(scaler_path)
            print("✅ Scaler chargé avec succès !")
        except Exception as e:
            print(f"❌ Erreur lors du chargement du Scaler : {e}")

    # 🔹 Charger le seuil d'anomalie
    threshold_path = os.path.join(model_dir, "threshold_final.pkl")
    if os.path.exists(threshold_path):
        try:
            models["threshold"] = joblib.load(threshold_path)
            print(f"✅ Seuil d'anomalie chargé : {models['threshold']}")
        except Exception as e:
            print(f"❌ Erreur lors du chargement du Seuil d'anomalie : {e}")

    _cached_models = models  # Stocker les modèles en cache
    print(f"✅ {len(models)} modèles chargés avec succès.")
    return models
