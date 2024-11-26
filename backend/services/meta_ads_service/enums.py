from enum import Enum

# === Enumerados para Estados de la Campaña y Conjunto de Anuncios ===

class CampaignStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DELETED = "DELETED"
    ARCHIVED = "ARCHIVED"

class StatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DELETED = "DELETED"
    ARCHIVED = "ARCHIVED"

# === Enumerados para Objetivos de la Campaña ===

class CampaignObjectiveEnum(str, Enum):
    OUTCOME_APP_PROMOTION = "OUTCOME_APP_PROMOTION"
    OUTCOME_AWARENESS = "OUTCOME_AWARENESS"
    OUTCOME_ENGAGEMENT = "OUTCOME_ENGAGEMENT"
    OUTCOME_LEADS = "OUTCOME_LEADS"
    OUTCOME_SALES = "OUTCOME_SALES"
    OUTCOME_TRAFFIC = "OUTCOME_TRAFFIC"
    # Agrega otros objetivos según sea necesario

# === Enumerados para Objetivos de Optimización ===

class OptimizationGoalEnum(str, Enum):
    NONE = "NONE"
    APP_INSTALLS = "APP_INSTALLS"
    AD_RECALL_LIFT = "AD_RECALL_LIFT"
    ENGAGED_USERS = "ENGAGED_USERS"
    EVENT_RESPONSES = "EVENT_RESPONSES"
    IMPRESSIONS = "IMPRESSIONS"
    LEAD_GENERATION = "LEAD_GENERATION"
    QUALITY_LEAD = "QUALITY_LEAD"
    LINK_CLICKS = "LINK_CLICKS"
    OFFSITE_CONVERSIONS = "OFFSITE_CONVERSIONS"
    PAGE_LIKES = "PAGE_LIKES"
    POST_ENGAGEMENT = "POST_ENGAGEMENT"
    QUALITY_CALL = "QUALITY_CALL"
    REACH = "REACH"
    LANDING_PAGE_VIEWS = "LANDING_PAGE_VIEWS"
    VISIT_INSTAGRAM_PROFILE = "VISIT_INSTAGRAM_PROFILE"
    VALUE = "VALUE"
    THRUPLAY = "THRUPLAY"
    DERIVED_EVENTS = "DERIVED_EVENTS"
    APP_INSTALLS_AND_OFFSITE_CONVERSIONS = "APP_INSTALLS_AND_OFFSITE_CONVERSIONS"
    CONVERSATIONS = "CONVERSATIONS"
    IN_APP_VALUE = "IN_APP_VALUE"
    MESSAGING_PURCHASE_CONVERSION = "MESSAGING_PURCHASE_CONVERSION"
    SUBSCRIBERS = "SUBSCRIBERS"
    REMINDERS_SET = "REMINDERS_SET"
    MEANINGFUL_CALL_ATTEMPT = "MEANINGFUL_CALL_ATTEMPT"
    PROFILE_VISIT = "PROFILE_VISIT"
    MESSAGING_APPOINTMENT_CONVERSION = "MESSAGING_APPOINTMENT_CONVERSION"

# === Enumerados para Estrategias de Puja ===

class BidStrategyEnum(str, Enum):
    LOWEST_COST_WITHOUT_CAP = "LOWEST_COST_WITHOUT_CAP"
    LOWEST_COST_WITH_BID_CAP = "LOWEST_COST_WITH_BID_CAP"
    COST_CAP = "COST_CAP"
    LOWEST_COST_WITH_MIN_ROAS = "LOWEST_COST_WITH_MIN_ROAS"

# === Enumerados para Eventos de Facturación ===

