# ============================================================================
# FILE: app.py
# ============================================================================
from flask import Flask, app
from flask_cors import CORS
from routes.api_routes import api_bp
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

def create_app():
    """Factory pour créer l'application Flask"""
    
    app = Flask(__name__)
     
    CORS(app)


    config = Config()
    
    # Configuration
    app.config.from_object(config)
    
    # Enregistrement des blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return {
            "message": "API LangChain SQL Agent",
            "version": "1.0.0",
            "endpoints": {
                "ask": "/api/ask",
                "tables": "/api/tables",
                "schema": "/api/schema/<table_name>",
                "health": "/api/health"
            }
        }
    
    logger.info("Application initialisée")
    
    return app

if __name__ == '__main__':
    app = create_app()
    config = Config()
    
    logger.info(f"Démarrage de l'application sur {config.FLASK_HOST}:{config.FLASK_PORT}")
    
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )