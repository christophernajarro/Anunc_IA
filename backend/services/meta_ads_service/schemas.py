from pydantic import BaseModel, Field, validator, model_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
from .enums import (
    BidStrategyEnum,
    BillingEventEnum,
    OptimizationGoalEnum,
    StatusEnum,
    TuneForCategoryEnum,
    MultiOptimizationGoalWeightEnum,
    SpecialAdCategoryEnum,
    CampaignObjectiveEnum,
    AdStatusEnum
)

# Modelos Existentes
class CampaignCreateResponse(BaseModel):
    message: str = Field(..., description="Mensaje indicando el resultado de la creación de la campaña.")
    campaign_id: str = Field(..., description="ID de la campaña creada exitosamente.")

class CampaignCreateRequest(BaseModel):
    name: str = Field(..., description="Nombre de la campaña.")
    objective: CampaignObjectiveEnum = Field(..., description="Objetivo de la campaña.")
    status: StatusEnum = Field(..., description="Estado de la campaña.")
    special_ad_categories: List[SpecialAdCategoryEnum] = Field(
        default=[SpecialAdCategoryEnum.NONE],
        description="Categorías especiales de anuncios (e.g., EMPLOYMENT, HOUSING, etc.)."
    )

class PromotedObject(BaseModel):
    page_id: Optional[str] = Field(
        None,
        description="ID de la página de Facebook que se está promocionando. Requerido para objetivos como PAGE_LIKES."
    )
    application_id: Optional[str] = Field(
        None,
        description="ID de la aplicación para objetivos como APP_INSTALLS. Requerido junto con `object_store_url`."
    )
    object_store_url: Optional[str] = Field(
        None,
        description="URL de la tienda de aplicaciones. Requerido junto con `application_id` para objetivos como APP_INSTALLS."
    )
    custom_event_type: Optional[str] = Field(
        None,
        description="Tipo de evento personalizado para optimización. Requerido para ciertos objetivos."
    )
    product_set_id: Optional[str] = Field(
        None,
        description="ID del conjunto de productos para objetivos como PRODUCT_CATALOG_SALES."
    )
    # Agrega otros campos según sea necesario.

class Targeting(BaseModel):
    geo_locations: Dict[str, Any] = Field(..., description="Ubicación geográfica de la audiencia.")
    age_min: Optional[int] = Field(None, description="Edad mínima de la audiencia.")
    age_max: Optional[int] = Field(None, description="Edad máxima de la audiencia.")
    genders: Optional[List[int]] = Field(None, description="Género de la audiencia.")
    facebook_positions: Optional[List[str]] = Field(None, description="Posiciones en Facebook.")
    publisher_platforms: Optional[List[str]] = Field(None, description="Plataformas de publicación.")
    flexible_spec: Optional[List[Dict[str, Any]]] = Field(None, description="Especificaciones flexibles para el targeting.")

