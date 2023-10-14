import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = ""

def limpiar_texto(texto):
    # Elimina saltos de línea y espacios en blanco adicionales.
    texto_limpio = " ".join(texto.split())
    return texto_limpio


def analizar_sentimientos(texto, max_respuesta_length=100):
    limpiar_texto(texto)
    prompt = (
        f"Por favor analiza el sentimiento predominante en el siguiente texto : '{texto}'. Pero quiero que me des una"
        f"explicacion mas detallada como si fuese un profesional (no más de {max_respuesta_length} tokens),")

    respuesta = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        n=1,
        max_tokens=max_respuesta_length * 2,  # Valor suficientemente grande para evitar frases cortadas.
        temperature=0.5
    )

    respuesta_formateada = respuesta.choices[0].text.strip()

    # Realizar un recorte si la respuesta excede la longitud máxima deseada
    if len(respuesta_formateada) > max_respuesta_length:
        respuesta_formateada = " ".join(respuesta_formateada.split()[:max_respuesta_length])

    # Divide la respuesta en párrafos de aproximadamente 75 caracteres
    respuesta_formateada = "\n".join(
        [respuesta_formateada[i:i + 75] for i in range(0, len(respuesta_formateada), 75)])

    return respuesta_formateada

# print("ANALISIS DE SENTIMIENTOS EN TEXTOS:\n"
#       "A tener en cuenta :\n"
#       "Si el texto que ingresa no espeficica a que hace referencia (peliculas, personas, articulos, etc.)"
#       " puede que de un analisis inexacto\n"
#       "A textos mejor especificados analisis mas exactos\n")
# texto_a_analizar = input("Ingresa el texto que quiere analizar :")
#
# sentimiento = analizar_sentimientos(texto_a_analizar)
#
# # Reemplazar el punto por "Texto analizado:"
# #sentimiento = "Texto analizado:" + sentimiento
#
# # Imprimir la respuesta en una nueva línea
# print("\n" + sentimiento)
# Configurar la página de Streamlit
st.title("Análisis de Sentimientos en Textos")
st.write("A tener en cuenta: Si el texto que ingresa no especifica a qué hace referencia (películas, personas, artículos, etc.),"
         " puede que el análisis sea inexacto."
         "En textos mejor especificados, el análisis será más preciso.")

# Columna izquierda con el campo de texto
texto_a_analizar = st.text_area("Ingrese el texto que quiere analizar:")
if st.button("Analizar Texto"):
    if texto_a_analizar:
        st.subheader("Resultado del Análisis:")
        sentimiento = analizar_sentimientos(texto_a_analizar)
        st.write(sentimiento)
