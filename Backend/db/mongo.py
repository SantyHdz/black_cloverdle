#No suelo comentar codigo alejo JAJAJAJAJAJA considerate afortunado te amo preciosin JAJAJAJA XD
from motor.motor_asyncio import AsyncIOMotorClient
# nuestro string
MONGO_URI = "mongodb+srv://admin:santilejo123@cluster0.gddax79.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGO_URI)
# Alejin aqui tomamos el nombre de la BD que yo cree
db = client["blackcloverdle"]
# Y en mongo se trabajan colecciones en los cluster en nuestro caso yo cree este que tiene el json de los personajes
characters = db["characters"]
