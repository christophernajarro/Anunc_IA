from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import ValidationError
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adimage import AdImage
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adset import AdSet
from facebook_business.exceptions import FacebookRequestError
from .facebook_api import initialize_facebook_api
import tempfile
import uuid

from .schemas import (
    CampaignCreateRequest,
    CampaignCreateResponse,
    AdSetCreateRequest,
    AdSetCreateResponse,
    UploadImageResponse,
    ListImagesResponse,
    DeleteImageRequest,
    CreateAdRequest,
    CreateAdResponse,
    AdCreativeCreateRequest,
    AdCreativeCreateResponse,
    AdCreateRequest,
    AdCreateResponse,
)
from .enums import BidStrategyEnum, SpecialAdCategoryEnum
import logging
import os
import traceback
from dotenv import load_dotenv
import requests
import httpx

# Cargar variables de entorno
load_dotenv()

# Configuración de Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Variables de entorno
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")  # Asegúrate de que incluye "act_"

if not all([ACCESS_TOKEN, APP_ID, APP_SECRET, AD_ACCOUNT_ID]):
    logging.error("Faltan variables de entorno. Verifica tu archivo .env.")
    raise EnvironmentError("Faltan variables de entorno. Verifica tu archivo .env.")

# Inicializar la API de Facebook Ads
initialize_facebook_api(ACCESS_TOKEN)

# Crear el router para meta_ads_service
router = APIRouter(
    prefix="/meta_ads",
    tags=["Meta Ads"]
)

@router.post("/create_campaign", response_model=CampaignCreateResponse, summary="Crear una Campaña")
def create_campaign(campaign_data: CampaignCreateRequest):
    logging.info("Inicio del proceso de creación de una campaña.")
    try:
        ad_account = AdAccount(AD_ACCOUNT_ID)
        logging.debug("Objeto AdAccount creado correctamente.")

        # Parámetros de la campaña
        params_campaign = {
            "name": campaign_data.name,
            "objective": campaign_data.objective.value,  # Usar el valor de la enum
            "status": campaign_data.status.value,  # Usar el valor de la enum
            "special_ad_categories": [category.value for category in campaign_data.special_ad_categories],
        }

        # Crear la campaña
        campaign = ad_account.create_campaign(params=params_campaign)
        campaign_id = campaign.get_id()
        logging.info(f"Campaña creada con éxito. ID: {campaign_id}")

        return CampaignCreateResponse(
            message="Campaña creada exitosamente.",
            campaign_id=campaign_id
        )
    except FacebookRequestError as e:
        logging.error(f"FacebookRequestError: {e.api_error_message()}")
        raise HTTPException(status_code=400, detail=e.api_error_message())
    except ValidationError as e:
        logging.error(f"ValidationError: {e}")
        raise HTTPException(status_code=422, detail="Error de validación en los datos proporcionados.")
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")

