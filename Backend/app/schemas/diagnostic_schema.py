from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class GraviteEnum(str, Enum):
    FAIBLE = "faible"
    MODERE = "modere"
    ELEVE = "eleve"


class StatutAnalyseEnum(str, Enum):
    EN_COURS = "en_cours"
    TERMINE = "termine"
    ERREUR = "erreur"


class RecommandationSchema(BaseModel):
    """Schéma de recommandation"""
    id_recommandation: int
    traitement: str
    produit: str
    dosage: str
    frequence: str
    source: Optional[str] = None
    
    class Config:
        from_attributes = True


class MaladieSchema(BaseModel):
    """Schéma de maladie"""
    id_maladie: int
    nom_maladie: str
    agent_causal: str
    organes_touches: str
    description: str
    recommandations: Optional[List[RecommandationSchema]] = []
    
    class Config:
        from_attributes = True


class DiagnosticSchema(BaseModel):
    """Schéma de diagnostic"""
    id_diagnostic: int
    maladie: Optional[MaladieSchema] = None
    niveau_gravite: Optional[GraviteEnum] = None
    score_confiance: float
    bbox: Optional[List[float]] = None
    chemin_image_annotee: Optional[str] = None
    flag_avertissement: bool = False
    
    class Config:
        from_attributes = True


class AnalyseSchema(BaseModel):
    """Schéma complet d'une analyse"""
    id_analyse: int
    date_heure: datetime
    statut: StatutAnalyseEnum
    duree_traitement_s: Optional[float] = None
    flag_avertissement: bool = False
    diagnostic: Optional[DiagnosticSchema] = None
    
    class Config:
        from_attributes = True


class AnalyseListItemSchema(BaseModel):
    """Schéma court pour liste d'analyses"""
    id_analyse: int
    date_heure: datetime
    statut: StatutAnalyseEnum
    maladie_nom: Optional[str] = None
    niveau_gravite: Optional[GraviteEnum] = None
    score_confiance: Optional[float] = None
    image_annotee_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class AnalysesListResponseSchema(BaseModel):
    """Réponse pour liste paginée d'analyses"""
    analyses: List[AnalyseListItemSchema]
    total: int
    page: int
    limit: int


class AnalysisFiltersSchema(BaseModel):
    """Filtres pour l'historique"""
    maladie: Optional[str] = None
    gravite: Optional[GraviteEnum] = None
    date_debut: Optional[str] = None
    date_fin: Optional[str] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
