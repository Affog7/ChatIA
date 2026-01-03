# FILE: services/database_service.py
# ============================================================================
from langchain_community.utilities import SQLDatabase
from typing import List, Optional
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

class DatabaseService:
    """Service de gestion de la base de données"""
    
    _instance = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._db is None:
            self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialise la connexion à la base de données"""
        try:
            config = Config()
            self._db = SQLDatabase.from_uri(config.DATABASE_URI)
            logger.info("Connexion à la base de données établie")
        except Exception as e:
            logger.error(f"Erreur de connexion à la base de données: {e}")
            raise
    
    def get_database(self) -> SQLDatabase:
        """Retourne l'instance de la base de données"""
        return self._db
    
    def get_tables(self) -> List[str]:
        """Retourne la liste des tables"""
        try:
            return self._db.get_usable_table_names()
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des tables: {e}")
            raise
    
    def get_table_schema(self, table_name: str) -> str:
        """Retourne le schéma d'une table"""
        try:
            return self._db.get_table_info([table_name])
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du schéma: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Teste la connexion à la base de données"""
        try:
            self._db.get_usable_table_names()
            return True
        except Exception as e:
            logger.error(f"Test de connexion échoué: {e}")
            return False