@router.post("/create_ad_set", response_model=AdSetCreateResponse, summary="Crear un Conjunto de Anuncios")
def create_ad_set(ad_set_data: AdSetCreateRequest):
    logging.info("Inicio del proceso de creación de un conjunto de anuncios.")
    try:
        ad_account = AdAccount(AD_ACCOUNT_ID)
        logging.debug("Objeto AdAccount creado correctamente.")

        # Validar que la campaña exista y obtener su objetivo
        campaign = Campaign(ad_set_data.campaign_id).api_get(fields=[Campaign.Field.objective])
        campaign_objective = campaign.get('objective')
        logging.debug(f"Objetivo de la campaña obtenida: {campaign_objective}")

        # Preparar parámetros para el Ad Set
        params_adset = {
            'name': ad_set_data.name,
            'campaign_id': ad_set_data.campaign_id,
            'billing_event': ad_set_data.billing_event.value,
            'optimization_goal': ad_set_data.optimization_goal.value,
            'targeting': ad_set_data.targeting.dict(exclude_none=True),
            'status': ad_set_data.status.value,
        }

        # Añadir 'promoted_object' si es necesario
        if ad_set_data.promoted_object:
            params_adset['promoted_object'] = ad_set_data.promoted_object.dict(exclude_none=True)

        # Añadir presupuesto diario o de por vida
        if ad_set_data.daily_budget:
            params_adset['daily_budget'] = ad_set_data.daily_budget
        if ad_set_data.lifetime_budget:
            params_adset['lifetime_budget'] = ad_set_data.lifetime_budget

        # Añadir 'bid_strategy' y 'bid_amount' si están presentes y son compatibles
        if ad_set_data.bid_strategy:
            params_adset['bid_strategy'] = ad_set_data.bid_strategy.value
            if ad_set_data.bid_strategy != BidStrategyEnum.LOWEST_COST_WITHOUT_CAP and ad_set_data.bid_amount:
                params_adset['bid_amount'] = ad_set_data.bid_amount
            elif ad_set_data.bid_strategy == BidStrategyEnum.LOWEST_COST_WITHOUT_CAP and ad_set_data.bid_amount:
                logging.warning('`bid_amount` será ignorado debido a la estrategia de puja LOWEST_COST_WITHOUT_CAP.')
                # Opcional: Puedes eliminar `bid_amount` aquí si es necesario
                # params_adset.pop('bid_amount', None)

        # Añadir tiempos de inicio y fin si están presentes
        if ad_set_data.start_time:
            params_adset['start_time'] = ad_set_data.start_time.isoformat()
        if ad_set_data.end_time:
            params_adset['end_time'] = ad_set_data.end_time.isoformat()

        # Añadir 'tune_for_category' si está presente
        if ad_set_data.tune_for_category:
            params_adset['tune_for_category'] = ad_set_data.tune_for_category.value

        # Añadir 'multi_optimization_goal_weight' si está presente
        if ad_set_data.multi_optimization_goal_weight:
            params_adset['multi_optimization_goal_weight'] = ad_set_data.multi_optimization_goal_weight.value

        # Añadir 'dsa_payor' y 'dsa_beneficiary' si están presentes
        if ad_set_data.dsa_payor:
            params_adset['dsa_payor'] = ad_set_data.dsa_payor
        if ad_set_data.dsa_beneficiary:
            params_adset['dsa_beneficiary'] = ad_set_data.dsa_beneficiary

        # Crear el Ad Set
        ad_set = ad_account.create_ad_set(params=params_adset)
        ad_set_id = ad_set.get_id()
        logging.info(f"Conjunto de anuncios creado con éxito. ID: {ad_set_id}")

        return AdSetCreateResponse(
            message="Conjunto de anuncios creado exitosamente.",
            ad_set_id=ad_set_id
        )
    except FacebookRequestError as e:
        logging.error(f"FacebookRequestError: {e.api_error_message()} (Code: {e.api_error_code()}, Subcode: {e.api_error_subcode()})")
        logging.error(f"Error JSON: {e.body}")
        raise HTTPException(status_code=400, detail=e.api_error_message())
    except ValidationError as e:
        logging.error(f"ValidationError: {e}")
        raise HTTPException(status_code=422, detail="Error de validación en los datos proporcionados.")
    except HTTPException as e:
        raise e  # Re-lanzar excepciones HTTP para que sean manejadas correctamente
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")

@router.post("/upload_image", response_model=UploadImageResponse, summary="Subir una Imagen")
async def upload_image(file: UploadFile = File(...)):
    logging.info("Recibiendo solicitud para subir una imagen.")
    try:
        filename = file.filename

        # Validar formato
        if file.content_type not in ["image/jpeg", "image/png", "image/gif", "image/bmp"]:
            raise HTTPException(
                status_code=400,
                detail=f"Formato de imagen no soportado: {file.content_type}. Formatos permitidos: JPEG, PNG, GIF, BMP."
            )

        # Leer contenido
        image_content = await file.read()
        if len(image_content) == 0:
            raise HTTPException(status_code=400, detail="El archivo está vacío.")

        # Validar que sea una imagen válida
        try:
            from PIL import Image
            from io import BytesIO

            image = Image.open(BytesIO(image_content))
            image.verify()  # Verifica que es una imagen válida
        except Exception as e:
            logging.error(f"El archivo no es una imagen válida: {e}")
            raise HTTPException(status_code=400, detail="El archivo no es una imagen válida.")

        # Normalizar el nombre del archivo
        import re
        sanitized_filename = re.sub(r'[^\w\-.]', '_', filename)

        # Preparar datos
        url = f"https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}/adimages"
        files = {'file': (sanitized_filename, image_content, file.content_type)}
        form_data = {'filename': sanitized_filename, 'access_token': ACCESS_TOKEN}

        # Enviar solicitud
        async with httpx.AsyncClient() as client:
            logging.info(f"Enviando datos: {form_data}, archivo: {sanitized_filename}")
            response = await client.post(url, data=form_data, files=files)

        # Validar respuesta
        if response.status_code != 200:
            logging.error(f"Error al subir la imagen: {response.text}")
            error_response = response.json().get('error', {})
            raise HTTPException(status_code=400, detail=error_response.get('error_user_msg', "Error desconocido."))

        response_json = response.json()
        image_hash = response_json.get('images', {}).get(sanitized_filename, {}).get('hash')
        if not image_hash:
            raise HTTPException(status_code=500, detail="No se pudo obtener el hash de la imagen.")

        return UploadImageResponse(message="Imagen subida exitosamente.", image_hash=image_hash)

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")

