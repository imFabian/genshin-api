import requests
import pymongo
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Conectar a MongoDB Atlas
client = pymongo.MongoClient(MONGO_URI)
db = client["genshin-api"]

# Eliminar todas las colecciones antes de insertar nuevos datos
def clear_database():
    collections = db.list_collection_names()
    for collection in collections:
        db[collection].delete_many({})
    print("🗑️ Se eliminaron todos los datos de MongoDB.")

# URL de la API de la comunidad (seleccionada como la más actualizada)
API_URL = "https://genshin.jmp.blue/"

# Endpoints que necesitamos
ENDPOINTS = ["characters", "weapons", "artifacts", "materials", "enemies", "events", "banners"]

def fetch_and_store_data():
    """Obtiene los datos de la API y los almacena en MongoDB."""
    for endpoint in ENDPOINTS:
        response = requests.get(API_URL + endpoint)
        if response.status_code == 200:
            try:
                data = response.json()
                
                if isinstance(data, list):  # Si la respuesta es una lista de identificadores
                    full_data = []
                    for item in data:
                        item_response = requests.get(f"{API_URL}{endpoint}/{item}")
                        if item_response.status_code == 200:
                            full_data.append(item_response.json())
                        else:
                            print(f"⚠️ No se pudo obtener información detallada de {item} en {endpoint}.")
                    data = full_data
                
                if isinstance(data, list) and all(isinstance(doc, dict) for doc in data):
                    if data:  # Solo insertar si hay datos
                        db[endpoint].insert_many(data)
                        print(f"✅ {len(data)} registros insertados en la colección {endpoint}!")
                    else:
                        print(f"⚠️ No se encontraron datos válidos en {endpoint}.")
                else:
                    print(f"⚠️ Los datos obtenidos de {endpoint} no son una lista de diccionarios válidos. Mostrando respuesta JSON: {data}")
            except Exception as e:
                print(f"⚠️ Error al procesar datos de {endpoint}: {str(e)}")
        else:
            print(f"❌ Error al obtener datos de {endpoint}: {response.status_code}")

if __name__ == "__main__":
    print("🔄 Eliminando todos los datos de MongoDB...")
    clear_database()
    print("🔄 Iniciando actualización de la base de datos...")
    fetch_and_store_data()
    print("✅ Actualización completada!")
