import pymongo
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Conectar a MongoDB Atlas
client = pymongo.MongoClient(MONGO_URI)
db = client["genshin-api"]  # Base de datos

# Función para limpiar todas las colecciones antes de una nueva ejecución
def clear_database():
    collections = ["characters", "weapons", "artifacts", "materials", "enemies", "events", "banners"]
    for collection in collections:
        db[collection].delete_many({})  # Borra documentos sin eliminar la colección
    print("🗑️ Se eliminaron todos los documentos en la base de datos, sin eliminar las colecciones.")

# Función para verificar el tamaño de la base de datos
def get_db_stats():
    stats = db.command("dbstats")
    print(f"📊 Tamaño total de la base de datos: {stats['dataSize'] / (1024 * 1024):.2f} MB")
    return stats
