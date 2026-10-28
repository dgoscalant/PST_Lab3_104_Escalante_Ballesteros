from fastapi import APIRouter
from .schemas import LecturaEntrada, ComandoLED
from . import services

router = APIRouter()

@router.get("/salud")
def salud():
    return {"estado": "ok", "laboratorio": "3"}

@router.get("/lecturas")
def get_lecturas():
    return services.listar_lecturas()

@router.post("/lecturas", status_code=201)
def post_lectura(datos: LecturaEntrada):
    return services.guardar_lectura(datos)

@router.get("/led")
def get_led():
    return services.consultar_led()

@router.put("/led")
def put_led(comando: ComandoLED):
    return services.cambiar_led(comando)

#RETO

from fastapi import Query

@router.get("/lecturas/promedio")
def obtener_promedio_lecturas(
    n: int = Query(3, ge=1, le=100) # Valor por defecto 3, mínimo 1, máximo 100
):
    return services.calcular_promedio(n)