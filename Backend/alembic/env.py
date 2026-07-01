"""
Application Alembic SQLAlchemy, pour les migrations de base de données
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from app.core.config import settings

# Ceci est le objet Alembic config qui assure les valeurs
# de la section [alembic] du fichier alembic.ini.
config = context.config

# Interprète le fichier du config pour la logging Python
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Objet target_metadata sera déterminé en utilisant les ORM models
# pour les migrations autogénérées
target_metadata = None  # TODO: Récupérer les métadonnées des modèles


def run_migrations_offline() -> None:
    """Exécuter les migrations 'offline'"""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Exécuter les migrations 'online'"""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
