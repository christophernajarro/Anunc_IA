from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ..auth_service.models import Usuario
from ..ai_content_service.models import Documento
from .utils import generar_respuesta_openai, extraer_json_de_respuesta
from fastapi import HTTPException
import json

async def manejar_definir_campana(data, current_user: Usuario, db: Session):
    prompt = f"""
    Como experto en marketing digital y campañas de Meta Ads, proporciona tus recomendaciones en formato JSON **válido** siguiendo exactamente el siguiente esquema **sin agregar texto adicional**:

    {{"detalles_campana": {{
        "objetivo_campana": {{
            "objetivo": "[Objetivo seleccionado]",
            "explicacion": "[Explicación breve]"
        }},
        "presupuesto_total": {{
            "cantidad": "[Cantidad en soles]",
            "explicacion": "[Explicación breve]"
        }},
        "duracion_optima": {{
            "duracion": "[Tiempo en días/semanas/meses]",
            "explicacion": "[Explicación breve]"
        }}
    }}}}

    Utiliza la información del producto a continuación para hacer tus recomendaciones.

    **Detalles del Producto:**
    - Nombre: {data.nombreProducto}
    - Descripción: {data.descripcionProducto}
    - tipoCampana: {data.tipoCampana}
    - duracionPreferida: {data.duracionPreferida}

    **Importante**: Proporciona **solo** la respuesta en formato JSON válido. No incluyas ninguna explicación o texto adicional antes o después del JSON.
    """

    resultado = await generar_respuesta_openai(prompt)
    detalles_campana = extraer_json_de_respuesta(resultado)

    # Manejo de la base de datos con un bloque de transacción explícito
    nuevo_documento = Documento(
        id_usuario=current_user.id_usuario,
        tipo_documento="definir_campana",
        contenido=json.dumps(detalles_campana),
        fecha_creacion=datetime.now(timezone.utc)
    )
    db.add(nuevo_documento)
    db.commit()
    db.refresh(nuevo_documento)

    return detalles_campana

async def manejar_definir_publico_ubicaciones(data, current_user: Usuario, db: Session):
    prompt = f"""
    Como estratega de marketing enfocado en segmentación y ubicaciones de anuncios en Meta Ads, proporciona tus recomendaciones en formato JSON **válido** siguiendo exactamente el siguiente esquema **sin agregar texto adicional**:

    {{
      "publico_objetivo": {{
        "demografico": {{
          "edad": "[Rango de edad]",
          "genero": "[Género(s)]",
          "ubicaciones": [
            {{
              "distrito": "[Distrito 1]",
              "provincia": "[Provincia 1]",
              "departamento": "[Departamento 1]"
            }},
            "... (más ubicaciones si es necesario)"
          ],
          "otros": "[Otros datos demográficos clave]"
        }},
        "psicografico": {{
          "intereses": "[Intereses específicos relacionados con el producto]",
          "comportamientos": "[Comportamientos de compra y otros]"
        }}
      }},
      "ubicaciones_anuncios": {{
        "ubicaciones_seleccionadas": ["[Ubicación 1]", "..."],
        "justificacion": "[Explicación breve de por qué se eligieron estas ubicaciones]"
      }}
    }}

    Utiliza la información del producto y las ubicaciones base a continuación para hacer tus recomendaciones.

    **Detalles del Producto:**
    - Nombre: {data.nombreProducto}
    - Descripción: {data.descripcionProducto}

    **Ubicaciones Base:**
    - Distrito: {data.distrito}
    - Provincia: {data.provincia}
    - Departamento: {data.departamento}

    **Importante**: Proporciona **solo** la respuesta en formato JSON válido. No incluyas ninguna explicación o texto adicional antes o después del JSON.

    **Nota**: Asegúrate de que todas las cadenas en el JSON estén entre comillas dobles y que el JSON sea estructuralmente válido.
    """

    resultado = await generar_respuesta_openai(prompt)
    publico_ubicaciones = extraer_json_de_respuesta(resultado)

    # Manejo de la base de datos con un bloque de transacción explícito
    nuevo_documento = Documento(
        id_usuario=current_user.id_usuario,
        tipo_documento="definir_publico_ubicaciones",
        contenido=json.dumps(publico_ubicaciones),
        fecha_creacion=datetime.now(timezone.utc)
    )
    db.add(nuevo_documento)
    db.commit()
    db.refresh(nuevo_documento)

    return publico_ubicaciones

async def manejar_elegir_formato_cta(data, current_user: Usuario, db: Session):
    prompt = f"""
    Como experto en creatividad publicitaria y plataformas de Meta Ads, proporciona tus recomendaciones en formato JSON **válido** siguiendo exactamente el siguiente esquema **sin agregar texto adicional**:

    {{
      "formato_anuncio": {{
        "formato": "[Formato seleccionado]",
        "explicacion": "[Explicación breve de por qué este formato es el más efectivo]"
      }},
      "cta": {{
        "llamada_a_la_accion": "[CTA seleccionada]",
        "explicacion": "[Explicación breve de por qué este CTA es el más impactante]"
      }}
    }}

    Utiliza las opciones predefinidas a continuación para hacer tus selecciones.

    **Opciones de Formato de Anuncio:**
    Anuncios en carrusel
    Anuncios en secuencia
    Colecciones
    Experiencias dinámicas
    Anuncios de Messenger
    Anuncios de Canvas 

    **Opciones de Llamada a la Acción (CTA):**
    Enviar solicitud
    Reservar
    Comprar
    Realizar pedido
    Cotizar
    Obtener oferta
    Más información
    Contactarnos
    Descargar
    Registrarte

    **Detalles del Producto:**
    - Nombre: {data.nombreProducto}
    - Descripción: {data.descripcionProducto}

    **Importante**: Proporciona **solo** la respuesta en formato JSON válido. No incluyas ninguna explicación o texto adicional antes o después del JSON.

    **Nota**: Asegúrate de que todas las cadenas en el JSON estén entre comillas dobles y que el JSON sea estructuralmente válido.
    """

    resultado = await generar_respuesta_openai(prompt)
    formato_y_cta = extraer_json_de_respuesta(resultado)

    # Manejo de la base de datos con un bloque de transacción explícito
    nuevo_documento = Documento(
        id_usuario=current_user.id_usuario,
        tipo_documento="elegir_formato_cta",
        contenido=json.dumps(formato_y_cta),
        fecha_creacion=datetime.now(timezone.utc)
    )
    db.add(nuevo_documento)
    db.commit()
    db.refresh(nuevo_documento)

    return formato_y_cta

