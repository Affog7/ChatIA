# ============================================================================
# FILE: routes/api_routes.py
# ============================================================================
from flask import Blueprint, request, jsonify
from agents.sql_agent import SQLAgentService
from services.database_service import DatabaseService
from utils.response_formatter import ResponseFormatter
from utils.logger import setup_logger

logger = setup_logger(__name__)

api_bp = Blueprint('api', __name__)

@api_bp.route('/ask', methods=['POST'])
def ask_question():
    """
    Endpoint pour interroger la base de données en langage naturel
    
    Body:
        {
            "question": "C'est qui Dupont ?"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return ResponseFormatter.error("La question est requise", 400)
        
        question = data.get('question')
        
        if not question or not question.strip():
            return ResponseFormatter.error("La question ne peut pas être vide", 400)
        
        # Interrogation de l'agent
        agent_service = SQLAgentService()
        result = agent_service.ask_question(question)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Erreur dans /ask: {e}")
        return ResponseFormatter.error(str(e))

@api_bp.route('/tables', methods=['GET'])
def get_tables():
    """Endpoint pour lister les tables disponibles"""
    try:
        db_service = DatabaseService()
        tables = db_service.get_tables()
        
        return jsonify(ResponseFormatter.success({
            "tables": tables
        })), 200
        
    except Exception as e:
        logger.error(f"Erreur dans /tables: {e}")
        return ResponseFormatter.error(str(e))

@api_bp.route('/schema/<table_name>', methods=['GET'])
def get_schema(table_name: str):
    """Endpoint pour obtenir le schéma d'une table"""
    try:
        db_service = DatabaseService()
        schema = db_service.get_table_schema(table_name)
        
        return jsonify(ResponseFormatter.success({
            "table": table_name,
            "schema": schema
        })), 200
        
    except Exception as e:
        logger.error(f"Erreur dans /schema: {e}")
        return ResponseFormatter.error(str(e))

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de vérification de santé"""
    try:
        db_service = DatabaseService()
        db_status = db_service.test_connection()
        
        return jsonify({
            "status": "healthy" if db_status else "unhealthy",
            "database": "connected" if db_status else "disconnected"
        }), 200 if db_status else 503
        
    except Exception as e:
        logger.error(f"Erreur dans /health: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 503