class BillingEventEnum(str, Enum):
    APP_INSTALLS = "APP_INSTALLS"
    CLICKS = "CLICKS"
    IMPRESSIONS = "IMPRESSIONS"
    LINK_CLICKS = "LINK_CLICKS"
    OFFER_CLAIMS = "OFFER_CLAIMS"
    PAGE_LIKES = "PAGE_LIKES"
    POST_ENGAGEMENT = "POST_ENGAGEMENT"
    VIDEO_VIEWS = "VIDEO_VIEWS"
    THRUPLAY = "THRUPLAY"
    PURCHASE = "PURCHASE"
    LISTING_INTERACTION = "LISTING_INTERACTION"

# === Enumerados para Categorías de Ajuste ===

class TuneForCategoryEnum(str, Enum):
    NONE = "NONE"
    EMPLOYMENT = "EMPLOYMENT"
    HOUSING = "HOUSING"
    CREDIT = "CREDIT"
    ISSUES_ELECTIONS_POLITICS = "ISSUES_ELECTIONS_POLITICS"
    ONLINE_GAMBLING_AND_GAMING = "ONLINE_GAMBLING_AND_GAMING"
    FINANCIAL_PRODUCTS_SERVICES = "FINANCIAL_PRODUCTS_SERVICES"

# === Enumerados para Peso de Múltiples Objetivos de Optimización ===

class MultiOptimizationGoalWeightEnum(str, Enum):
    UNDEFINED = "UNDEFINED"
    BALANCED = "BALANCED"
    PREFER_INSTALL = "PREFER_INSTALL"
    PREFER_EVENT = "PREFER_EVENT"

# === Enumerados para Categorías Especiales de Anuncios ===

class SpecialAdCategoryEnum(str, Enum):
    NONE = "NONE"
    EMPLOYMENT = "EMPLOYMENT"
    HOUSING = "HOUSING"
    CREDIT = "CREDIT"
    ISSUES_ELECTIONS_POLITICS = "ISSUES_ELECTIONS_POLITICS"

# === Enumerados para Tipos de Compra (Buy Type) ===

class BuyingTypeEnum(str, Enum):
    AUCTION = "AUCTION"
    RESERVED = "RESERVED"
    REACH_AND_FREQUENCY = "REACH_AND_FREQUENCY"

# === Enumerados para Tipos de Creativo de Anuncio ===

class AdCreativeTypeEnum(str, Enum):
    LINK = "LINK"
    PHOTO = "PHOTO"
    VIDEO = "VIDEO"
    CAROUSEL = "CAROUSEL"
    COLLECTION = "COLLECTION"
    SLIDESHOW = "SLIDESHOW"
    OFFER = "OFFER"

# === Enumerados para Formatos de Anuncio ===

class AdFormatEnum(str, Enum):
    SINGLE_IMAGE = "SINGLE_IMAGE"
    CAROUSEL = "CAROUSEL"
    VIDEO = "VIDEO"
    COLLECTION = "COLLECTION"

# === Enumerados para Posiciones de Publicación ===

class PublisherPlatformEnum(str, Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    AUDIENCE_NETWORK = "audience_network"
    MESSENGER = "messenger"

class FacebookPositionEnum(str, Enum):
    FEED = "feed"
    RIGHT_COLUMN = "right_column"
    INSTAGRAM_STORY = "instagram_story"
    INSTREAM_VIDEO = "instream_video"
    INSTAGRAM_FEED = "instagram_feed"
    MESSENGER_HOME = "messenger_home"
    INSTAGRAM_EXPLORER = "instagram_explorer"
    INSTAGRAM_REELS = "instagram_reels"
    INSTAGRAM_CANVAS = "instagram_canvas"
    STORIES = "stories"

# === Enumerados para Categorías de Contenido Especial ===

class ContentCategoryEnum(str, Enum):
    AUTOMOTIVE = "AUTOMOTIVE"
    REAL_ESTATE = "REAL_ESTATE"
    FINANCIAL_SERVICES = "FINANCIAL_SERVICES"
    HEALTH_AND_BEAUTY = "HEALTH_AND_BEAUTY"
    TECHNOLOGY = "TECHNOLOGY"

class AdStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DELETED = "DELETED"
    ARCHIVED = "ARCHIVED"