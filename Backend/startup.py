#!/usr/bin/env python
"""
Script de démarrage rapide pour le backend CacaoDetect

Usage:
    python startup.py          # Démarrer le serveur
    python startup.py --db     # Initialiser la BD
    python startup.py --help   # Aide
"""

import argparse
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent


def run_command(cmd, description):
    """Exécuter une commande et afficher le statut"""
    print(f" {description}...")
    result = subprocess.run(cmd, shell=True, cwd=ROOT_DIR)
    if result.returncode != 0:
        print(f"✗ Erreur: {description}")
        return False
    print(f"✓ {description}")
    return True


def start_server(debug=True, reload=True):
    """Démarrer le serveur FastAPI"""
    cmd = f"python -m uvicorn app.main:app"
    
    if reload:
        cmd += " --reload"
    
    if not debug:
        cmd += " --workers 4"
    
    cmd += " --host 0.0.0.0 --port 8000"
    
    print(f"\n Démarrage du serveur sur http://localhost:8000")
    print(f" Documentation: http://localhost:8000/docs")
    print(f" API: http://localhost:8000/api/v1\n")
    
    subprocess.run(cmd, shell=True, cwd=ROOT_DIR)


def init_database():
    """Initialiser la base de données"""
    success = True
    
    # Exécuter les migrations
    success &= run_command(
        "alembic upgrade head",
        "Exécution des migrations Alembic"
    )
    
    # Initialiser les données
    success &= run_command(
        "python alembic/seed_data.py",
        "Initialisation des données de test"
    )
    
    return success


def check_dependencies():
    """Vérifier que les dépendances sont installées"""
    try:
        import fastapi
        import pydantic
        return True
    except ImportError as e:
        print(f"✗ Erreur: Dépendance manquante - {e}")
        print("Installez les dépendances avec: pip install -r requirements.txt")
        return False


def main():
    parser = argparse.ArgumentParser(description="CacaoDetect Backend Startup")
    parser.add_argument(
        "--db", 
        action="store_true", 
        help="Initialiser la base de données"
    )
    parser.add_argument(
        "--production", 
        action="store_true", 
        help="Mode production (pas de rechargement automatique)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port d'écoute"
    )
    
    args = parser.parse_args()
    
    # Vérifier les dépendances
    if not check_dependencies():
        sys.exit(1)
    
    # Initialiser la BD si demandé
    if args.db:
        if not init_database():
            print("⚠ Certaines opérations ont échoué")
    
    # Démarrer le serveur
    start_server(debug=not args.production)


if __name__ == "__main__":
    main()