# Modelos para Ad Set
class AdSetCreateRequest(BaseModel):
    name: str = Field(
        ...,
        description="Nombre del conjunto de anuncios. Máximo 400 caracteres."
    )
    optimization_goal: OptimizationGoalEnum = Field(
        ...,
        description="""
        Objetivo de optimización para este conjunto de anuncios.
        Opciones disponibles incluyen:
        - NONE
        - APP_INSTALLS
        - AD_RECALL_LIFT
        - ENGAGED_USERS
        - EVENT_RESPONSES
        - IMPRESSIONS
        - LEAD_GENERATION
        - QUALITY_LEAD
        - LINK_CLICKS
        - OFFSITE_CONVERSIONS
        - PAGE_LIKES
        - POST_ENGAGEMENT
        - QUALITY_CALL
        - REACH
        - LANDING_PAGE_VIEWS
        - VISIT_INSTAGRAM_PROFILE
        - VALUE
        - THRUPLAY
        - DERIVED_EVENTS
        - APP_INSTALLS_AND_OFFSITE_CONVERSIONS
        - CONVERSATIONS
        - IN_APP_VALUE
        - MESSAGING_PURCHASE_CONVERSION
        - SUBSCRIBERS
        - REMINDERS_SET
        - MEANINGFUL_CALL_ATTEMPT
        - PROFILE_VISIT
        - MESSAGING_APPOINTMENT_CONVERSION
        """
    )
    billing_event: BillingEventEnum = Field(
        ...,
        description="""
        Evento de facturación para este conjunto de anuncios.
        Opciones disponibles incluyen:
        - IMPRESSIONS
        - LINK_CLICKS
        - POST_ENGAGEMENT
        - PAGE_LIKES
        - etc.
        """
    )
    bid_amount: Optional[int] = Field(
        None,
        description="""
        Monto de la puja en la unidad mínima de la moneda de la cuenta.
        Requerido si `bid_strategy` es LOWEST_COST_WITH_BID_CAP o COST_CAP.
        """
    )
    bid_strategy: Optional[BidStrategyEnum] = Field(
        None,
        description="""
        Estrategia de puja para este conjunto de anuncios.
        Opciones disponibles:
        - LOWEST_COST_WITHOUT_CAP
        - LOWEST_COST_WITH_BID_CAP
        - COST_CAP
        - LOWEST_COST_WITH_MIN_ROAS
        """
    )
    daily_budget: Optional[int] = Field(
        None,
        description="""
        Presupuesto diario del conjunto de anuncios en la unidad mínima de la moneda de la cuenta.
        Debe ser mayor que 0 si se especifica.
        """
    )
    lifetime_budget: Optional[int] = Field(
        None,
        description="""
        Presupuesto de por vida del conjunto de anuncios en la unidad mínima de la moneda de la cuenta.
        Requiere `end_time` si se especifica.
        """
    )
    campaign_id: str = Field(
        ...,
        description="ID de la campaña a la que pertenece este conjunto de anuncios."
    )
    promoted_object: PromotedObject = Field(
        ...,
        description="""
        El objeto que este conjunto de anuncios está promoviendo.
        Dependiendo del `optimization_goal`, se requieren diferentes campos.
        """
    )
    targeting: Targeting = Field(
        ...,
        description="Estructura de targeting para el conjunto de anuncios."
    )
    status: StatusEnum = Field(
        ...,
        description="""
        Estado del conjunto de anuncios.
        Opciones disponibles:
        - ACTIVE
        - PAUSED
        - DELETED
        - ARCHIVED
        """
    )
    start_time: Optional[datetime] = Field(
        None,
        description="""
        Hora de inicio del conjunto de anuncios en formato ISO 8601.
        Ejemplo: "2024-11-22T00:00:00+00:00"
        """
    )
    end_time: Optional[datetime] = Field(
        None,
        description="""
        Hora de finalización del conjunto de anuncios en formato ISO 8601.
        Requerido si se especifica `lifetime_budget`.
        Ejemplo: "2024-12-01T00:00:00+00:00"
        """
    )
    tune_for_category: Optional[TuneForCategoryEnum] = Field(
        None,
        description="""
        Categoría para ajustar la optimización.
        Opciones disponibles:
        - NONE
        - EMPLOYMENT
        - HOUSING
        - CREDIT
        - ISSUES_ELECTIONS_POLITICS
        - ONLINE_GAMBLING_AND_GAMING
        - FINANCIAL_PRODUCTS_SERVICES
        """
    )
    multi_optimization_goal_weight: Optional[MultiOptimizationGoalWeightEnum] = Field(
        None,
        description="""
        Peso para múltiples objetivos de optimización.
        Opciones disponibles:
        - UNDEFINED
        - BALANCED
        - PREFER_INSTALL
        - PREFER_EVENT
        """
    )
    dsa_payor: Optional[str] = Field(
        None,
        description="""
        El pagador de todos los anuncios en este conjunto de anuncios.
        Requerido para regiones reguladas por DSA (e.g., EU).
        """
    )
    dsa_beneficiary: Optional[str] = Field(
        None,
        description="""
        El beneficiario de todos los anuncios en este conjunto de anuncios.
        Requerido para regiones reguladas por DSA (e.g., EU).
        """
    )
    # Agrega otros campos según sea necesario.

    @validator('daily_budget', always=True)
    def check_daily_budget(cls, v, values):
        if v is not None and v <= 0:
            raise ValueError('El presupuesto diario debe ser mayor que 0.')
        return v

    @validator('lifetime_budget', always=True)
    def check_lifetime_budget(cls, v, values):
        if v is not None and v <= 0:
            raise ValueError('El presupuesto de por vida debe ser mayor que 0.')
        return v

    @validator('promoted_object')
    def validate_promoted_object(cls, v, values):
        optimization_goal = values.get('optimization_goal')
        if optimization_goal in [
            OptimizationGoalEnum.PAGE_LIKES,
            OptimizationGoalEnum.POST_ENGAGEMENT,
            OptimizationGoalEnum.EVENT_RESPONSES
        ]:
            if not v.page_id:
                raise ValueError(f'`page_id` es requerido para el objetivo de optimización {optimization_goal}.')
        elif optimization_goal in [
            OptimizationGoalEnum.APP_INSTALLS,
            OptimizationGoalEnum.APP_INSTALLS_AND_OFFSITE_CONVERSIONS
        ]:
            if not (v.application_id and v.object_store_url):
                raise ValueError('`application_id` y `object_store_url` son requeridos para objetivos de optimización de aplicaciones.')
        # Agrega otras validaciones según los objetivos necesarios.
        return v

    @validator('bid_amount', always=True)
    def validate_bid_amount(cls, v, values):
        bid_strategy = values.get('bid_strategy')
        if bid_strategy == BidStrategyEnum.LOWEST_COST_WITHOUT_CAP and v is not None:
            raise ValueError('No puedes establecer `bid_amount` con la estrategia de puja LOWEST_COST_WITHOUT_CAP.')
        if bid_strategy in [BidStrategyEnum.LOWEST_COST_WITH_BID_CAP, BidStrategyEnum.COST_CAP]:
            if v is None or v <= 0:
                raise ValueError(f'`bid_amount` debe ser mayor que 0 si `bid_strategy` es {bid_strategy}.')
        return v

    @validator('end_time')
    def validate_end_time(cls, v, values):
        lifetime_budget = values.get('lifetime_budget')
        if lifetime_budget and not v:
            raise ValueError('`end_time` es requerido si se especifica `lifetime_budget`.')
        return v

