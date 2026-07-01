#!/bin/bash
# Quick start script for CacaoDetect Backend

echo "🚀 CacaoDetect Backend - Quick Start"
echo "===================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "✓ Python trouvé: $(python3 --version)"

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activate venv
echo "✓ Activation de l'environnement virtuel..."
source venv/bin/activate

# Install requirements
echo "📚 Installation des dépendances..."
pip install -q -r requirements.txt

# Run diagnostics
echo ""
echo "🔍 Diagnostic..."
python3 diagnose.py

echo ""
echo "✓ Configuration complète!"
echo ""
echo "Pour démarrer le serveur:"
echo "  source venv/bin/activate  # Si pas déjà activé"
echo "  python startup.py"
echo ""
echo "Pour accéder à l'API:"
echo "  - Documentation: http://localhost:8000/docs"
echo "  - Health check: http://localhost:8000/health"
