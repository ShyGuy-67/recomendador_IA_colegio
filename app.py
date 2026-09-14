import streamlit as st
from google import genai

# Configuración de la ventana
st.set_page_config(page_title="Recomendador Cultural IA", page_icon="🎬", layout="centered")

# 🔑 INGRESA TU API KEY DE GOOGLE AI STUDIO AQUÍ:
API_KEY = st.secrets["API_KEY"]

# System Prompt oficial de tu proyecto
SYSTEM_PROMPT = """
Eres un sistema experto de recomendación cultural de música, películas y libros. Tu objetivo es interactuar con el usuario para descubrir sus gustos y ofrecer recomendaciones altamente coherentes y personalizadas.

REGLAS DE INTERACCIÓN Y FLUJO:
1. INICIO: En tu primer mensaje di únicamente: "¿Qué te puedo recomendar hoy?" y espera la respuesta del usuario.
2. EVALUACIÓN DE AMBIGÜEDAD: 
   - Si los gustos son ambiguos o muy generales (ej. "Me gusta la música urbana"), NO recomiendes de inmediato. Haz PREGUNTAS DE EVALUACIÓN DE A UNO EN UNO (formato cuestionario corto) para precisar (ej. "¿Tienes algún artista o subgénero favorito como Trap o Boom Bap?").
   - Detén el cuestionario tan pronto tengas suficiente información relevante.
3. PROHIBIDO MOSTRAR PENSAMIENTO INTERNO: NUNCA incluyas tu proceso de análisis, cadenas de razonamiento o frases como ("Analizando a X y Y..."). Muestra directa y limpiamente el resultado al usuario.
4. MENOS TEXTO RELLENO: Sé conciso en las transiciones y preguntas. Guarda la profundidad de texto únicamente para la sección de recomendaciones.

ESTRUCTURA DE LAS RECOMENDACIONES (Mínimo 3 recomendaciones):
Cuando tengas datos suficientes, entrega las recomendaciones con el siguiente formato Markdown:

- 📌 **Categoría y Tags:** #Tag1 #Tag2 #Tag3
- 🎬📚🎵 **Título y Creador:** (Año)
- 💡 **¿Por qué te gustará?:** (Explicación extendida conectando directamente los intereses del usuario entre diferentes medios si aplica).
- 🎧 **Enlaces directos:**
- 🎬 [Buscar en Netflix](https://www.netflix.com/search?q=Nombre%20Pelicula%20o%20Serie)
  - 🔗 [Escuchar en Spotify](https://open.spotify.com/search/Nombre%20Artista%20Cancion)
  - 🎬 [Ver/Escuchar en YouTube](https://www.youtube.com/results?search_query=Nombre%20Artista%20Cancion)

REGLAS DE CIERRE:
-Si el usuario pide un formato específico (ej. álbumes, canciones, películas o libros), entrega ESTRICTAMENTE ese formato. Si pide álbumes, incluye el nombre del álbum completo y los links de búsqueda del álbum.
 Si recomiendas un artista en específico, incluye 1 tema clave representativo y los links de búsqueda de la canción.
- Al entregar las recomendaciones, pregunta de forma breve si el usuario está satisfecho o si desea ajustar/agregar algo a la búsqueda. NO des por terminada la interacción hasta que el usuario lo indique.
"""

st.title("🎬📚🎵 Recomendador Cultural IA")

# Memoria del chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "¿Qué te puedo recomendar hoy?"}
    ]

# Mostrar historial en pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto del usuario
if prompt := st.chat_input("Escribe tus gustos o responde al cuestionario..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if API_KEY == "TU_API_KEY_AQUI" or not API_KEY:
            st.error("⚠️ Olvidaste poner tu API Key en la línea 8 del archivo app.py")
        else:
            with st.spinner("Analizando tus gustos..."):
                try:
                    client = genai.Client(api_key=API_KEY)
                    
                    # Formatear el historial para Gemini
                    contents = []
                    for msg in st.session_state.messages:
                        role = "user" if msg["role"] == "user" else "model"
                        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
                    
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=contents,
                        config={
                            "system_instruction": SYSTEM_PROMPT,
                            "temperature": 0.6
                        }
                    )
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
