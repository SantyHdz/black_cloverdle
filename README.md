🧙‍♂️ Black Cloverdle

Juego tipo Wordle/DLE inspirado en el anime Black Clover, donde los jugadores deben adivinar personajes basándose en sus atributos.

Este proyecto está basado en la lógica de juegos como Wordle y Narutodle, pero adaptado al universo de Black Clover.

🎮 Descripción del Proyecto

Black Cloverdle es un juego web donde el jugador debe adivinar un personaje del anime Black Clover utilizando pistas relacionadas con:

Nombre
Género
Edad
Altura
Reino
Orden mágica
Tipo de magia
Arco debut

Cada intento muestra información visual:

🟩 Verde → Correcto
🟨 Amarillo → Parcial
🟥 Rojo → Incorrecto
⬆️ ⬇️ → Mayor o menor (altura/arco)

El proyecto contará con múltiples modos de juego.

🧩 Módulos del Juego
🧙‍♂️ Módulo 1 — Adivina el Personaje

Modo principal donde el jugador intenta adivinar el personaje usando atributos.

Atributos:

Nombre
Género
Atributos secundarios
Raza
Altura
Reino
Orden
Tipo de magia
Arco debut
💥 Módulo 2 — ¿Quién lanza este hechizo?

El jugador ve:

Un GIF borroso
En blanco y negro

Cada fallo:

Mejora la calidad del GIF
Puede añadirse color como ayuda

Objetivo:

Adivinar el personaje que ejecutó el ataque.

🗣️ Módulo 3 — Frases

Se muestra:

Una frase famosa de un personaje.

Objetivo:

Adivinar quién la dijo.

🧠 Módulo 4 — ¿Quién es este mago?

Se muestra:

Una imagen borrosa del personaje.

Cada fallo:

La imagen se vuelve más nítida.

🧱 Tecnologías Utilizadas
Backend
Python 3.10+
FastAPI
Uvicorn
Motor (MongoDB async driver)
Pydantic
Frontend
SvelteKit
TypeScript
CSS
Animaciones personalizadas (Flip Cards)
Base de Datos
MongoDB Atlas
🏗️ Arquitectura del Proyecto
black_cloverdle/
│
├── Backend/
│   ├── db/
│   │   └── mongo.py
│   │
│   ├── routes/
│   │   └── characters.py
│   │
│   ├── models/
│   │   └── character.py
│   │
│   ├── main.py
│   └── requirements.txt
│
├── Frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   │   ├── GuessInput.svelte
│   │   │   │   ├── GuessRow.svelte
│   │   │   │   └── FlipCard.svelte
│   │   │   │
│   │   │   └── api/
│   │   │       └── api.ts
│   │   │
│   │   ├── routes/
│   │   │   └── +page.svelte
│   │   │
│   │   └── app.css
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── data/
│   └── characters.json
│
├── README.md
└── .env

⚙️ Instalación del Proyecto
1️⃣ Clonar repositorio
git clone https://github.com/tu-usuario/black_cloverdle.git

cd black_cloverdle

🧪 Backend Setup
2️⃣ Crear entorno virtual

Windows:

python -m venv .venv

.venv\Scripts\activate


Linux / Mac:

python3 -m venv .venv

source .venv/bin/activate

3️⃣ Instalar dependencias
pip install -r requirements.txt


Ejemplo requirements.txt:

fastapi
uvicorn
motor
pydantic
python-dotenv

🧬 Configurar MongoDB
4️⃣ Crear archivo .env
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net

DATABASE_NAME=black_cloverdle

5️⃣ Configurar conexión Mongo

Archivo:

Backend/db/mongo.py


Ejemplo:

from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)

db = client["black_cloverdle"]

characters = db["characters"]

🚀 Ejecutar Backend
uvicorn Backend.main:app --reload


Servidor:

http://127.0.0.1:8000


Documentación API:

http://127.0.0.1:8000/docs

🎨 Frontend Setup

Ir a la carpeta:

cd Frontend

6️⃣ Instalar dependencias
npm install

7️⃣ Ejecutar frontend
npm run dev


Servidor:

http://localhost:5173

🔄 Flujo de Datos
Usuario
   ↓
Frontend (Svelte)
   ↓
API (FastAPI)
   ↓
MongoDB

📦 Endpoints Principales

Ejemplos:

GET /characters
GET /characters/{name}
POST /guess
GET /random-character

🧠 Lógica del Juego

Comparación de atributos:

Resultado	Significado
Verde	Correcto
Amarillo	Parcial
Rojo	Incorrecto
↑	Mayor
↓	Menor
📊 Funcionalidades Futuras
Ranking diario
Racha de victorias
Estadísticas
Modo infinito
Sistema de login
Guardado en base de datos

Estas funcionalidades forman parte del diseño original del proyecto.

🧪 Testing

Ejecutar pruebas:

pytest

🧰 Scripts útiles

Actualizar dependencias:

pip freeze > requirements.txt

📌 Roadmap
Versión 1.0
 Backend básico
 MongoDB
 Módulo 1 funcional
 Frontend con animaciones
Versión 2.0
 GIF mode
 Frases
 Imagen borrosa
 Estadísticas
👨‍💻 Autor

Santy

Desarrollador del proyecto Black Cloverdle

📜 Licencia

MIT License

🧙‍♂️ Créditos

Inspirado en:

Wordle
Narutodle
Anime: Black Clover
⭐ Recomendación

Si subes esto a GitHub:

Añade imágenes del juego
Añade GIFs
Añade capturas del frontend

Eso hace que el repo se vea mucho más profesional.
