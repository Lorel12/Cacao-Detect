"""
Service pour la gestion du stockage (local ou S3)
"""
import os
import logging
from typing import Optional
from pathlib import Path
from app.core.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    """Service d'upload et download de fichiers"""
    
    def __init__(self):
        self.use_s3 = settings.USE_S3
        self.upload_folder = settings.UPLOAD_FOLDER
        self.max_file_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
        
        # Créer le dossier local s'il n'existe pas
        if not self.use_s3:
            Path(self.upload_folder).mkdir(parents=True, exist_ok=True)
    
    def validate_file(self, filename: str, file_size: int) -> tuple[bool, str]:
        """Valide qu'un fichier est acceptable"""
        # Vérifier l'extension
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if ext not in self.allowed_extensions:
            return False, f"Format non supporté. Accepté: {self.allowed_extensions}"
        
        # Vérifier la taille
        if file_size > self.max_file_size:
            return False, f"Fichier trop volumineux (max {settings.MAX_FILE_SIZE_MB} Mo)"
        
        return True, ""
    
    def save_file_local(self, file_content: bytes, filename: str) -> str:
        """Sauvegarde un fichier localement et retourne son chemin"""
        try:
            filepath = os.path.join(self.upload_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(file_content)
            logger.info(f"Fichier sauvegardé: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du fichier: {e}")
            raise Exception(f"Erreur de sauvegarde: {e}")
    
    def save_file_s3(self, file_content: bytes, filename: str) -> str:
        """Sauvegarde un fichier sur S3 et retourne son URL"""
        if not self.use_s3:
            raise Exception("S3 n'est pas configuré")
        
        try:
            # TODO: Implémenter l'upload S3 avec boto3
            # Placeholder
            url = f"s3://{settings.S3_BUCKET}/{filename}"
            logger.info(f"Fichier sauvegardé sur S3: {url}")
            return url
        except Exception as e:
            logger.error(f"Erreur lors de l'upload S3: {e}")
            raise Exception(f"Erreur S3: {e}")
    
    def save_file(self, file_content: bytes, filename: str) -> str:
        """Sauvegarde un fichier selon la configuration"""
        if self.use_s3:
            return self.save_file_s3(file_content, filename)
        else:
            return self.save_file_local(file_content, filename)
    
    def delete_file(self, file_path: str) -> bool:
        """Supprime un fichier"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Fichier supprimé: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la suppression: {e}")
            return False


# Instance globale
storage_service = StorageService()
