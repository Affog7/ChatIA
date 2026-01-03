# ============================================================================
# FILE: agents/sql_agent.py
# ============================================================================
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from typing import Dict, Any, Optional
from config import Config
from services.database_service import DatabaseService
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SQLAgentService:
    """Service de l'agent SQL LangChain"""
    
    _instance = None
    _agent = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SQLAgentService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._agent is None:
            self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialise l'agent SQL"""
        try:
            config = Config()
            db_service = DatabaseService()
            
            # Configuration du LLM
            llm = ChatOpenAI(
                model=config.OPENAI_MODEL,
                temperature=0,
                api_key=config.OPENAI_API_KEY
            )
            
            # Création du toolkit SQL
            toolkit = SQLDatabaseToolkit(
                db=db_service.get_database(),
                llm=llm
            )
            
            # Création de l'agent avec le toolkit
            self._agent = create_sql_agent(
                llm=llm,
                toolkit=toolkit,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=10,
                agent_executor_kwargs={"return_intermediate_steps": True}
            )
            
            logger.info("Agent SQL initialisé avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de l'agent: {e}")
            raise
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """
        Pose une question à l'agent SQL
        
        Args:
            question: La question en langage naturel
            
        Returns:
            Dict contenant la réponse, la question et la requête SQL
        """
        try:
            logger.info(f"Question reçue: {question}")
            
            # Préfixe pour forcer la réponse en français
            question_with_instruction = f"{question}\n\nRAPPEL: Réponds toujours en français de manière naturelle et conversationnelle."
            
            # Exécution de la requête
            response = self._agent.invoke({"input": question_with_instruction})
            
            # Extraction de la réponse
            answer = response.get('output', '')
            
            # Extraction de la requête SQL
            sql_query = self._extract_sql_query(response)

            #logger.info(f"sql_query< ========> {sql_query}")
            
            logger.info(f"Réponse générée avec succès")
            
            return {
                "question": question,
                "answer": answer,
                "sql": sql_query
            }
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement de la question: {e}")
            raise
    
    def _extract_sql_query(self, response: Dict[str, Any]) -> Optional[str]:
        """Extrait la requête SQL depuis la réponse de l'agent"""
        try:
            sql_queries = []
            
            if 'intermediate_steps' in response:
                for step in response['intermediate_steps']:
                    if len(step) >= 2:
                        action = step[0]
                        observation = step[1]
                        
                        # Récupérer le nom de l'outil et l'input
                        tool_name = ""
                        tool_input = ""
                        
                        # L'action peut être un objet AgentAction ou un tuple
                        if hasattr(action, 'tool'):
                            tool_name = str(action.tool).lower()
                        if hasattr(action, 'tool_input'):
                            tool_input = str(action.tool_input)
                        
                        # Chercher spécifiquement l'outil 'sql_db_query' qui exécute le SQL
                        if 'sql_db_query' in tool_name and tool_input:
                            # Nettoyer la requête (enlever les guillemets de début/fin si présents)
                            clean_sql = tool_input.strip().strip('"').strip("'")
                            sql_queries.append(clean_sql)
                            logger.info(f"SQL trouvé via sql_db_query: {clean_sql}")
            
            # Retourner la dernière requête SQL trouvée (la requête finale exécutée)
            if sql_queries:
                return sql_queries[-1]
            
            logger.warning("Aucune requête SQL trouvée dans les intermediate_steps")
            return None
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction de la requête SQL: {e}", exc_info=True)
            return None
