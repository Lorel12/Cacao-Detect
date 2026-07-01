"""
Première migration - créer les tables de base
"""
from alembic import op
import sqlalchemy as sa


revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Créer les tables initiales"""
    
    # Table utilisateurs
    op.create_table(
        'utilisateurs',
        sa.Column('id_utilisateur', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('nom', sa.String(100), nullable=False),
        sa.Column('prenom', sa.String(100), nullable=False),
        sa.Column('mot_de_passe_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('statut', sa.Boolean(), default=True),
        sa.Column('date_inscription', sa.DateTime(), nullable=False),
        sa.Column('dernier_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id_utilisateur'),
        sa.Index('idx_utilisateurs_email', 'email'),
    )
    
    # Table maladies
    op.create_table(
        'maladies',
        sa.Column('id_maladie', sa.Integer(), nullable=False),
        sa.Column('nom_maladie', sa.String(100), nullable=False, unique=True),
        sa.Column('agent_causal', sa.String(200), nullable=False),
        sa.Column('organes_touches', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('symptomes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id_maladie'),
    )
    
    # Table recommandations
    op.create_table(
        'recommandations',
        sa.Column('id_recommandation', sa.Integer(), nullable=False),
        sa.Column('id_maladie', sa.Integer(), nullable=False),
        sa.Column('traitement', sa.String(200), nullable=False),
        sa.Column('produit', sa.String(100), nullable=False),
        sa.Column('dosage', sa.String(100), nullable=False),
        sa.Column('frequence', sa.String(100), nullable=False),
        sa.Column('source', sa.String(200), nullable=True),
        sa.PrimaryKeyConstraint('id_recommandation'),
        sa.ForeignKeyConstraint(['id_maladie'], ['maladies.id_maladie']),
    )
    
    # Table analyses
    op.create_table(
        'analyses',
        sa.Column('id_analyse', sa.Integer(), nullable=False),
        sa.Column('id_utilisateur', sa.Integer(), nullable=False),
        sa.Column('date_heure', sa.DateTime(), nullable=False),
        sa.Column('statut', sa.String(50), nullable=False),
        sa.Column('duree_traitement_s', sa.Float(), nullable=True),
        sa.Column('flag_avertissement', sa.Boolean(), default=False),
        sa.Column('notes_utilisateur', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id_analyse'),
        sa.ForeignKeyConstraint(['id_utilisateur'], ['utilisateurs.id_utilisateur']),
        sa.Index('idx_analyses_utilisateur', 'id_utilisateur'),
        sa.Index('idx_analyses_date', 'date_heure'),
    )
    
    # Table images
    op.create_table(
        'images',
        sa.Column('id_image', sa.Integer(), nullable=False),
        sa.Column('id_analyse', sa.Integer(), nullable=False),
        sa.Column('chemin_local', sa.String(500), nullable=True),
        sa.Column('url_s3', sa.String(500), nullable=True),
        sa.Column('mimetype', sa.String(50), nullable=False),
        sa.Column('taille_bytes', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id_image'),
        sa.ForeignKeyConstraint(['id_analyse'], ['analyses.id_analyse']),
    )
    
    # Table diagnostics
    op.create_table(
        'diagnostics',
        sa.Column('id_diagnostic', sa.Integer(), nullable=False),
        sa.Column('id_analyse', sa.Integer(), nullable=False),
        sa.Column('id_maladie', sa.Integer(), nullable=True),
        sa.Column('niveau_gravite', sa.String(50), nullable=True),
        sa.Column('score_confiance', sa.Float(), nullable=False),
        sa.Column('bbox', sa.String(500), nullable=True),
        sa.Column('chemin_image_annotee', sa.String(500), nullable=True),
        sa.Column('flag_avertissement', sa.Boolean(), default=False),
        sa.Column('temps_inference_ms', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id_diagnostic'),
        sa.ForeignKeyConstraint(['id_analyse'], ['analyses.id_analyse']),
        sa.ForeignKeyConstraint(['id_maladie'], ['maladies.id_maladie']),
    )
    
    # Table modeles_ia
    op.create_table(
        'modeles_ia',
        sa.Column('id_modele', sa.Integer(), nullable=False),
        sa.Column('version', sa.String(50), nullable=False, unique=True),
        sa.Column('chemin_fichier', sa.String(500), nullable=False),
        sa.Column('accuracy', sa.Float(), nullable=True),
        sa.Column('precision', sa.Float(), nullable=True),
        sa.Column('recall', sa.Float(), nullable=True),
        sa.Column('date_deploiement', sa.DateTime(), nullable=False),
        sa.Column('actif', sa.Integer(), default=1),
        sa.PrimaryKeyConstraint('id_modele'),
    )


def downgrade():
    """Supprimer les tables"""
    op.drop_table('modeles_ia')
    op.drop_table('diagnostics')
    op.drop_table('images')
    op.drop_table('analyses')
    op.drop_table('recommandations')
    op.drop_table('maladies')
    op.drop_table('utilisateurs')
