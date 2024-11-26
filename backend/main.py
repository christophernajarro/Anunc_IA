# from ddtrace import patch_all, tracer
# patch_all()  # Habilita el trazado automático para todas las dependencias compatibles

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.ai_content_service.routes import router as ai_content_router
from services.auth_service.routes import router as auth_router
from services.user_service.routes import router as user_router
from services.document_service.routes import router as document_router
from services.product_service.routes import router as product_router
from services.meta_ads_service.routes import router as meta_ads_router
from dotenv import load_dotenv
import os
from mangum import Mangum  # Importar Mangum para Lambda
import logging
from fastapi.responses import JSONResponse

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

# Cargar las variables de entorno
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# # Configura el tracer de Datadog para FastAPI
# tracer.configure(
#     hostname=os.getenv("DD_AGENT_HOST", "localhost")  # Asegúrate de que apunte al Datadog Agent
# )

# Crear la instancia de FastAPI
app = FastAPI(
    debug=True,
    title="Anunc IA Backend",
    description="API para gestionar el backend de Anunc IA",
    version="1.0.0"
)

origins = ["http://localhost:8080"]

# origins = [
#     "http://localhost:8080",
#     "https://anuncia.tech",
#     # Añade otros orígenes si es necesario
# ]

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialización de servicios al iniciar la aplicación
@app.on_event("startup")
async def startup_event():
    from common.utils.session_manager import SessionManager
    try:
        await SessionManager.initialize_redis()
    except Exception as e:
        logger.error(f"Fallo en la inicialización de Redis: {e}")
        # Dependiendo de la lógica, podrías querer terminar la aplicación o manejar el error de otra manera

# Cierre de servicios al cerrar la aplicación
@app.on_event("shutdown")
async def shutdown_event():
    from common.utils.session_manager import SessionManager
    await SessionManager.close_redis()

# Incluir routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(ai_content_router, prefix="/content", tags=["ai_content"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(document_router, prefix="/documents", tags=["documents"])
app.include_router(product_router, prefix="/productos", tags=["productos"])
app.include_router(meta_ads_router, prefix="/meta_ads", tags=["meta_ads"])

# Ruta raíz para verificar que la API está funcionando
@app.get("/", response_class=JSONResponse)
async def root():
    return {"message": "Bienvenido a la API publicitaria"}

# Adaptador Mangum para ejecutar en AWS Lambda
handler = Mangum(app)

# Este bloque solo es necesario si deseas ejecutar la aplicación localmente con Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)