import re
import json
import logging
from fastapi import HTTPException
from .config import client

logger = logging.getLogger(__name__)

async def generar_respuesta_openai(prompt: str, max_tokens: int = 300) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Puedes cambiar al modelo que prefieras
            messages=[
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        # Acceder al contenido de la respuesta
        resultado = ''.join([
            choice.message.content for choice in response.choices
            if choice.message and choice.message.content
        ]).strip()
        return resultado
    except Exception as e:
        logger.exception("Error en generar_respuesta_openai")
        raise HTTPException(status_code=500, detail=f"Error en la llamada a OpenAI: {str(e)}")

def extraer_json_de_respuesta(respuesta: str) -> dict:
    if not isinstance(respuesta, str):
        raise HTTPException(status_code=500, detail="La respuesta no es un string válido.")

    try:
        # Intentar cargar toda la respuesta como JSON
        data = json.loads(respuesta)
        return data
    except json.JSONDecodeError:
        # Si falla, buscar el primer objeto JSON en la respuesta
        match = re.search(r'\{(?:[^{}]|(?R))*\}', respuesta, re.DOTALL)
        if match:
            json_str = match.group()
            try:
                data = json.loads(json_str)
                return data
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al parsear JSON: {e.msg}\nRespuesta del modelo:\n{respuesta}"
                )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"No se pudo encontrar un JSON válido en la respuesta.\nRespuesta del modelo:\n{respuesta}"
            )
