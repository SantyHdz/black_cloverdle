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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # En producción reemplazar con el origen del frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache en memoria para no releer el JSON en cada request
_characters: List[Dict] = []

def get_characters() -> List[Dict]:
    global _characters
    if not _characters:
        _characters = load_characters()
    return _characters


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
def root():
    """Verificación de que la API está corriendo."""
    return {"status": "ok", "game": "Black Cloverdle"}


# ── Personaje diario ────────────────────────────────────────────────────────

@app.get("/daily", tags=["Módulo 1"], summary="Personaje del día (sin spoilers)")
def get_daily():
    """
    Devuelve metadata del reto diario SIN revelar el personaje objetivo.
    Útil para que el frontend muestre el número de personajes disponibles.
    """
    characters = get_characters()
    if not characters:
        raise HTTPException(status_code=503, detail="No se pudieron cargar los personajes.")

    daily = get_daily_character(characters)
    return {
        "total_characters": len(characters),
        "message": "¡Adivina el personaje de hoy!",
        # No devolvemos el nombre del personaje diario aquí
    }


@app.get("/daily/reveal", tags=["Debug"], summary="[DEBUG] Revela el personaje del día")
def reveal_daily():
    """
    ⚠️ Solo para desarrollo/pruebas. En producción este endpoint debe eliminarse o protegerse.
    Devuelve el personaje objetivo del día.
    """
    characters = get_characters()
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
def guess_character(body: GuessRequest):
    """
    Recibe el nombre del personaje adivinado por el jugador y devuelve
    la comparación campo por campo contra el personaje del día.

    ### Resultados posibles por campo:
    | Valor        | Significado                                    |
    |--------------|------------------------------------------------|
    | `correct`    | 🟢 Verde — valor exactamente igual             |
    | `partial`    | 🟡 Amarillo — coincidencia parcial (listas)    |
    | `incorrect`  | 🔴 Rojo — sin coincidencia                     |
    | `higher`     | ⬆️ El objetivo tiene un valor mayor/posterior  |
    | `lower`      | ⬇️ El objetivo tiene un valor menor/anterior   |
    """
    characters = get_characters()
    if not characters:
        raise HTTPException(status_code=503, detail="No se pudieron cargar los personajes.")

    target = get_daily_character(characters)
    if target is None:
        raise HTTPException(status_code=503, detail="No se pudo determinar el personaje del día.")

    result = process_guess(body.nombre, target, characters)

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
def guess_against_custom(body: GuessRequest, target_name: str = Query(..., description="Nombre del personaje objetivo")):
    """
    ⚠️ Solo para desarrollo/pruebas.
    Permite enviar un intento contra cualquier personaje objetivo (no el del día).
    """
    characters = get_characters()
    if not characters:
        raise HTTPException(status_code=503, detail="No se pudieron cargar los personajes.")

    target = get_character_by_name(target_name, characters)
    if target is None:
        raise HTTPException(status_code=404, detail=f"Personaje objetivo '{target_name}' no encontrado.")

    result = process_guess(body.nombre, target, characters)

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
def search_characters(
    q: str = Query(..., min_length=1, description="Texto de búsqueda"),
    limit: int = Query(10, ge=1, le=50, description="Máximo de resultados"),
):
    """
    Devuelve una lista de nombres de personajes que coincidan con la búsqueda.
    Usar para alimentar el campo de autocompletado del frontend.
    """
    characters = get_characters()
    suggestions = get_autocomplete_suggestions(q, characters, limit=limit)
    return {"query": q, "results": suggestions}


# ── Datos de referencia ─────────────────────────────────────────────────────

@app.get("/characters", tags=["Referencia"], summary="Lista completa de personajes")
def list_characters():
    """Devuelve todos los personajes disponibles con sus atributos completos."""
    return get_characters()


@app.get("/characters/{nombre}", tags=["Referencia"], summary="Detalle de un personaje")
def get_character(nombre: str):
    """Devuelve los datos completos de un personaje por su nombre."""
    characters = get_characters()
    char = get_character_by_name(nombre, characters)
    if char is None:
        raise HTTPException(status_code=404, detail=f"Personaje '{nombre}' no encontrado.")
    return char


@app.get("/meta/fields", tags=["Referencia"], summary="Valores únicos por campo")
def get_field_values():
    """
    Devuelve los valores únicos disponibles para cada campo.
    Útil para construir filtros o validaciones en el frontend.
    """
    characters = get_characters()
    fields = ["genero", "reino", "orden", "arco"]
    return {
        field: get_unique_values(field, characters)
        for field in fields
    }


@app.get("/meta/arcs", tags=["Referencia"], summary="Orden canónico de arcos")
def get_arc_order():
    """Devuelve el orden cronológico de arcos utilizado para las comparaciones de debut."""
    return {"arcs": ARC_ORDER}