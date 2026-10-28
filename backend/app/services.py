from . import store
from .schemas import LecturaEntrada, ComandoLED

def guardar_lectura(datos: LecturaEntrada) -> dict:
    lectura = datos.model_dump()
    store.lecturas.append(lectura)
    # Conservamos como máximo las últimas 100 lecturas recibidas.
    del store.lecturas[:-100]
    return {"lectura": lectura, "led": store.estado_led["color"]}

def listar_lecturas() -> list[dict]:
    return store.lecturas

def consultar_led() -> dict:
    return store.estado_led

def cambiar_led(comando: ComandoLED) -> dict:
    store.estado_led["color"] = comando.color
    return store.estado_led

#RETO
from app.store import lecturas
from fastapi import HTTPException

def calcular_promedio(n: int):
    # Condición: No hay lecturas
    if not lecturas:
        raise HTTPException(status_code=404, detail="No hay lecturas disponibles para calcular el promedio.")
    
    # Seleccionar las últimas n lecturas (si hay menos, toma todas automáticamente)
    ultimas = lecturas[-n:]
    cantidad_real = len(ultimas)
    
    # Calcular sumatorias y promedios
    temp_prom = sum(l["temperatura"] for l in ultimas) / cantidad_real
    hum_prom = sum(l["humedad"] for l in ultimas) / cantidad_real
    
    # Retornar el diccionario con los valores redondeados
    return {
        "cantidad": cantidad_real,
        "temperatura_promedio": round(temp_prom, 2),
        "humedad_promedio": round(hum_prom, 2)
    }