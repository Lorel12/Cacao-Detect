from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship


class Maladie:
    """Représente une maladie du cacaoyer"""
    
    __tablename__ = "maladies"
    
    id_maladie = Column(Integer, primary_key=True, index=True)
    nom_maladie = Column(String(100), unique=True, nullable=False)
    agent_causal = Column(String(200), nullable=False)
    organes_touches = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    symptomes = Column(Text, nullable=True)
    
    # Relations
    recommandations = relationship("Recommandation", back_populates="maladie")
    diagnostics = relationship("Diagnostic", back_populates="maladie")
    
    def __repr__(self):
        return f"<Maladie {self.nom_maladie}>"


class Recommandation:
    """Représente une recommandation de traitement"""
    
    __tablename__ = "recommandations"
    
    id_recommandation = Column(Integer, primary_key=True, index=True)
    id_maladie = Column(Integer, ForeignKey("maladies.id_maladie"), nullable=False)
    traitement = Column(String(200), nullable=False)
    produit = Column(String(100), nullable=False)
    dosage = Column(String(100), nullable=False)
    frequence = Column(String(100), nullable=False)
    source = Column(String(200), nullable=True)
    
    # Relations
    maladie = relationship("Maladie", back_populates="recommandations")
    
    def __repr__(self):
        return f"<Recommandation {self.traitement}>"
