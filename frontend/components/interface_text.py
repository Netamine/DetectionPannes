# frontend/components/interface_text.py

TEXT_INTRO = """
🔍 **Système de Prédiction des Pannes avec Imputation**  
🛠️ **Comment utiliser cette Interface ?**  
Cette interface permet de **tester manuellement** la prédiction des pannes.

🌐 **Système en production** : Un service web est disponible pour un usage industriel.

📩 **Vous devez téléverser un fichier CSV contenant des mesures de capteurs.**
"""

TEXT_CSV_CONDITIONS = """
📄 **Conditions du fichier CSV**  
✅ **Format accepté** : Un fichier CSV contenant **au moins 30 minutes de données**.  
✅ **Intervalle fixe** : Données relevées **toutes les 10 secondes** (soit 300 observations).  
✅ **Colonnes requises** :
"""

REQUIRED_COLUMNS = [
    "timestamp", "TP2", "TP3", "H1", "DV_pressure", "Reservoirs",
    "Oil_temperature", "Motor_current", "COMP", "DV_eletric",
    "Towers", "MPG", "LPS", "Pressure_switch", "Oil_level", "Caudal_impulses"
]
