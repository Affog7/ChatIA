# ============================================================================
# FILE: utils/response_formatter.py
# ============================================================================
from typing import Dict, Any, Optional

class ResponseFormatter:
    """Formateur de réponses API"""
    
    @staticmethod
    def success(data: Dict[str, Any], message: str = "Success") -> Dict[str, Any]:
        """Formate une réponse de succès"""
        return {
            "success": True,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error(error_message: str, status_code: int = 500) -> tuple:
        """Formate une réponse d'erreur"""
        return {
            "success": False,
            "error": error_message,
            "status_code": status_code
        }, status_code
    
    @staticmethod
    def format_question_response(
        question: str,
        answer: str,
        sql: Optional[str] = None
    ) -> Dict[str, Any]:
        """Formate la réponse à une question"""
        return {
            "question": question,
            "answer": answer,
            "sql": sql if sql else "Requête SQL non disponible"
        }