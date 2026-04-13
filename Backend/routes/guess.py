from fastapi import APIRouter
from db.mongo import characters

router = APIRouter()

@router.get("/test-db")
async def test_db():
    data = []

    async for doc in characters.find():
        doc["_id"] = str(doc["_id"])
        data.append(doc)

    return data