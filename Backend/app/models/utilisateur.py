from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class RoleEnum(str, enum.Enum):
    AGRICULTEUR = "agriculteur"
    AGRONOME = "agronome"
    CHERCHEUR = "chercheur"
    ADMINISTRATEUR = "administrateur"


class Utilisateur:
    """Représente un utilisateur de l'application"""
    
    __tablename__ = "utilisateurs"
    
    id_utilisateur = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    mot_de_passe_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.AGRICULTEUR, nullable=False)
    statut = Column(Boolean, default=True, nullable=False)
    date_inscription = Column(DateTime, default=datetime.utcnow, nullable=False)
    dernier_login = Column(DateTime, nullable=True)
    
    # Relations
    analyses = relationship("Analyse", back_populates="utilisateur")
    
    def __repr__(self):
        return f"<Utilisateur {self.prenom} {self.nom}>"
