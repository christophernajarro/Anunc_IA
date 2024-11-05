from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from .models import CampanaDetallesInput, PublicoObjetivoUbicacionesInput, FormatoCTAInput, ContenidoCreativoInput, EncabezadoAnuncio

# Cargar las variables de entorno desde el archivo .env en la carpeta config
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

# Crear una instancia del cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Crear el router de FastAPI
router = APIRouter()

# Endpoint 1: Definir el objetivo de la campaña y detalles como presupuesto y duración
@router.post("/definir_campana")
async def definir_campana(data: CampanaDetallesInput):
    prompt = f"""
Como experto en marketing digital y campañas de Meta Ads, tu tarea es:

1. **Seleccionar el objetivo de campaña más adecuado** para "{data.nombreProducto}" de entre los objetivos predefinidos por Meta (por ejemplo, 'Reconocimiento de marca', 'Tráfico', 'Interacciones', 'Conversiones', etc.).

    Considera:
    - **Beneficios únicos** y **características diferenciadoras** de "{data.nombreProducto}".
    - **Necesidades y deseos** del público objetivo.
    - **Objetivos comerciales** de la empresa.

2. **Recomendar un presupuesto total** que maximice el retorno de inversión (ROI) para la campaña, basado en:
    - **Tipo de campaña**: {data.tipoCampana}.
    - **Duración preferida**: {data.duracionPreferida}.

3. **Determinar la duración óptima** de la campaña en días, semanas o meses, considerando:
    - **Objetivos de marketing** y **expectativas de rendimiento**.
    - **Sector del producto**, **comportamiento del consumidor** y **prácticas actuales del mercado**.

Proporciona tu respuesta en un formato claro y estructurado, explicando brevemente las razones detrás de cada recomendación.

**Detalles del Producto:**
- Nombre: {data.nombreProducto}
- Descripción: {data.descripcionProducto}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.7,
        )
        resultado = response.choices[0].message.content.strip()
        
        # Suponiendo que la respuesta de GPT está estructurada con secciones claras
        # Puedes parsear el resultado según el formato que devuelva GPT
        # Aquí simplemente devolvemos el texto completo
        return {
            "detalles_campana": resultado
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint 3: Definir el público objetivo + Seleccionar las ubicaciones de los anuncios
@router.post("/definir_publico_ubicaciones")
async def definir_publico_ubicaciones(data: PublicoObjetivoUbicacionesInput):
    prompt = f"""
Como estratega de marketing enfocado en segmentación y ubicaciones de anuncios en Meta Ads, define el **público objetivo ideal** para la campaña de "{data.nombreProducto}" utilizando criterios demográficos, geográficos y psicográficos.

Considera:

- **Ubicaciones geográficas**:
  - Distrito: {data.distrito}
  - Provincia: {data.provincia}
  - Departamento: {data.departamento}

- **Características del producto** y cómo se alinean con las **preferencias del público**.

Selecciona **criterios de segmentación relevantes**, incluyendo:

- Edad, género, intereses, comportamientos de compra, y otros datos demográficos clave.
- Intereses específicos relacionados con "{data.descripcionProducto}".

Luego, elige las **ubicaciones de anuncios más efectivas** de la lista predefinida de Meta ({data.ubicacionesMeta}), como Feed de Facebook, Historias de Instagram, Marketplace, etc.

Justifica tu selección basándote en:

- **Tendencias actuales del mercado**.
- **Hábitos de consumo de medios** del público objetivo.
- **Rendimiento histórico** de esas ubicaciones para productos similares.

Proporciona tu respuesta de manera estructurada, incluyendo las razones detrás de cada elección.

