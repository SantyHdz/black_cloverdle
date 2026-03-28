"""
Lógica de comparación para el Módulo 1: Adivina el Personaje - Black Cloverdle
Compara los atributos del personaje adivinado contra el personaje objetivo.

Resultados posibles por campo:
    - "correct"  (VERDE)   : El valor es exactamente igual
    - "partial"  (AMARILLO): El valor comparte al menos un elemento (para campos de lista)
    - "incorrect"(ROJO)    : No hay coincidencia
    - "higher"   (↑)       : El valor real es mayor (para campos numéricos)
    - "lower"    (↓)       : El valor real es menor (para campos numéricos)
"""

from typing import Any, Dict, List, Optional
from data_loader import (
    get_character_by_name,
    get_character_names,
    load_characters,
)

# ---------------------------------------------------------------------------
# Tipos de resultado
# ---------------------------------------------------------------------------
CORRECT   = "correct"    # Verde
PARTIAL   = "partial"    # Amarillo
INCORRECT = "incorrect"  # Rojo
HIGHER    = "higher"     # ↑  (el objetivo es más alto / más tarde)
LOWER     = "lower"      # ↓  (el objetivo es más bajo / más temprano)


# ---------------------------------------------------------------------------
# Comparadores atómicos
# ---------------------------------------------------------------------------

def _compare_exact(guess_val: Any, target_val: Any) -> str:
    """Comparación exacta: verde o rojo."""
    return CORRECT if str(guess_val).strip().lower() == str(target_val).strip().lower() else INCORRECT


def _compare_numeric(guess_val: Any, target_val: Any) -> str:
    """
    Compara valores numéricos.
    Devuelve CORRECT, HIGHER (el objetivo es mayor que el guess) o LOWER.
    """
    try:
        g = float(str(guess_val).replace("cm", "").strip())
        t = float(str(target_val).replace("cm", "").strip())
    except (ValueError, TypeError):
        return INCORRECT

    if g == t:
        return CORRECT
    return HIGHER if t > g else LOWER


def _compare_arc(guess_val: Any, target_val: Any, arc_order: List[str]) -> str:
    """
    Compara arcos de debut usando un orden canónico.
    Devuelve CORRECT, HIGHER (el objetivo aparece más tarde) o LOWER.
    """
    g_norm = str(guess_val).strip().lower()
    t_norm = str(target_val).strip().lower()

    arc_order_lower = [a.lower() for a in arc_order]

    try:
        g_idx = arc_order_lower.index(g_norm)
        t_idx = arc_order_lower.index(t_norm)
    except ValueError:
        # Si alguno no está en la lista conocida, caemos a comparación exacta
        return CORRECT if g_norm == t_norm else INCORRECT

    if g_idx == t_idx:
        return CORRECT
    return HIGHER if t_idx > g_idx else LOWER


def _compare_list(guess_val: Any, target_val: Any) -> str:
    """
    Compara campos que pueden ser listas (atributos, raza, tipo de magia, etc.).
    - CORRECT  si los conjuntos son idénticos.
    - PARTIAL  si hay al menos un elemento en común.
    - INCORRECT si no hay ninguno en común.
    Acepta tanto listas como strings separados por coma.
    """
    def to_set(val: Any):
        if isinstance(val, list):
            return {str(v).strip().lower() for v in val}
        return {v.strip().lower() for v in str(val).split(",")}

    g_set = to_set(guess_val)
    t_set = to_set(target_val)

    if g_set == t_set:
        return CORRECT
    if g_set & t_set:          # intersección no vacía
        return PARTIAL
    return INCORRECT


# ---------------------------------------------------------------------------
# Orden canónico de arcos (ajusta según el manga/anime de Black Clover)
# ---------------------------------------------------------------------------
ARC_ORDER: List[str] = [
    "arco de presentación",
    "arco del examen de ingreso",
    "arco del dungeon",
    "arco del ataque al reino del trébol",
    "arco del torneo de magia",
    "arco de la invasión al reino del trébol",
    "arco del bosque de witches",
    "arco del éxodo del elf",
    "arco de la reencarnación",
    "arco de la invasión al reino de kiten",
    "arco del aguijón del diablo",
    "arco del reino del corazón",
    "arco de la triada oscura",
    "arco de spade",
    "arco del país del sol",
    "arco final",
]


# ---------------------------------------------------------------------------
# Comparación principal de un personaje
# ---------------------------------------------------------------------------