async def manejar_crear_contenido_creativo(data, current_user: Usuario, db: Session):
    prompt = f"""
    Como redactor creativo especializado en anuncios de Meta Ads, genera **contenido publicitario persuasivo y atractivo** para "{data.nombreProducto}" en formato JSON **válido**, siguiendo exactamente el siguiente esquema **sin agregar texto adicional**:

    {{
      "variaciones": [
        {{
          "titulo": "[Título de la variación 1]",
          "contenido": "[Contenido de la variación 1]"
        }},
        {{
          "titulo": "[Título de la variación 2]",
          "contenido": "[Contenido de la variación 2]"
        }},
        {{
          "titulo": "[Título de la variación 3]",
          "contenido": "[Contenido de la variación 3]"
        }}
      ]
    }}

    El contenido debe:

    - Resaltar las **características y beneficios clave** del producto.
    - Adaptarse al **tono y estilo** especificado: "{data.tonoEstilo}".
    - Alinear el mensaje con los **intereses y necesidades** del público objetivo: "{data.publicoObjetivo}".
    - Utilizar un lenguaje que **resuene** con la audiencia y **genere una conexión emocional**.

    **Detalles del Producto:**
    - Nombre: {data.nombreProducto}
    - Descripción: {data.descripcionProducto}

    **Importante**: Proporciona **solo** la respuesta en formato JSON válido. No incluyas ninguna explicación o texto adicional antes o después del JSON.

    **Nota**: Asegúrate de que todas las cadenas en el JSON estén entre comillas dobles y que el JSON sea estructuralmente válido.
    """

    resultado = await generar_respuesta_openai(prompt)
    contenido_creativo = extraer_json_de_respuesta(resultado)

    # Manejo de la base de datos con un bloque de transacción explícito
    nuevo_documento = Documento(
        id_usuario=current_user.id_usuario,
        tipo_documento="crear_contenido_creativo",
        contenido=json.dumps(contenido_creativo),
        fecha_creacion=datetime.now(timezone.utc)
    )
    db.add(nuevo_documento)
    db.commit()
    db.refresh(nuevo_documento)

    return contenido_creativo

async def manejar_create_heading(encabezado, current_user: Usuario, db: Session):
    prompt = f"""
    Eres un redactor publicitario experto en crear **encabezados cautivadores** para anuncios en plataformas de redes sociales.

    Tu tarea es generar **encabezados concisos y atractivos** que cumplan con los siguientes requisitos y proporcionarlos en formato JSON **válido** siguiendo exactamente el siguiente esquema **sin agregar texto adicional**:

    {{
      "encabezados": [
        "Encabezado 1",
        "Encabezado 2",
        "... hasta {encabezado.variantes} encabezados"
      ]
    }}

    Un ejemplo de respuesta es este el cual podrias copiar el formato:
    {{
      "encabezados": [
        "¡Descubre los beneficios únicos de nuestro String!",
        "String: la solución perfecta para tus necesidades",
        "Mejora tu vida con String",
        "String: la mejor opción para ti",
        "¡Aprovecha las propuestas de valor de String ahora mismo!"
      ]
    }}

    Los encabezados deben:

    1. **Producto**: Estar optimizados para "{encabezado.nombreProducto}", destacando sus **beneficios** y **propuestas de valor únicas**.

    2. **Palabras Clave**: Incorporar las siguientes palabras clave para mejorar la optimización y relevancia del encabezado: {', '.join(encabezado.palabrasClave)}.

    3. **Estilo de Escritura**: Adaptarse al estilo de escritura especificado, que es "{encabezado.estiloEscritura}".

    4. **Longitud Máxima**: Limitarse a un máximo de {encabezado.longitudMaxima} caracteres, asegurando **claridad** y **poder de atracción**.

    5. **Variantes**: Proporcionar {encabezado.variantes} versiones únicas del encabezado, cada una manteniendo el tono y relevancia para el producto, pero explorando diferentes enfoques creativos.

    **Detalles del Producto:**
    - Nombre: {encabezado.nombreProducto}
    - Descripción: {encabezado.descripcionProducto}

    **Importante**: Proporciona **solo** la respuesta en formato JSON válido, sin incluir texto adicional antes o después del JSON.

    **Nota**: Asegúrate de que todas las cadenas en el JSON estén entre comillas dobles y que el JSON sea estructuralmente válido.
    """

    resultado = await generar_respuesta_openai(prompt)
    encabezados_data = extraer_json_de_respuesta(resultado)
    encabezados = encabezados_data.get("encabezados", [])[:encabezado.variantes]

    # Manejo de la base de datos con un bloque de transacción explícito
    nuevo_documento = Documento(
        id_usuario=current_user.id_usuario,
        tipo_documento="create_heading",
        contenido=json.dumps(encabezados),
        fecha_creacion=datetime.now(timezone.utc)
    )
    db.add(nuevo_documento)
    db.commit()
    db.refresh(nuevo_documento)

    return {"encabezados": encabezados}
