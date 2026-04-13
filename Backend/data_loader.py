from typing import List, Dict, Optional
from db.mongo import characters as characters_collection


async def load_characters() -> List[Dict]:
    """
    Carga todos los personajes desde la colección de MongoDB.

    Returns:
        Lista de diccionarios con los datos de cada personaje.
    """
    try:
        result = []
        async for doc in characters_collection.find():
            doc["_id"] = str(doc["_id"])
            result.append(doc)
        return result
    except Exception as e:
        print(f"Error al cargar personajes desde MongoDB: {e}")
        return []


async def get_character_by_name(name: str) -> Optional[Dict]:
    """
    Busca un personaje por su nombre exacto (insensible a mayúsculas).

    Args:
        name: Nombre del personaje a buscar

    Returns:
        Diccionario del personaje si existe, None si no se encuentra
    """
    try:
        doc = await characters_collection.find_one(
            {"nombre": {"$regex": f"^{name}$", "$options": "i"}}
        )
        if doc:
            doc["_id"] = str(doc["_id"])
        return doc
    except Exception as e:
        print(f"Error al buscar personaje '{name}': {e}")
        return None


async def get_character_names() -> List[str]:
    """
    Obtiene una lista con todos los nombres de personajes disponibles.

    Returns:
        Lista de nombres de personajes
    """
    try:
        cursor = characters_collection.find({}, {"nombre": 1, "_id": 0})
        names = []
        async for doc in cursor:
            if doc.get("nombre"):
                names.append(doc["nombre"])
        return names
    except Exception as e:
        print(f"Error al obtener nombres: {e}")
        return []


async def get_unique_values(field: str) -> List[str]:
    """
    Obtiene todos los valores únicos de un campo específico.

    Args:
        field: Nombre del campo

    Returns:
        Lista de valores únicos para ese campo
    """
    try:
        values = await characters_collection.distinct(field)
        return sorted([str(v) for v in values if v is not None])
    except Exception as e:
        print(f"Error al obtener valores únicos para '{field}': {e}")
        return []