import requests
from bs4 import BeautifulSoup
import pymongo
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Conectar a MongoDB Atlas
client = pymongo.MongoClient(MONGO_URI)
db = client["genshin-api"]  # Nombre de la base de datos
collection = db["characters"]  # Colección donde guardaremos los personajes

# URL de la wiki de Genshin Impact
URL = "https://genshin-impact.fandom.com/wiki/Characters/List"

# Hacer la solicitud HTTP
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Buscar la tabla de personajes
table = soup.find("table", {"class": "article-table"})
rows = table.find_all("tr")[1:]  # Omitimos la primera fila (encabezados)

characters = []

for row in rows:
    cols = row.find_all("td")
    if len(cols) > 1:
        name = cols[0].text.strip()
        element = cols[1].text.strip()
        rarity = cols[2].text.strip()
        weapon = cols[3].text.strip()

        # Verificar si rarity tiene un valor antes de convertirlo
        rarity_value = rarity.replace("★", "").strip()  # Quita espacios y caracteres no numéricos
        rarity_value = int(rarity_value) if rarity_value.isdigit() else None  # Si es número, lo convierte, si no, lo deja como None

        character = {
            "name": name,
            "element": element,
            "rarity": rarity_value,  # Rareza con manejo de errores
            "weaponType": weapon
        }

        characters.append(character)

# Insertar datos en MongoDB Atlas
if characters:
    collection.insert_many(characters)
    print(f"✅ {len(characters)} personajes agregados a MongoDB!")
else:
    print("❌ No se encontraron personajes.")

client.close()
