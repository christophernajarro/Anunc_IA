from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from services.auth_service import security, schemas
from common.database.database import get_db
from datetime import timedelta
from common.models.usuario import Usuario, Cuenta
from common.schemas.usuario import UsuarioCreate, UsuarioResponse
from common.utils.session_manager import SessionManager  # Importar SessionManager

router = APIRouter()
session_manager = SessionManager()  # Inicializar el gestor de sesiones

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, summary="Registrar un nuevo usuario")
async def register_usuario(usuario: UsuarioCreate, response: Response, db: Session = Depends(get_db)):
    logs = [f"Datos de registro recibidos - Nombre: {usuario.nombre}, Email: {usuario.email}, Contraseña: {usuario.password}"]

    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

    try:
        # Crear el usuario con campos básicos
        hashed_password = security.get_password_hash(usuario.password)
        nuevo_usuario = Usuario(
            nombre=usuario.nombre,
            email=usuario.email,
            contraseña=hashed_password
        )
        logs.append("Usuario creado en memoria")

        # Crear una cuenta asociada con valores predeterminados
        nueva_cuenta = Cuenta(
            tipo_cuenta="Standard",
            saldo=0.0
        )
        nuevo_usuario.cuenta = nueva_cuenta
        logs.append("Cuenta asociada creada")

        # Guardar en la base de datos
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        logs.append("Usuario y cuenta guardados en la base de datos")

        # Generar token JWT
        access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            data={"sub": nuevo_usuario.email}, expires_delta=access_token_expires
        )
        logs.append("Token JWT generado")

        # Almacenar el JWT en Redis
        session_id = f"session_{nuevo_usuario.email}"
        await session_manager.store_jwt(session_id, access_token)
        logs.append("Token JWT almacenado en Redis")

        # Configurar la cookie con el session_id
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=False,
            samesite="Lax",
            secure=False  # Cambiar a True en producción con HTTPS
        )
        logs.append("Cookie de sesión configurada en la respuesta")

        # Imprimir todos los logs en un solo print
        print("\n".join(logs))

        return nuevo_usuario
    except Exception as e:
        db.rollback()
        print(f"Error en register_usuario: {e}")
        raise HTTPException(status_code=500, detail="Error al registrar el usuario.")

@router.post("/login", summary="Iniciar sesión de un usuario")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logs = [f"Intento de inicio de sesión - Email: {form_data.username}"]

    # Autenticar al usuario
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales inválidas.",
        )

    # Generar el token JWT
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    logs.append("Token JWT generado")

    # Almacenar el JWT en Redis
    session_id = f"session_{user.email}"
    await session_manager.store_jwt(session_id, access_token)
    logs.append("Token JWT almacenado en Redis")

    # Configurar la cookie con el session_id
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=False,
        samesite="Lax",
        secure=False  # Cambiar a True en producción con HTTPS
    )
    logs.append("Cookie de sesión configurada en la respuesta")

    # Imprimir todos los logs en un solo print
    print("\n".join(logs))

    return {"message": "Inicio de sesión exitoso"}

@router.post("/logout", summary="Cerrar sesión")
async def logout(response: Response, request: Request):
    logs = ["Intento de cierre de sesión"]

    # Obtener el session_id de la cookie
    session_id = request.cookies.get("session_id")
    if session_id:
        await session_manager.delete_jwt(session_id)  # Eliminar el JWT de Redis
        response.delete_cookie("session_id")          # Eliminar la cookie de sesión
        logs.append("Sesión cerrada y JWT eliminado de Redis")
    else:
        logs.append("No se encontró session_id en las cookies")

    # Imprimir todos los logs en un solo print
    print("\n".join(logs))

    return {"message": "Sesión cerrada"}

@router.get("/check_session", summary="Verificar sesión")
async def check_session(current_user: Usuario = Depends(security.get_current_user)):
    print(f"Verificación de sesión para el usuario: {current_user.email}")
    return {"message": "Sesión válida", "user": current_user.email}
