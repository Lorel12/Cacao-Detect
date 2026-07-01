"""
Configuration générale pour Alembic.

Paramètres utiles editables par l'utilisateur:

- migration location
- sqlalchemy.url
- output file encoding
- Et plusieurs autres options de configuration
"""

from configparser import ConfigParser
import os
from logging.config import fileConfig

# chemin vers cet fichier de config
config = ConfigParser()
here = os.path.abspath(os.path.dirname(__file__))
config.read(os.path.join(here, 'alembic.ini'))

# Ensemble de valeurs par défaut:
file_config = fileConfig(config)
if file_config:
    for key in file_config.keys():
        if key == 'loggers':
            continue
        # Configure la sortie des logs