@router.post("/create_ad_creative", response_model=AdCreativeCreateResponse, summary="Crear un Ad Creative")
def create_ad_creative(ad_creative_data: AdCreativeCreateRequest):
    logging.info("Inicio del proceso de creación de un Ad Creative.")
    try:
        ad_account = AdAccount(AD_ACCOUNT_ID)
        logging.debug("Objeto AdAccount creado correctamente.")

        # Convertir object_story_spec a un diccionario
        object_story_spec_dict = ad_creative_data.object_story_spec.dict()

        # Convert degrees_of_freedom_spec to dict
        degrees_of_freedom_spec_dict = ad_creative_data.degrees_of_freedom_spec.dict()

        # Preparar los parámetros de la solicitud
        params = {
            "name": ad_creative_data.name,
            "object_story_spec": object_story_spec_dict,
            "degrees_of_freedom_spec": degrees_of_freedom_spec_dict
        }

        if ad_creative_data.authorization_category and ad_creative_data.authorization_category != SpecialAdCategoryEnum.NONE:
            params["authorization_category"] = ad_creative_data.authorization_category.value

        # Verificar que object_story_spec_dict es un diccionario
        if not isinstance(object_story_spec_dict, dict):
            logging.error("object_story_spec no es un diccionario.")
            raise HTTPException(status_code=400, detail="object_story_spec debe ser un diccionario.")

        # Crear el Ad Creative
        ad_creative = ad_account.create_ad_creative(params=params)
        ad_creative_id = ad_creative.get_id()
        logging.info(f"Ad Creative creado con éxito. ID: {ad_creative_id}")

        return AdCreativeCreateResponse(
            message="Ad Creative creado exitosamente.",
            ad_creative_id=ad_creative_id
        )
    except FacebookRequestError as e:
        logging.error(f"FacebookRequestError: {e.api_error_message()} (Code: {e.api_error_code()}, Subcode: {e.api_error_subcode()})")
        logging.error(f"Error JSON: {e.body}")
        raise HTTPException(status_code=400, detail=e.api_error_message())
    except ValidationError as e:
        logging.error(f"ValidationError: {e}")
        raise HTTPException(status_code=422, detail="Error de validación en los datos proporcionados.")
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        logging.error(f"Traceback: {traceback_str}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")

@router.post("/create_ad", response_model=AdCreateResponse, summary="Crear un Anuncio")
def create_ad(ad_data: AdCreateRequest):
    logging.info("Inicio del proceso de creación de un anuncio.")
    try:
        ad_account = AdAccount(AD_ACCOUNT_ID)
        logging.debug("Objeto AdAccount creado correctamente.")
        
        # Preparar los parámetros para la creación del anuncio
        params_ad = {
            "name": ad_data.name,
            "adset_id": ad_data.adset_id,
            "creative": ad_data.creative,
            "status": ad_data.status.value,
        }
        
        # Agregar parámetros opcionales si están presentes
        if ad_data.ad_schedule_end_time:
            params_ad["ad_schedule_end_time"] = ad_data.ad_schedule_end_time
        if ad_data.ad_schedule_start_time:
            params_ad["ad_schedule_start_time"] = ad_data.ad_schedule_start_time
        if ad_data.adlabels:
            params_ad["adlabels"] = ad_data.adlabels
        if ad_data.audience_id:
            params_ad["audience_id"] = ad_data.audience_id
        if ad_data.conversion_domain:
            params_ad["conversion_domain"] = ad_data.conversion_domain
        if ad_data.creative_asset_groups_spec:
            params_ad["creative_asset_groups_spec"] = ad_data.creative_asset_groups_spec
        if ad_data.date_format:
            params_ad["date_format"] = ad_data.date_format
        if ad_data.display_sequence:
            params_ad["display_sequence"] = ad_data.display_sequence
        if ad_data.draft_adgroup_id:
            params_ad["draft_adgroup_id"] = ad_data.draft_adgroup_id
        if ad_data.engagement_audience is not None:
            params_ad["engagement_audience"] = ad_data.engagement_audience
        if ad_data.execution_options:
            params_ad["execution_options"] = ad_data.execution_options
        if ad_data.include_demolink_hashes is not None:
            params_ad["include_demolink_hashes"] = ad_data.include_demolink_hashes
        if ad_data.priority is not None:
            params_ad["priority"] = ad_data.priority
        if ad_data.source_ad_id:
            params_ad["source_ad_id"] = ad_data.source_ad_id
        if ad_data.tracking_specs:
            params_ad["tracking_specs"] = ad_data.tracking_specs

        logging.debug(f"Parámetros para crear el anuncio: {params_ad}")
        
        # Crear el anuncio
        ad = ad_account.create_ad(params=params_ad)
        ad_id = ad.get_id()
        logging.info(f"Anuncio creado con éxito. ID: {ad_id}")
        
        return AdCreateResponse(
            message="Anuncio creado exitosamente.",
            ad_id=ad_id
        )
        
    except FacebookRequestError as e:
        logging.error(f"FacebookRequestError: {e.api_error_message()} (Code: {e.api_error_code()}, Subcode: {e.api_error_subcode()})")
        logging.error(f"Error JSON: {e.body}")
        raise HTTPException(status_code=400, detail=e.api_error_message())
    except ValidationError as e:
        logging.error(f"ValidationError: {e}")
        raise HTTPException(status_code=422, detail="Error de validación en los datos proporcionados.")
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")