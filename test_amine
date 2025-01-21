Voici une version mise à jour de ton fichier `README.md` en fonction de la nouvelle structure de ton projet :

---

# ProjetSynthese

## Description
**ProjetSynthese** est une solution de maintenance prédictive basée sur l'analyse des séries temporelles. Elle utilise des outils de gestion de données, d’apprentissage automatique et de déploiement pour permettre une maintenance proactive des équipements critiques.

## Fonctionnalités principales
- **Maintenance prédictive** : Modèles de classification et de régression pour anticiper les pannes des équipements.
- **Imputation des données manquantes** : Remplissage intelligent des valeurs absentes via des modèles avancés.
- **Exploration des données (EDA)** : Visualisation et analyse détaillée des séries temporelles.
- **Détection d'anomalies** : Identification des comportements inhabituels grâce à des algorithmes de machine learning.
- **Déploiement API** : Interface REST pour l'interaction avec les modèles de prédiction et d'imputation.
- **Visualisation et monitoring** : Intégration de Prometheus et Grafana pour le suivi des performances.

---

## Structure du projet

```
ProjetSynthese/
│   .dvcignore                   # Ignore certains fichiers pour DVC
│   .gitignore                    # Fichiers ignorés par Git
│   data.dvc                      # Fichiers suivis par DVC
│   dvc.yaml                      # Pipeline de gestion des données
│   pytest.ini                     # Configuration des tests unitaires
│   README.md                      # Documentation principale
│   requirements.txt               # Dépendances du projet
│   requirements_dev.txt            # Dépendances pour le développement
│   run.py                         # Script principal
│   run_flask.py                    # Lancement de l'API Flask
│   structure_projet.txt            # Description de la structure du projet
│
├───.dvc/                          # Dossiers internes de DVC
│   │   .gitignore                  # Ignorer les caches
│   │   config                       # Configuration DVC
│   ├───cache/                       # Cache des fichiers suivis
│   └───tmp/                         # Fichiers temporaires
│
├───.github/workflows/              # CI/CD avec GitHub Actions
│       ci_cd.yaml                   # Définition du pipeline CI/CD
│
├───.idea/                           # Configuration de l'IDE PyCharm (à ignorer)
│
├───.pytest_cache/                   # Cache des tests unitaires
│
├───backend/                         # Code de l'application backend
│   │   models_loader.py              # Chargement des modèles
│   │   __init__.py                    # Initialisation du module
│   ├───routes/                        # Endpoints de l'API
│   │   ├── general.py                  # Routes générales
│   │   ├── imputation.py               # Route pour l’imputation
│   │   └── __init__.py
│   ├───utils/                          # Fonctions utilitaires
│   │   ├── data_processing.py           # Prétraitement des données
│   │   └── __init__.py
│   └───__pycache__/                     # Cache Python (à ignorer)
│
├───data/                              # Dossier des données
│   ├───models/                         # Modèles pré-entraînés
│   ├───processed/                       # Données traitées
│   └───raw/                             # Données brutes
│
├───docker/                             # Fichiers de configuration Docker
│   ├── docker-compose.yml               # Déploiement multi-conteneurs
│   └── Dockerfile                        # Fichier de construction d'image Docker
│
├───frontend/                           # Interface utilisateur
│   ├── app.py                           # Application Streamlit
│   └── components/                       # Composants de l'application
│
├───keys/                               # Clés d'authentification (à ignorer)
│       CleDVCJason.json
│
├───mlruns/                             # Logs des expériences MLflow
│
├───notebooks/                          # Notebooks Jupyter pour l'analyse et le développement
│   ├───eda/                             # Analyse exploratoire des données
│   │       EDA.ipynb
│   ├───modele_classification/           # Modèles de classification
│   │       Model_1_LSTM.ipynb
│   │       Model_1_Random_Forest.ipynb
│   │       Model_1_TSS_POC_1.ipynb
│   ├───modele_regression/               # Modèles de régression
│   │       Model_2_LightGBM.ipynb
│   │       Model_2_XGBoost.ipynb
│   └───preprocessing/                    # Étapes de prétraitement des données
│           Imputation.ipynb
│           Preprocessing.ipynb
│
├───scripts/                             # Scripts de gestion des modèles
│       evaluate_model.py                 # Évaluation des modèles
│       train_model.py                     # Entraînement des modèles
│
└───tests/                               # Tests unitaires
        test_api_handler.py
        test_imputation.py
        test_models_loader.py
```

---

## Prérequis

- **Python** : Version 3.8 ou supérieure
- **Outils** :
  - `pip`, `virtualenv` pour la gestion des packages
  - `Docker` et `Docker Compose` pour le déploiement
  - `DVC` pour la gestion des données

---

## Installation

1. **Cloner le projet :**
   ```bash
   git clone https://github.com/nidhel/Projet_synthese.git
   cd ProjetSynthese
   ```

2. **Créer un environnement virtuel et installer les dépendances :**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Pour Linux/Mac
   venv\Scripts\activate      # Pour Windows
   pip install -r requirements.txt
   ```

3. **Configurer DVC pour récupérer les données :**
   ```bash
   dvc pull
   ```

4. **Lancer l'API Flask en local :**
   ```bash
   python run_flask.py
   ```

5. **Exécuter l'interface utilisateur Streamlit :**
   ```bash
   streamlit run frontend/app.py
   ```

---

## Déploiement avec Docker

Utilisez Docker pour déployer l'application :

```bash
docker-compose up --build
```

---

## Tests

Pour exécuter les tests unitaires, utilisez la commande :

```bash
pytest tests/
```

---

## Contribution

1. Créez une branche pour vos modifications :
   ```bash
   git checkout -b feature/nom-de-la-fonctionnalité
   ```

2. Effectuez vos modifications et testez-les localement.

3. Soumettez une Pull Request vers la branche `dev`.

---

## Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus de détails.

---
