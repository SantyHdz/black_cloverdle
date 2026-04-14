"""
main.py — FastAPI endpoints para Black Cloverdle, Módulo 1: Adivina el Personaje.

Ejecutar con:
    uvicorn main:app --reload
Documentación interactiva en:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from data_loader import load_characters, get_character_by_name, get_unique_values
from routes.guess import router as guess_router
from logic import (
    get_daily_character,
    get_autocomplete_suggestions,
    process_guess,
    ARC_ORDER,
)

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Black Cloverdle API",
    description="Backend para el juego Black Cloverdle — Módulo 1: Adivina el Personaje",
    version="1.0.0",
)

app.include_router(guess_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # En producción reemplazar con el origen del frontend
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Schemas Pydantic
# ---------------------------------------------------------------------------

class GuessRequest(BaseModel):
    nombre: str

    model_config = {
        "json_schema_extra": {
            "example": {"nombre": "Asta"}
        }
    }


class GuessResponse(BaseModel):
    found: bool
    is_correct: bool
    message: str
    comparison: Optional[Dict[str, Any]] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "found": True,
                "is_correct": False,
                "message": "Incorrecto. Sigue intentando.",
                "comparison": {
                    "nombre":     {"value": "Asta",        "result": "incorrect"},
                    "genero":     {"value": "Masculino",   "result": "correct"},
                    "atributos":  {"value": ["Mago"],      "result": "partial"},
                    "raza":       {"value": ["Humano"],    "result": "correct"},
                    "altura":     {"value": "155cm",       "result": "higher"},
                    "reino":      {"value": "Reino del Trébol", "result": "correct"},
                    "orden":      {"value": "Toros Negros","result": "correct"},
                    "tipo_magia": {"value": ["Anti-Magia"],"result": "incorrect"},
                    "arco":       {"value": "Arco de presentación", "result": "lower"},
                    "is_correct": False,
                },
            }
        }
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
async def root():
    """Verificación de que la API está corriendo."""
    return {"status": "ok", "game": "Black Cloverdle"}


# ── Personaje diario ────────────────────────────────────────────────────────

@app.get(
    "/daily",
    tags=["Módulo 1"],
    summary="Personaje del día (sin spoilers)"
)
async def get_daily():
    """
    Devuelve metadata del reto diario SIN revelar el personaje objetivo.
    Incluye pistas desbloqueables.
    """

    characters = await load_characters()

    if not characters:
        raise HTTPException(
            status_code=503,
            detail="No se pudieron cargar los personajes."
        )

    daily_character = get_daily_character(characters)

    if daily_character is None:
        raise HTTPException(
            status_code=503,
            detail="No se pudo determinar el personaje del día."
        )

    return {

        # ya existente
        "total_characters": len(characters),

        "arco": daily_character.get("arco"),
        "reino": daily_character.get("reino"),

        "message": "¡Adivina el personaje de hoy!",
    }



@app.get("/daily/reveal", tags=["Debug"], summary="[DEBUG] Revela el personaje del día")
async def reveal_daily():
    """
    ⚠️ Solo para desarrollo/pruebas. Eliminar en producción.
    """
    characters = await load_characters()
    if not characters:
        raise HTTPException(status_code=503, detail="No se pudieron cargar los personajes.")
    return get_daily_character(characters)


# ── Adivinar ────────────────────────────────────────────────────────────────

@app.post(
    "/guess",
    response_model=GuessResponse,
    tags=["Módulo 1"],
    summary="Enviar un intento de adivinanza",
)
async def guess_character(body: GuessRequest):
    """
    Recibe el nombre del personaje adivinado y devuelve
    la comparación campo por campo contra el personaje del día.
    """
    characters = await load_characters()
    if not characters:
        raise HTTPException(status_code=503, detail="No se pudieron cargar los personajes.")

    target = get_daily_character(characters)
    if target is None:
        raise HTTPException(status_code=503, detail="No se pudo determinar el personaje del día.")

    result = await process_guess(body.nombre, target)

    return GuessResponse(
        found=result["found"],
        is_correct=result["comparison"]["is_correct"] if result["found"] else False,
        message=result["message"],
        comparison=result["comparison"],
    )


@app.post(
    "/guess/custom",
    response_model=GuessResponse,
    tags=["Debug"],
    summary="[DEBUG] Adivinar contra un personaje objetivo específico",
)
async def guess_against_custom(
    body: GuessRequest,
    target_name: str = Query(..., description="Nombre del personaje objetivo"),
):
    """
    ⚠️ Solo para desarrollo/pruebas.
    """
    target = await get_character_by_name(target_name)
    if target is None:
        raise HTTPException(status_code=404, detail=f"Personaje objetivo '{target_name}' no encontrado.")

    result = await process_guess(body.nombre, target)

    return GuessResponse(
        found=result["found"],
        is_correct=result["comparison"]["is_correct"] if result["found"] else False,
        message=result["message"],
        comparison=result["comparison"],
    )


# ── Autocompletado ──────────────────────────────────────────────────────────

@app.get(
    "/characters/search",
    tags=["Módulo 1"],
    summary="Sugerencias de autocompletado",
)
async def search_characters(
    q: str = Query(..., min_length=1, description="Texto de búsqueda"),
    limit: int = Query(10, ge=1, le=50, description="Máximo de resultados"),
):
    """
    Devuelve nombres de personajes que coincidan con la búsqueda.
    """
    suggestions = await get_autocomplete_suggestions(q, limit=limit)
    return {"query": q, "results": suggestions}


# ── Datos de referencia ─────────────────────────────────────────────────────

@app.get("/characters", tags=["Referencia"], summary="Lista completa de personajes")
async def list_characters():
    """Devuelve todos los personajes con sus atributos completos."""
    return await load_characters()


@app.get("/characters/{nombre}", tags=["Referencia"], summary="Detalle de un personaje")
async def get_character(nombre: str):
    """Devuelve los datos de un personaje por su nombre."""
    char = await get_character_by_name(nombre)
    if char is None:
        raise HTTPException(status_code=404, detail=f"Personaje '{nombre}' no encontrado.")
    return char


@app.get("/meta/fields", tags=["Referencia"], summary="Valores únicos por campo")
async def get_field_values():
    """
    Devuelve los valores únicos disponibles para cada campo.
    """
    fields = ["genero", "reino", "orden", "arco"]
    return {
        field: await get_unique_values(field)
        for field in fields
    }


@app.get("/meta/arcs", tags=["Referencia"], summary="Orden canónico de arcos")
async def get_arc_order():
    """Devuelve el orden cronológico de arcos para las comparaciones."""
    return {"arcs": ARC_ORDER}