class AdSetCreateResponse(BaseModel):
    message: str = Field(
        ...,
        description="Mensaje indicando el resultado de la creación del Ad Set."
    )
    ad_set_id: str = Field(
        ...,
        description="ID del Ad Set creado exitosamente."
    )

# Modelos para Gestión de Imágenes y Anuncios

class UploadImageResponse(BaseModel):
    message: str = Field(..., description="Mensaje indicando el resultado de la carga de la imagen.")
    image_hash: str = Field(..., description="Hash único de la imagen cargada.")

class ListImagesResponse(BaseModel):
    images: List[Dict[str, Any]] = Field(..., description="Lista de imágenes disponibles en la cuenta de anuncios.")

class DeleteImageRequest(BaseModel):
    image_hash: str = Field(..., description="Hash de la imagen que se desea eliminar.")

class CreateAdRequest(BaseModel):
    name: str = Field(..., description="Nombre del anuncio.")
    ad_set_id: str = Field(..., description="ID del conjunto de anuncios al que pertenece el anuncio.")
    image_hash: str = Field(..., description="Hash de la imagen a utilizar en el anuncio.")
    title: str = Field(..., description="Título del anuncio.")
    body: str = Field(..., description="Cuerpo del anuncio.")
    object_url: str = Field(..., description="URL a la que dirigirá el anuncio.")
    status: Optional[StatusEnum] = Field("PAUSED", description="Estado del anuncio. Por defecto está pausado.")

class CreateAdResponse(BaseModel):
    message: str = Field(..., description="Mensaje indicando el resultado de la creación del anuncio.")
    ad_id: str = Field(..., description="ID del anuncio creado exitosamente.")

class ObjectStorySpec(BaseModel):
    page_id: str = Field(..., description="ID de la página de Facebook que se está promocionando.")
    link_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Datos del enlace, incluyendo `image_hash`, `link`, y `message`."
    )
    # Puedes añadir otros campos como `photo_data`, `video_data`, etc., según tus necesidades.

class StandardEnhancements(BaseModel):
    enroll_status: str = Field(..., description="Debe ser 'OPT_IN' o 'OPT_OUT'.")

    @validator('enroll_status')
    def validate_enroll_status(cls, v):
        if v not in ["OPT_IN", "OPT_OUT"]:
            raise ValueError("`enroll_status` debe ser 'OPT_IN' o 'OPT_OUT'.")
        return v

