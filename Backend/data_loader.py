"""
Cargador de datos de personajes desde JSON.
"""

import json
import os
from typing import List, Dict, Optional


# Ruta al archivo de datos
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "Data", "personajes.json")


def load_characters() -> List[Dict]:
    """
    Carga todos los personajes desde el archivo JSON.

    Returns:
        Lista de diccionarios con los datos de cada personaje.
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {DATA_FILE}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON: {e}")
        return []


def get_character_by_name(name: str, characters: List[Dict]) -> Optional[Dict]:
    """
    Busca un personaje por su nombre exacto.

    Args:
        name: Nombre del personaje a buscar
        characters: Lista de personajes

    Returns:
        Diccionario del personaje si existe, None si no se encuentra
    """
    for char in characters:
        if char.get("nombre", "").lower() == name.lower():
            return char
    return None


def get_character_names(characters: List[Dict]) -> List[str]:
    """
    Obtiene una lista con todos los nombres de personajes disponibles.

    Args:
        characters: Lista de personajes

    Returns:
        Lista de nombres de personajes
    """
    return [char.get("nombre") for char in characters if char.get("nombre")]


def get_unique_values(field: str, characters: List[Dict]) -> List[str]:
    """
    Obtiene todos los valores únicos de un campo específico.

    Args:
        field: Nombre del campo
        characters: Lista de personajes

    Returns:
        Lista de valores únicos para ese campo
    """
    values = set()
    for char in characters:
        if field in char:
            values.add(char[field])
    return sorted(list(values))