from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Agregar el directorio backend al sys.path para permitir la importación de modelos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importa solo Base, ya que engine no se utiliza en env.py
from common.database.database import Base  # Eliminado 'engine' ya que no se usa

# Importar todos los modelos aquí, asegurando que 'Cuenta' se importe antes que 'Usuario'
from common.database.database import Base
from common.models.usuario import Usuario, Cuenta
from services.ai_content_service.models import Documento
from services.product_service.models import Producto

# Alembic Config object, which provides access to the .ini file values
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Establece el target_metadata con la información de tus modelos
target_metadata = Base.metadata

# Configuración para ejecutar migraciones offline
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# Configuración para ejecutar migraciones online
def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()