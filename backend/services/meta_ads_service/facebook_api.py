from facebook_business.api import FacebookAdsApi
from facebook_business.exceptions import FacebookRequestError
import logging

def initialize_facebook_api(access_token: str):
    try:
        FacebookAdsApi.init(access_token=access_token)
        logging.info("FacebookAdsApi inicializada correctamente.")
    except FacebookRequestError as e:
        logging.error(f"Error al inicializar FacebookAdsApi: {e}")
        raise
    except Exception as e:
        logging.error(f"Error inesperado al inicializar FacebookAdsApi: {e}")
        raise
