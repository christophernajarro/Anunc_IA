import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Cargar las variables de entorno desde el archivo .env en la raíz del proyecto
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

# Verificar que la clave de API esté configurada
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY no está configurada en las variables de entorno.")
    raise ValueError("OPENAI_API_KEY no está configurada en las variables de entorno.")

# Crear una instancia del cliente de OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)
