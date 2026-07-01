"""
Script pour initialiser le modèle de données et remplir avec des données de test
"""
import sys
from pathlib import Path

# Ajouter le répertoire racine au path Python
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from app.core.security import hash_password


def init_database():
    """Initialise la base de données avec les données de test"""
    
    # TODO: Implémenter l'initialisation réelle
    # Ceci est un placeholder pour la structure
    
    # Créer l'administrateur par défaut
    admin_user = {
        "email": "admin@cacaodetect.com",
        "nom": "Admin",
        "prenom": "CacaoDetect",
        "mot_de_passe_hash": hash_password("admin123456"),
        "role": "administrateur",
        "statut": True,
        "date_inscription": datetime.utcnow(),
    }
    
    # Maladies communes du cacaoyer
    maladies = [
        {
            "nom_maladie": "Frosque",
            "agent_causal": "Crinipellis perniciosa",
            "organes_touches": "Feuilles, cabosses, tiges",
            "description": "Maladie dévastatrice causant une pourriture des cabosses",
            "symptomes": "Lésions brunes, pourriture des fruits",
        },
        {
            "nom_maladie": "Pourriture brune",
            "agent_causal": "Phytophthora spp.",
            "organes_touches": "Cabosses, tiges",
            "description": "Infection fongique affectant les cabosses",
            "symptomes": "Taches brunes sur les cabosses, brunissement",
        },
        {
            "nom_maladie": "Rouille noire",
            "agent_causal": "Ceratocystis fimbriata",
            "organes_touches": "Tiges, branches",
            "description": "Canker sur les tiges et branches",
            "symptomes": "Nécrose des tiges, dépérissement",
        },
    ]
    
    print("✓ Configuration des données de test prête")
    print(f"✓ Admin par défaut: {admin_user['email']}")
    print(f"✓ {len(maladies)} maladies référencées")


if __name__ == "__main__":
    init_database()
