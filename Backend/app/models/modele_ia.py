from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime


class ModeleIA:
    """Représente une version du modèle IA"""
    
    __tablename__ = "modeles_ia"
    
    id_modele = Column(Integer, primary_key=True, index=True)
    version = Column(String(50), unique=True, nullable=False)
    chemin_fichier = Column(String(500), nullable=False)
    accuracy = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    date_deploiement = Column(DateTime, default=datetime.utcnow, nullable=False)
    actif = Column(Integer, default=1, nullable=False)
    
    def __repr__(self):
        return f"<ModeleIA v{self.version}>"
