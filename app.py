import streamlit as st
import openai
import os
from dotenv import load_dotenv

import requests


# load_dotenv()

# Función para restablecer la variable de sesión
def reset_session():
    session_state.api_key = None
    openai.api_key = ""


# Crear o recuperar la variable de sesión
session_state = st.session_state
if not hasattr(session_state, 'api_key'):
    reset_session()  # Restablecer la variable de sesión si no existe

# Título de la app
st.write("<h1 style='color: #66b3ff; font-size: 36px;'>Esta aplicación funciona con API Key de OpenAI</h1>",
         unsafe_allow_html=True)

# Entrada de API key
user_input = st.text_input("Ingresa tu API key de OpenAI:", type="password")

# Botón de validación
if st.button("Validar API Key"):
    session_state.api_key = user_input  # Almacena la API key en la sesión

try:
    if session_state.api_key:
        openai.api_key = session_state.api_key  # Configura la API key de la sesión

        response = openai.Completion.create(
            engine="davinci", prompt="This is a test."
        )

        st.success("API key válida. Puedes utilizar la aplicación.")
        # Coloca aquí el código de tu aplicación que requiere la API key
    else:
        st.error("Debes ingresar tu API key para validarla y acceder a la aplicación.")
except Exception as e:
    st.error("API key no válida. Acceso denegado.")

# Agregar una línea horizontal
st.write('<hr>', unsafe_allow_html=True)


def limpiar_texto(texto):
    # Elimina saltos de línea y espacios en blanco adicionales.
    texto_limpio = " ".join(texto.split())
    return texto_limpio


# Diccionario de emociones y palabras clave
emociones_dict = {
    "gusto": ["gusto", "encanta", "encantan", "me gusta", "es un buen", "hermosa", "hermoso", "satisfacción"],
    "amor": ["gusto", "encanta", "amor", "amo", "me gusta", "enamoramiento"],
    "interesante": ["interesante", "fascinante", "atractivo", "intrigante"],
    "enfado": ["enfado", "enojado", "molesto", "rabia", "basta", "furioso"],
    "tristeza": ["tristeza", "melancolía", "abatido", "deprimido", "triste"],
    "felicidad": ["feliz", "alegría", "me gusta" "contento", "entusiasmado", "satisfacción"],
    "sorpresa": ["sorpresa", "asombro", "increíble", "impactante", "tremendo"],
    "miedo": ["miedo", "aterrorizado", "asustado", "temor", "panico"],
    "desprecio": ["desprecio", "asco", "repulsión", "detesto"],
    "divertido": ["divertido", "divertirnos", "chiste", "risa", "humor"],
    "orgullo": ["orgullo", "satisfacción", "elogio", "dignidad"],
    "culpa": ["culpa", "remordimiento", "arrepentimiento", "penitencia"],
    "emoción": ["emoción", "emocionado", "sentir", "experiencia"],
    "confusión": ["confusión", "desconcertado", "perplejo", "incomprensión"],
    "aburrimiento": ["aburrimiento", "monótono", "tedio", "insípido", "aburrido"],
    "tranquilidad": ["tranquilidad", "serenidad", "paz", "calma"],
    "indiferencia": ["indiferencia", "apático", "desinterés", "neutral", "me da lo mismo", "me da igual"],
    "esperanza": ["esperanza", "optimismo", "esperanzado"],
    "inquietud": ["inquietud", "nerviosismo", "ansiedad", "preocupación"],

}


def analizar_sentimientos(texto, max_respuesta_length=100):
    limpiar_texto(texto)
    prompt = (
        f"Por favor analiza el sentimiento predominante en el siguiente texto: '{texto}'. El sentimiento es: Pero quiero que me des una"
        f"explicación más detallada como si fuese un profesional (no más de {max_respuesta_length} tokens),")
    openai.api_key = session_state.api_key  # Configura la API key de la sesión
    respuesta = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        n=1,
        max_tokens=max_respuesta_length * 2,  # Valor suficientemente grande para evitar frases cortadas.
        temperature=0.5
    )

    respuesta_formateada = respuesta.choices[0].text.strip()
    openai.api_key = ""  # Configura la API key de la sesión
    # Añadir la detección de emociones utilizando el diccionario
    emociones = {}  # Un diccionario para almacenar las emociones y sus porcentajes
    for emocion, palabras_clave in emociones_dict.items():
        for palabra_clave in palabras_clave:
            if palabra_clave in respuesta_formateada:
                emociones[emocion] = respuesta_formateada.count(palabra_clave) / len(respuesta_formateada)

    # Rellenar las emociones faltantes con cero
    for emocion in emociones_dict.keys():
        if emocion not in emociones:
            emociones[emocion] = 0.0

    # Realizar un recorte si la respuesta excede la longitud máxima deseada
    if len(respuesta_formateada) > max_respuesta_length:
        respuesta_formateada = " ".join(respuesta_formateada.split()[:max_respuesta_length])

    # Divide la respuesta en párrafos de aproximadamente 75 caracteres
    respuesta_formateada = "".join(
        [respuesta_formateada[i:i + 75] for i in range(0, len(respuesta_formateada), 75)])

    return respuesta_formateada, emociones


# imagen del banner
imagen = "banner.jpg"
st.image(imagen)
# Agregar una línea horizontal
st.write('<hr>', unsafe_allow_html=True)
st.write("<h1 style='color: #66b3ff;font-size: 28px;'>Análisis Textual:</h1>", unsafe_allow_html=True)

st.write("A tener en cuenta:")
st.write("Si el texto que ingresa no especifica a qué hace referencia (películas, personas, artículos, etc.),"
         " puede que el análisis sea inexacto."
         "En textos mejor especificados, el análisis será más preciso.")

# Columna izquierda con el campo de texto
with st.container():
    try:
        texto_a_analizar = st.text_area("Ingrese el texto que quiere analizar:")
        if st.button("Analizar Texto"):
            # Agregar una línea horizontal
            st.write('<hr>', unsafe_allow_html=True)
            if texto_a_analizar:
                st.subheader("Resultado del Análisis:")
                resultado_analisis, emociones = analizar_sentimientos(texto_a_analizar)
                st.write(resultado_analisis)
                # Agregar una línea horizontal
                st.write('<hr>', unsafe_allow_html=True)
                # Mostrar el gráfico de barras con emociones
                st.subheader("Emociones Detectadas:")
                st.bar_chart(emociones)
    except Exception as e:
        st.error("Acceso Denegado")

st.divider()

st.write("<h1 style='color: #66b3ff;font-size: 28px;'>Análisis Grafico:</h1>", unsafe_allow_html=True)

with st.container():
    st.write("En cuanto al gráfico el resultado puede tener diferentes enfoques, ya que el modelo trabaja "
             "bajo probabilidades por lo que un mismo texto puede tener diferentes puntos de vista."
             "Puede buscar variantes con el botón de Analizar Gráfico Nuevamente")

    if st.button("Analizar Gráfico Nuevamente"):
        try:
            # Agregar una línea horizontal
            st.write('<hr>', unsafe_allow_html=True)
            resultado_analisis, emociones = analizar_sentimientos(texto_a_analizar)
            st.subheader("Emociones Detectadas:")
            st.bar_chart(emociones)
        except Exception as e:
            st.error("No se pudo generar el gráfico")
#
#
st.write('<hr>', unsafe_allow_html=True)
# Verificar si la API key está en la sesión
if session_state.api_key:
    st.write(f"Sesión establecida")
else:
    st.write("API key no presente en la sesión")

# Botón para cerrar la sesión (ya lo tienes en tu código)
if st.button("Cerrar Sesión"):
    reset_session()