class CreativeFeaturesSpec(BaseModel):
    standard_enhancements: StandardEnhancements = Field(..., description="Especificaciones de las mejoras estándar.")

class DegreesOfFreedomSpec(BaseModel):
    creative_features_spec: CreativeFeaturesSpec = Field(..., description="Especificaciones de las características creativas.")

class AdCreativeCreateRequest(BaseModel):
    name: str = Field(..., description="Nombre del Ad Creative.")
    object_story_spec: ObjectStorySpec = Field(..., description="Especificaciones del objeto de la historia.")
    degrees_of_freedom_spec: DegreesOfFreedomSpec = Field(..., description="Especificaciones de las mejoras estándar.")
    authorization_category: Optional[SpecialAdCategoryEnum] = Field(
        None,
        description="Categoría de autorización para anuncios relacionados con temas sociales, elecciones o política."
    )

class LinkData(BaseModel):
    image_hash: str = Field(..., description="Hash de la imagen.")
    link: str = Field(..., description="Enlace al que dirige el anuncio.")
    message: str = Field(..., description="Mensaje del anuncio.")

class ObjectStorySpec(BaseModel):
    page_id: str = Field(..., description="ID de la página de Facebook que se está promocionando.")
    link_data: LinkData = Field(..., description="Datos del enlace.")

class CreativeSpec(BaseModel):
    name: str = Field(..., description="Nombre del Ad Creative.")
    object_story_spec: ObjectStorySpec = Field(..., description="Especificaciones del objeto de la historia.")

class CreativeDict(BaseModel):
    creative_id: Optional[str] = Field(None, description="ID del Ad Creative existente.")
    creative_spec: Optional[CreativeSpec] = Field(
        None,
        description="Especificaciones del Ad Creative para crear uno nuevo en la misma solicitud."
    )

    @model_validator(mode='after')
    def check_creative(cls, instance):
        if not instance.creative_id and not instance.creative_spec:
            raise ValueError("Se debe proporcionar 'creative_id' o 'creative_spec'.")
        return instance
class AdCreateRequest(BaseModel):
    name: str = Field(..., example="Mi Anuncio")
    adset_id: str = Field(..., example="1234567890")
    creative: Dict[str, str] = Field(..., example={"creative_id": "0987654321"})
    status: AdStatusEnum = Field(..., example="PAUSED")
    ad_schedule_end_time: Optional[str] = Field(None, example="2024-12-31T23:59:59")
    ad_schedule_start_time: Optional[str] = Field(None, example="2024-01-01T00:00:00")
    adlabels: Optional[List[Dict]] = Field(None, example=[{"id": "label_id", "name": "Label Name"}])
    audience_id: Optional[str] = Field(None, example="audience_id")
    conversion_domain: Optional[str] = Field(None, example="facebook.com")
    creative_asset_groups_spec: Optional[str] = Field(None, example="Spec details")
    date_format: Optional[str] = Field(None, example="YYYY-MM-DD")
    display_sequence: Optional[int] = Field(None, example=1)
    draft_adgroup_id: Optional[str] = Field(None, example="draft_id")
    engagement_audience: Optional[bool] = Field(None, example=True)
    execution_options: Optional[List[str]] = Field(None, example=["validate_only"])
    include_demolink_hashes: Optional[bool] = Field(None, example=False)
    priority: Optional[int] = Field(None, example=10)
    source_ad_id: Optional[str] = Field(None, example="source_ad_id")
    tracking_specs: Optional[Dict] = Field(None, example={"action": "click"})
    
class AdCreateResponse(BaseModel):
    message: str
    ad_id: str

class AdCreativeCreateRequest(BaseModel):
    name: str = Field(..., description="Nombre del Ad Creative.")
    object_story_spec: ObjectStorySpec = Field(..., description="Especificaciones del objeto de la historia.")
    degrees_of_freedom_spec: DegreesOfFreedomSpec = Field(..., description="Especificaciones de las mejoras estándar.")
    authorization_category: Optional[SpecialAdCategoryEnum] = Field(
        None,
        description="Categoría de autorización para anuncios relacionados con temas sociales, elecciones o política."
    )

class AdCreativeCreateResponse(BaseModel):
    message: str = Field(..., description="Mensaje indicando el resultado de la creación del Ad Creative.")
    ad_creative_id: str = Field(..., description="ID del Ad Creative creado exitosamente.")