def compare_characters(guess: Dict, target: Dict) -> Dict[str, Any]:
    """
    Compara todos los atributos del personaje adivinado (guess) contra el objetivo (target).

    Args:
        guess:  Diccionario del personaje introducido por el jugador.
        target: Diccionario del personaje que se debe adivinar.

    Returns:
        Diccionario con la siguiente estructura por campo:
        {
            "nombre":       { "value": ..., "result": "correct"|"incorrect" },
            "genero":       { "value": ..., "result": ... },
            "atributos":    { "value": ..., "result": "correct"|"partial"|"incorrect" },
            "raza":         { "value": ..., "result": "correct"|"partial"|"incorrect" },
            "altura":       { "value": ..., "result": "correct"|"higher"|"lower" },
            "reino":        { "value": ..., "result": "correct"|"incorrect" },
            "orden":        { "value": ..., "result": "correct"|"incorrect" },
            "tipo_magia":   { "value": ..., "result": "correct"|"partial"|"incorrect" },
            "arco":         { "value": ..., "result": "correct"|"higher"|"lower" },
            "is_correct":   bool   <- True si TODOS los campos son CORRECT
        }
    """
    result: Dict[str, Any] = {}

    # --- Nombre (exacto) ---
    result["nombre"] = {
        "value": guess.get("nombre"),
        "result": _compare_exact(guess.get("nombre"), target.get("nombre")),
    }

    # --- Género (exacto) ---
    result["genero"] = {
        "value": guess.get("genero"),
        "result": _compare_exact(guess.get("genero"), target.get("genero")),
    }

    # --- Atributos (lista: Acompañante, Mago, Híbrido, No mago…) ---
    result["atributos"] = {
        "value": guess.get("atributos"),
        "result": _compare_list(
            guess.get("atributos", []),
            target.get("atributos", []),
        ),
    }

    # --- Raza (lista: Humano, Diablo, Elfo…) ---
    result["raza"] = {
        "value": guess.get("raza"),
        "result": _compare_list(
            guess.get("raza", []),
            target.get("raza", []),
        ),
    }

    # --- Altura (numérico + flecha) ---
    result["altura"] = {
        "value": guess.get("altura"),
        "result": _compare_numeric(guess.get("altura"), target.get("altura")),
    }

    # --- Reino (exacto) ---
    result["reino"] = {
        "value": guess.get("reino"),
        "result": _compare_exact(guess.get("reino"), target.get("reino")),
    }

    # --- Orden mágica (exacto) ---
    result["orden"] = {
        "value": guess.get("orden"),
        "result": _compare_exact(guess.get("orden"), target.get("orden")),
    }

    # --- Tipo de magia (lista, ya que algunos personajes tienen más de una) ---
    result["tipo_magia"] = {
        "value": guess.get("tipo_magia"),
        "result": _compare_list(
            guess.get("tipo_magia", []),
            target.get("tipo_magia", []),
        ),
    }

    # --- Arco debut (orden cronológico + flecha) ---
    result["arco"] = {
        "value": guess.get("arco"),
        "result": _compare_arc(
            guess.get("arco", ""),
            target.get("arco", ""),
            ARC_ORDER,
        ),
    }

    # --- ¿Adivinó completamente? ---
    all_results = [v["result"] for v in result.values() if isinstance(v, dict)]
    result["is_correct"] = all(r == CORRECT for r in all_results)

    return result


# ---------------------------------------------------------------------------
# Helpers de sesión de juego
# ---------------------------------------------------------------------------

def get_daily_character(characters: List[Dict]) -> Optional[Dict]:
    """
    Selecciona el personaje diario de forma determinista usando la fecha actual.
    Esto garantiza que todos los jugadores tengan el mismo personaje cada día.
    """
    if not characters:
        return None
    from datetime import date
    day_index = date.today().toordinal() % len(characters)
    return characters[day_index]


def process_guess(
    guess_name: str,
    target: Dict,
    characters: List[Dict],
) -> Dict[str, Any]:
    """
    Punto de entrada principal para procesar un intento del jugador.

    Args:
        guess_name: Nombre escrito por el jugador.
        target:     Personaje objetivo (el que se debe adivinar).
        characters: Lista completa de personajes (para buscar al adivinado).

    Returns:
        {
            "found":      bool,           # False si el nombre no existe en la BD
            "comparison": Dict | None,    # Resultado de la comparación
            "message":    str             # Mensaje legible para el frontend
        }
    """
    guess_char = get_character_by_name(guess_name, characters)

    if guess_char is None:
        return {
            "found": False,
            "comparison": None,
            "message": f"No se encontró el personaje '{guess_name}'. Verifica el nombre.",
        }

    comparison = compare_characters(guess_char, target)

    if comparison["is_correct"]:
        message = f"¡Correcto! El personaje era {target.get('nombre')}. 🎉"
    else:
        message = f"Incorrecto. Sigue intentando."

    return {
        "found": True,
        "comparison": comparison,
        "message": message,
    }


def get_autocomplete_suggestions(
    query: str,
    characters: List[Dict],
    limit: int = 10,
) -> List[str]:
    """
    Devuelve sugerencias de nombres de personajes que contengan el query.
    Útil para el campo de búsqueda del frontend.
    """
    query_lower = query.strip().lower()
    names = get_character_names(characters)
    matches = [n for n in names if query_lower in n.lower()]
    return matches[:limit]