**Detalles del Producto:**
- Nombre: {data.nombreProducto}
- Descripción: {data.descripcionProducto}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7,
        )
        resultado = response.choices[0].message.content.strip()
        return {"publico_objetivo_y_ubicaciones": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint 4: Elegir el formato del anuncio + Definir la llamada a la acción (CTA)
@router.post("/elegir_formato_cta")
async def elegir_formato_cta(data: FormatoCTAInput):
    prompt = f"""
Como experto en creatividad publicitaria y plataformas de Meta Ads, tu tarea es:

1. **Seleccionar el formato de anuncio más efectivo** para promocionar "{data.nombreProducto}" de entre las opciones predefinidas por Meta:

   - Imagen única
   - Video
   - Carrusel
   - Colección

   Explica por qué este formato:

   - **Maximiza el engagement** con la audiencia objetivo.
   - Resalta las **características y beneficios clave** de "{data.nombreProducto}".
   - Se adapta a las **preferencias de consumo de contenido** de la audiencia.

2. **Definir la llamada a la acción (CTA) más impactante** de la lista proporcionada por Meta:

   - Comprar ahora
   - Más información
   - Registrarse
   - Enviar mensaje
   - Otros

   Justifica tu elección del CTA basándote en:

   - Los **objetivos de la campaña**.
   - El **comportamiento esperado** de los usuarios.
   - Cómo el CTA elegido **impulsa a la acción** al público objetivo.

Proporciona una respuesta clara, estructurada y enfocada en maximizar los resultados de marketing.

**Detalles del Producto:**
- Nombre: {data.nombreProducto}
- Descripción: {data.descripcionProducto}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        resultado = response.choices[0].message.content.strip()
        return {"formato_y_cta": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint 5: Crear el contenido creativo
@router.post("/crear_contenido_creativo")
async def crear_contenido_creativo(data: ContenidoCreativoInput):
    prompt = f"""
Como redactor creativo especializado en anuncios de Meta Ads, genera **contenido publicitario persuasivo y atractivo** para "{data.nombreProducto}".

El contenido debe:

- Resaltar las **características y beneficios clave** del producto.
- Adaptarse al **tono y estilo** especificado: {data.tonoEstilo}.
- Alinear el mensaje con los **intereses y necesidades** del público objetivo ({data.publicoObjetivo}).
- Utilizar un lenguaje que **resuene** con la audiencia y **genere una conexión emocional**.

Incluye:

- **Llamados a la acción** sutiles y efectivos.
- Al menos **tres variaciones** del contenido para pruebas A/B, incorporando:
  - Testimonios auténticos.
  - Datos impactantes o estadísticas relevantes.
  - Frases inspiradoras o eslóganes memorables.

Presenta tu respuesta de manera organizada y clara, asegurando que cada variación sea única pero mantenga la coherencia con la marca y el objetivo de la campaña.

**Detalles del Producto:**
- Nombre: {data.nombreProducto}
- Descripción: {data.descripcionProducto}
- Público Objetivo: {data.publicoObjetivo}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.7,
        )
        resultado = response.choices[0].message.content.strip()
        return {"contenido_creativo": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para generar el encabezado del anuncio
@router.post("/create_heading")
async def create_heading(encabezado: EncabezadoAnuncio):
    prompt = f"""
Eres un redactor publicitario experto en crear **encabezados cautivadores** para anuncios en plataformas de redes sociales.

Tu tarea es generar **encabezados concisos y atractivos** que cumplan con los siguientes requisitos:

1. **Producto**: El encabezado debe estar optimizado para "{encabezado.nombreProducto}", destacando sus **beneficios** y **propuestas de valor únicas**.

2. **Palabras Clave**: Incorpora las siguientes palabras clave para mejorar la optimización y relevancia del encabezado: {encabezado.palabrasClave}.

3. **Estilo de Escritura**: Adapta el estilo de escritura especificado, que es {encabezado.estiloEscritura}. Esto puede variar desde un tono profesional hasta uno casual y atractivo, según se indique.

4. **Longitud Máxima**: Limita el encabezado a un máximo de {encabezado.longitudMaxima} caracteres, asegurando **claridad** y **poder de atracción**.

5. **Variantes**: Proporciona {encabezado.variantes} versiones únicas del encabezado, cada una manteniendo el tono y relevancia para el producto, pero explorando diferentes enfoques creativos.

Asegúrate de que cada encabezado:

- **Capte la atención inmediata** del lector.
- Genere **interés** y motive al lector a **interactuar** con el anuncio.
- Sea coherente con la **imagen de marca** y los **objetivos de la campaña**.

**Detalles del Producto:**
- Nombre: {encabezado.nombreProducto}
- Descripción: {encabezado.descripcionProducto}

Palabras Clave: {encabezado.palabrasClave}
Estilo de Escritura: {encabezado.estiloEscritura}
Longitud Máxima de Caracteres: {encabezado.longitudMaxima}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
        )
        encabezados_generados = response.choices[0].message.content.strip()

        # Usar expresiones regulares para eliminar numeración o formato adicional
        variantes = re.findall(r"^\d+\.?\s*(.*)$", encabezados_generados, re.MULTILINE)

        # Si no se encontró ningún encabezado numerado, dividir por líneas como respaldo
        if not variantes:
            variantes = [line.strip() for line in encabezados_generados.split('\n') if line.strip() != '']

        # Limitar el número de variantes según lo especificado
        variantes = variantes[:encabezado.variantes]

        return {
            "encabezados": variantes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
