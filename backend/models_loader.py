import os
import joblib

def load_models():
    """Charge les modèles d'imputation."""
    model_dir = os.path.join(os.path.dirname(__file__), '../data/models')
    models = {}

    if not os.path.exists(model_dir):
        raise FileNotFoundError(f"Le répertoire des modèles {model_dir} n'existe pas.")

    for model_file in os.listdir(model_dir):
        if model_file.endswith('.pkl'):
            col_name = model_file.replace('lightgbm_imputer_', '').replace('.pkl', '')
            model_path = os.path.join(model_dir, model_file)

            try:
                model = joblib.load(model_path, mmap_mode=None)
                if not hasattr(model, 'get_params'):
                    raise ValueError(f"Le modèle {col_name} ne possède pas la méthode get_params.")
                models[col_name] = model
                print(f"✅ Modèle chargé : {col_name}")
            except Exception as e:
                print(f"❌ Erreur lors du chargement du modèle {model_file}: {e}")

    print(f"✅ {len(models)} modèles chargés avec succès.")
    return models
