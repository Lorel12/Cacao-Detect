#!/usr/bin/env python
"""
🚀 CacaoDetect - Quick Start Guide

Ce script affiche les instructions de démarrage pour le backend et le frontend.
"""

import sys
import os
from pathlib import Path

def print_header():
    print("""
╔════════════════════════════════════════════════════════════════╗
║                   🌱 CACAODETECT QUICK START 🌱                ║
║              Système de Détection de Maladies IA               ║
╚════════════════════════════════════════════════════════════════╝
    """)

def print_section(title):
    print(f"\n{'='*65}")
    print(f"  {title}")
    print(f"{'='*65}\n")

def check_prerequisites():
    """Vérifier les prérequis"""
    print_section("✓ VÉRIFICATION DES PRÉREQUIS")
    
    checks = []
    
    # Python
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print("  ✓ Python 3.9+ détecté")
        checks.append(True)
    else:
        print(f"  ✗ Python 3.9+ requis (vous avez {version.major}.{version.minor})")
        checks.append(False)
    
    # Node.js (check)
    try:
        import subprocess
        subprocess.run(["node", "--version"], capture_output=True, check=True)
        print("  ✓ Node.js détecté")
        checks.append(True)
    except:
        print("  ⚠ Node.js non détecté (requis pour le frontend)")
        checks.append(False)
    
    # Git
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print("  ✓ Git détecté")
        checks.append(True)
    except:
        print("  ⚠ Git non détecté (optionnel)")
    
    return all(checks)

def backend_setup():
    """Instructions pour le backend"""
    print_section("1️⃣  DÉMARRER LE BACKEND (Port 8000)")
    
    print("""
  Ouvrir un PREMIER terminal:
  
  $ cd Backend
  $ python -m venv venv
  
  Sur Windows:
    venv\\Scripts\\activate.bat
  
  Sur Linux/Mac:
    source venv/bin/activate
  
  $ pip install -r requirements.txt
  $ python diagnose.py          # Vérifier les dépendances
  $ python startup.py           # Démarrer le serveur
  
  ✅ Vous devriez voir:
    Uvicorn running on http://0.0.0.0:8000
    
  📖 Documentation interactive:
    http://localhost:8000/docs
    """)

def frontend_setup():
    """Instructions pour le frontend"""
    print_section("2️⃣  DÉMARRER LE FRONTEND (Port 3001)")
    
    print("""
  Ouvrir un DEUXIÈME terminal:
  
  $ cd Frontend
  $ npm install                  # (Si pas déjà fait)
  $ npm start
  
  ✅ Vous devriez voir:
    Compiled successfully!
    
  🌐 Accès application:
    http://localhost:3001
    """)

def usage_guide():
    """Guide d'utilisation"""
    print_section("3️⃣  UTILISER L'APPLICATION")
    
    print("""
  1. Ouvrir http://localhost:3001 dans le navigateur
  
  2. Créer un compte:
     - Email: user@example.com
     - Mot de passe: Mot123!Pass
     - Rôle: Agriculteur / Agronome / Chercheur
  
  3. Tester le diagnostic:
     - Upload une image JPG/PNG de feuille
     - Voir le résultat IA avec:
       * Maladie détectée
       * Niveau de gravité
       * Score de confiance
       * Recommandations de traitement
  
  4. Voir l'historique:
     - Toutes les analyses précédentes
     - Filtrer par maladie, gravité, date
     - Exporter en PDF
  
  5. Admin (si accès):
     - Voir tous les utilisateurs
     - Statistiques globales
     - Déployer nouveau modèle IA
    """)

