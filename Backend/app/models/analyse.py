from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, Text, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class StatutAnalyseEnum(str, enum.Enum):
    EN_COURS = "en_cours"
    TERMINE = "termine"
    ERREUR = "erreur"


class GraviteEnum(str, enum.Enum):
    FAIBLE = "faible"
    MODERE = "modere"
    ELEVE = "eleve"


class Analyse:
    """Représente une analyse d'image"""
    
    __tablename__ = "analyses"
    
    id_analyse = Column(Integer, primary_key=True, index=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id_utilisateur"), nullable=False)
    date_heure = Column(DateTime, default=datetime.utcnow, nullable=False)
    statut = Column(Enum(StatutAnalyseEnum), default=StatutAnalyseEnum.EN_COURS, nullable=False)
    duree_traitement_s = Column(Float, nullable=True)
    flag_avertissement = Column(Boolean, default=False, nullable=False)
    notes_utilisateur = Column(Text, nullable=True)
    
    # Relations
    utilisateur = relationship("Utilisateur", back_populates="analyses")
    image = relationship("Image", uselist=False, back_populates="analyse")
    diagnostic = relationship("Diagnostic", uselist=False, back_populates="analyse")
    
    def __repr__(self):
        return f"<Analyse {self.id_analyse} - {self.statut}>"


class Image:
    """Représente une image uploadée"""
    
    __tablename__ = "images"
    
    id_image = Column(Integer, primary_key=True, index=True)
    id_analyse = Column(Integer, ForeignKey("analyses.id_analyse"), nullable=False)
    chemin_local = Column(String(500), nullable=True)
    url_s3 = Column(String(500), nullable=True)
    mimetype = Column(String(50), nullable=False)
    taille_bytes = Column(Integer, nullable=False)
    
    # Relations
    analyse = relationship("Analyse", back_populates="image")
    
    def __repr__(self):
        return f"<Image {self.id_image}>"


class Diagnostic:
    """Représente le résultat du diagnostic IA"""
    
    __tablename__ = "diagnostics"
    
    id_diagnostic = Column(Integer, primary_key=True, index=True)
    id_analyse = Column(Integer, ForeignKey("analyses.id_analyse"), nullable=False)
    id_maladie = Column(Integer, ForeignKey("maladies.id_maladie"), nullable=True)
    niveau_gravite = Column(Enum(GraviteEnum), nullable=True)
    score_confiance = Column(Float, nullable=False)
    bbox = Column(String(500), nullable=True)  # JSON stringifié
    chemin_image_annotee = Column(String(500), nullable=True)
    flag_avertissement = Column(Boolean, default=False, nullable=False)
    temps_inference_ms = Column(Integer, nullable=True)
    
    # Relations
    analyse = relationship("Analyse", back_populates="diagnostic")
    maladie = relationship("Maladie", back_populates="diagnostics")
    
    def __repr__(self):
        return f"<Diagnostic {self.id_diagnostic}>"
