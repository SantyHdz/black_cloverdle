<div align="center">

# ❁ BLACK CLOVERDLE ❁

### *¿Puedes adivinar al mago del día?*

![Svelte](https://img.shields.io/badge/Svelte-5-FF3E00?style=for-the-badge&logo=svelte&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

*Un juego tipo Wordle/DLE inspirado en el universo de [Black Clover](https://es.wikipedia.org/wiki/Black_Clover)*

</div>

---

## ✦ ¿Qué es Black Cloverdle?

**Black Cloverdle** es un juego web diario donde el jugador intenta adivinar un personaje del anime **Black Clover** basándose en sus atributos. Cada intento revela pistas visuales mediante tarjetas animadas con efecto flip, al estilo de los populares juegos DLE.

El personaje del día cambia automáticamente cada 24 horas. ¡Sin spoilers hasta que lo adivines!

---

## 🎮 Cómo jugar

1. **Escribe** el nombre de un personaje en el campo de búsqueda.
2. **Observa** las tarjetas animadas que revelan la comparación atributo por atributo.
3. **Usa las pistas de color** para guiar tus siguientes intentos.
4. **Desbloquea pistas adicionales** conforme avanzas en los intentos.

### Indicadores de resultado

| Color | Significado |
|-------|-------------|
| 🟩 **Verde** | El atributo coincide exactamente |
| 🟨 **Amarillo** | Coincidencia parcial (en listas como magia o raza) |
| 🟥 **Rojo** | El atributo no coincide |
| 🔵 **↑ Azul** | El valor real es **mayor / más tarde** |
| 🔵 **↓ Azul** | El valor real es **menor / más temprano** |

### Atributos comparados

```
Nombre  ·  Género  ·  Atributos  ·  Raza  ·  Altura  ·  Reino  ·  Orden  ·  Magia  ·  Arco
```

### Pistas desbloqueables

| Intento | Pista disponible |
|---------|-----------------|
| 5 | 🏰 **País de origen** del personaje |
| 7 | 📖 **Primer arco de aparición** |

---

## 🧩 Módulos del juego

El proyecto está diseñado con múltiples modos de juego:

| Módulo | Nombre | Estado |
|--------|--------|--------|
| 1 | 🧙 **Adivina el Personaje** — modo clásico de atributos | ✅ Disponible |
| 2 | 💥 **¿Quién lanza este hechizo?** — GIF borroso que mejora con cada fallo | 🔜 Próximamente |
| 3 | 🗣️ **Frases** — adivina al personaje por su frase célebre | 🔜 Próximamente |
| 4 | 🧠 **¿Quién es este mago?** — imagen que se revela progresivamente | 🔜 Próximamente |

---

## 🏗️ Arquitectura del proyecto

```
black_cloverdle/
│
├── 📁 Backend/
│   ├── 📁 db/
│   │   └── mongo.py           # Conexión a MongoDB Atlas (Motor async)
│   ├── 📁 routes/
│   │   └── guess.py           # Rutas de prueba de conexión
│   ├── data_loader.py         # Carga y búsqueda de personajes
│   ├── logic.py               # Lógica de comparación y juego
│   └── main.py                # FastAPI app + todos los endpoints
│
├── 📁 Frontend/
│   └── 📁 src/
│       ├── 📁 lib/
│       │   ├── 📁 components/
│       │   │   ├── GuessInput.svelte   # Input con autocompletado
│       │   │   ├── GuessRow.svelte     # Fila de intento completa
│       │   │   └── FlipCard.svelte     # Tarjeta con animación flip
│       │   └── api.ts                  # Cliente HTTP hacia el backend
│       └── 📁 routes/
│           └── +page.svelte            # Página principal del juego
│
└── 📁 Data/
    └── personajes.json        # Dataset de personajes de Black Clover
```

---

## 🚀 Instalación y configuración

### Requisitos previos

- Python **3.10+**
- Node.js **20+**
- Una cuenta en [MongoDB Atlas](https://www.mongodb.com/atlas) (gratuita)

---

### ⚙️ Backend

**1. Crear y activar entorno virtual**

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

**2. Instalar dependencias**

```bash
pip install fastapi uvicorn motor pydantic python-dotenv
```

**3. Configurar variables de entorno**

Crea un archivo `.env` en la raíz del proyecto:

```env
MONGO_URI=mongodb+srv://<usuario>:<password>@cluster0.gddax79.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=blackcloverdle
```

**4. Iniciar el servidor**

```bash
uvicorn Backend.main:app --reload
```

El servidor arrancará en `http://127.0.0.1:8000`.
Documentación interactiva disponible en `http://127.0.0.1:8000/docs`.

---

### 🎨 Frontend

**1. Instalar dependencias**

```bash
cd Frontend
npm install
```

**2. Iniciar el servidor de desarrollo**

```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`.

> El frontend está configurado con un proxy en `vite.config.ts` que redirige `/api/*` → `http://127.0.0.1:8000`, por lo que no necesitas configurar CORS manualmente durante el desarrollo.

---

## 🌐 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/daily` | Metadata del reto diario (sin spoilers) |
| `POST` | `/guess` | Enviar un intento de adivinanza |
| `GET` | `/characters/search?q=` | Autocompletado de nombres |
| `GET` | `/characters` | Lista completa de personajes |
| `GET` | `/characters/{nombre}` | Detalle de un personaje |
| `GET` | `/meta/fields` | Valores únicos por campo |
| `GET` | `/meta/arcs` | Orden canónico de arcos |
| `GET` | `/daily/reveal` | ⚠️ [Debug] Revela el personaje del día |

---

## 🛠️ Stack tecnológico

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** — Framework web asíncrono de alto rendimiento
- **[Motor](https://motor.readthedocs.io/)** — Driver asíncrono para MongoDB
- **[Pydantic](https://docs.pydantic.dev/)** — Validación de datos y esquemas
- **[Uvicorn](https://www.uvicorn.org/)** — Servidor ASGI

### Frontend
- **[SvelteKit 2](https://kit.svelte.dev/)** con **Svelte 5** (Runes API)
- **[TypeScript](https://www.typescriptlang.org/)** — Tipado estático
- **[Tailwind CSS 4](https://tailwindcss.com/)** + CSS personalizado con animaciones
- **[Vite 7](https://vitejs.dev/)** — Bundler y servidor de desarrollo

### Base de datos
- **[MongoDB Atlas](https://www.mongodb.com/atlas)** — Base de datos en la nube (tier gratuito, 512 MB)

---

## 🧠 Lógica de comparación

El motor de comparación en `Backend/logic.py` evalúa cada atributo con una estrategia distinta:

```python
# Campos exactos (género, reino, orden)
→ "correct" si coincide, "incorrect" si no

# Campos numéricos (altura)
→ "correct" | "higher" (↑) | "lower" (↓)

# Campos de lista (tipo_magia, raza, atributos)
→ "correct" si todas coinciden
→ "partial" si hay intersección
→ "incorrect" si no hay ninguna coincidencia

# Campo de arco
→ Comparación por posición en orden cronológico canónico
→ "correct" | "higher" (más tarde) | "lower" (antes)
```

---

## 🗺️ Roadmap

### v1.0 — MVP ✅
- [x] Backend con FastAPI y MongoDB
- [x] Módulo 1: Adivina el Personaje
- [x] Frontend con SvelteKit y animaciones flip
- [x] Autocompletado de personajes
- [x] Sistema de pistas desbloqueables
- [x] Personaje diario determinista

### v2.0 — En desarrollo 🔜
- [ ] Módulo 2: Adivina el hechizo (GIF progresivo)
- [ ] Módulo 3: Adivina la frase
- [ ] Módulo 4: Adivina el mago (imagen progresiva)
- [ ] Estadísticas de victorias y rachas
- [ ] Modo infinito
- [ ] Sistema de autenticación y rankings

---

## 👨‍💻 Autor

Desarrollado con 🖤 por **Santy** — fan del anime y del universo de Black Clover.

---

## 📜 Licencia

[MIT License](LICENSE) — libre para usar, modificar y distribuir.

---

<div align="center">

*"No importa qué tipo de magia tengas. Lo que importa es hasta dónde llegas con ella."*
— **Yami Sukehiro**

**❁ ¡Que el grimorio te guíe! ❁**

</div>