def architecture_overview():
    """Architecture du système"""
    print_section("🏗️  ARCHITECTURE DU SYSTÈME")
    
    print("""
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │  Frontend (React)          Backend (FastAPI)           │
  │  Port 3001                 Port 8000                   │
  │  ┌──────────┐              ┌──────────┐               │
  │  │ React 19 │◄────JWT────►│ FastAPI  │               │
  │  │ App      │  (Bearer)   │ API      │               │
  │  └──────────┘              └──────────┘               │
  │       │                          │                    │
  │       │ Tailwind CSS            │ SQLAlchemy        │
  │       │ React Router            │ Pydantic          │
  │       │ Axios + Auth            │ Alembic           │
  │       │                         │                    │
  │  ┌──────────────────────────────────────┐             │
  │  │    PostgreSQL Database               │             │
  │  │    - Utilisateurs                    │             │
  │  │    - Analyses                        │             │
  │  │    - Diagnostics                     │             │
  │  │    - Maladies                        │             │
  │  └──────────────────────────────────────┘             │
  │                                                         │
  │  ┌──────────────────────────────────────┐             │
  │  │    AI Model                          │             │
  │  │    - TensorFlow/PyTorch              │             │
  │  │    - Plant disease detection         │             │
  │  │    - Inference on upload             │             │
  │  └──────────────────────────────────────┘             │
  │                                                         │
  └─────────────────────────────────────────────────────────┘
    """)

def troubleshooting():
    """Dépannage courant"""
    print_section("🔧 DÉPANNAGE")
    
    print("""
  ❌ "Port 8000 already in use"
     $ python -m uvicorn app.main:app --port 8001
  
  ❌ "ModuleNotFoundError: No module named 'fastapi'"
     $ pip install -r requirements.txt
  
  ❌ "Connection refused" (Backend non accessible)
     Vérifier que: python startup.py est en cours d'exécution
  
  ❌ "npm install fails"
     Vérifier: Node.js est installé (node --version)
     Vérifier: npm est à jour (npm install -g npm@latest)
  
  ❌ Login échoue
     Backend doit être en cours d'exécution
     Vérifier l'email et mot de passe (validation côté serveur)
  
  ❌ Upload d'image échoue
     Max 10 Mo, formats: JPG/PNG uniquement
    """)

def next_steps():
    """Prochaines étapes"""
    print_section("📚 PROCHAINES ÉTAPES")
    
    print("""
  ✓ Si tout fonctionne:
    1. Tester la création de compte
    2. Tester l'upload d'image
    3. Vérifier l'historique
  
  ⏳ Développement ultérieur:
    - Intégrer vrai modèle IA
    - Configurer S3 pour images
    - Ajouter notifications email
    - Déployer en production
  
  📖 Documentation complète:
    - Backend: Backend/README.md
    - Backend Installation: Backend/INSTALLATION.md
    - API Endpoints: Backend/API_DOCUMENTATION.md
    - Frontend: Frontend/README.md
    """)

def print_footer():
    print("""
╔════════════════════════════════════════════════════════════════╗
║                    ✨ PRÊT À DÉMARRER! ✨                      ║
║                                                                ║
║  Commandes rapides:                                           ║
║  ─────────────────────────────────────────────────────────    ║
║  Backend:  cd Backend && python startup.py                   ║
║  Frontend: cd Frontend && npm start                          ║
║                                                                ║
║  Accès:                                                        ║
║  ─────────────────────────────────────────────────────────    ║
║  App:  http://localhost:3001                                 ║
║  API:  http://localhost:8000                                 ║
║  Docs: http://localhost:8000/docs                            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)

def main():
    """Main function"""
    print_header()
    
    # Vérifications
    if not check_prerequisites():
        print("⚠️  Certains prérequis manquent - installation pourrait échouer")
    
    # Instructions
    backend_setup()
    frontend_setup()
    usage_guide()
    architecture_overview()
    troubleshooting()
    next_steps()
    print_footer()
    
    print("\n💡 Conseil: Garder les deux terminaux ouverts pendant le développement")
    print("   (Backend sur terminal 1, Frontend sur terminal 2)\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterruption. Au revoir! 👋")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)
