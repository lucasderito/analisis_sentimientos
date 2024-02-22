import streamlit as st
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from openai import OpenAI

import requests

# imagen = "banner2.jpg"
# st.image(imagen)
# # Agregar una línea horizontal
# st.write('<hr>', unsafe_allow_html=True)
# st.write("<h1 style='color: #66b3ff;font-size: 28px;'>Análisis Textual:</h1>", unsafe_allow_html=True)
# load_dotenv() no se usa pq no hay variables de entorno , en un comienzo lo utilice antes de hacer la validacion con apikey directamente en el front de la app

# Función para restablecer la variable de sesión
def reset_session():
    session_state.api_key = None



# Crear o recuperar la variable de sesión
session_state = st.session_state
if not hasattr(session_state, 'api_key'):
    reset_session()  # Restablecer la variable de sesión si no existe

imagen = "banner.jpg"
st.image(imagen)
# Título de la app
st.write("<h1 style='color: #66b3ff; font-size: 36px;'>Esta aplicación funciona con API Key de OpenAI</h1>",
         unsafe_allow_html=True)


# Mostrar el cuadro de entrada de la API key si la sesión no está establecida
if session_state.api_key is None:
    user_input = st.text_input("Ingresa tu API key de OpenAI:", type="password")
else:
    user_input = ""  # Cuadro de entrada en blanco si la sesión está establecida

# Botón de validación
if st.button("Validar API Key"):
    session_state.api_key = user_input  # Almacena la API key en la sesión


try:
    if session_state.api_key:

        client = OpenAI(api_key=session_state.api_key)

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ]
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


def analizar_sentimientos(texto, max_respuesta_length=200):
    limpiar_texto(texto)
    prompt = (
        f"Por favor analiza el sentimiento predominante en el siguiente texto: '{texto}'Pero quiero que me des una explicación más detallada como si fueses un profesional"
        f" El sentimiento es: "
        f" (no más de {max_respuesta_length} tokens),")
    client = OpenAI(api_key=session_state.api_key)
    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        #engine="gpt-3.5-turbo-instruct",
        #prompt=prompt,
        messages=[
            {"role": "system", "content": "Menciona los sentimientos relacionados al texto ingresado"},
            {"role": "user", "content": f"Por favor analiza el sentimiento predominante en el siguiente texto: '{texto}'Pero quiero que me des una explicación más detallada como si fueses un profesional"}
        ],
        #n=1,
        #max_tokens=max_respuesta_length * 2,  # Valor suficientemente grande para evitar frases cortadas. ( las que devuelve la api)
        #temperature=0.8
    )


    respuesta_formateada = respuesta.choices[0].message.content.strip()




    # Diccionario de emociones y palabras clave
    emociones_dict = {
        "gusto": ["gusto", "encanta", "encantan", "me gusta", "es un buen", "hermosa", "hermoso", "satisfacción", "placer", "agradable", "adorar", "encantador", "divertido", "excelente", "divino", "fantástico", "encantador"],
        "amor": ["encanta", "amor", "amo", "me gusta", "enamoramiento", "cariño", "afecto", "ternura", "devoción", "compañerismo", "fascinación", "apego", "pasión", "amistad", "dulzura", "complicidad", "romance", "idilio"],
        "interesante": ["interesante", "fascinante", "atractivo", "intrigante", "curioso", "apasionante", "emocionante", "captivante", "entretenido", "envolvente", "llamativo", "seductor", "sorprendente", "involucrante", "excitante"],
        "enfado": ["frustración", "disgusto", "enfado", "enojado", "molesto", "molestia", "rabia", "furioso", "indignación", "exasperación", "irritación", "hostilidad", "odio", "desprecio", "iracundo", "resentimiento", "acalorado", "violento"],
        "tristeza": ["tristeza", "melancolía", "abatido", "deprimido", "triste", "desánimo", "pesar", "aflicción", "pena", "duelo", "luto", "sufrimiento", "angustia", "nostalgia", "desesperanza", "congoja", "desolación"],
        "felicidad": ["feliz", "alegría", "contento", "entusiasmado", "éxtasis", "júbilo", "regocijo", "diversión", "euforia", "placer", "satisfacción", "festejo", "alegría inmensa", "alboroto", "felicidad radiante", "regocijo desbordante"],
        "sorpresa": ["sorpresa", "asombro", "increíble", "impactante", "tremendo", "estupefacción", "maravilla", "conmoción", "perplejidad", "deslumbrante", "atónito", "desconcertante", "estupefacto", "boquiabierto", "perplejo", "impresionante"],
        "miedo": ["miedo", "aterrorizado", "asustado", "temor", "panico", "terror", "horror", "aprehensión", "espanto", "angustia", "ansiedad", "susto", "preocupación", "nervios", "escalofríos", "inquietud"],
        "desprecio": ["disgusto", "desprecio", "asco", "repulsión", "detesto", "rechazo", "condena", "violación", "aversión", "desagrado", "desdén", "abominación", "odio", "aborrecimiento", "aborrecible", "abyecto", "insultante"],
        "divertido": ["divertido", "divertirnos", "chiste", "risa", "humor", "entretenido", "gracioso", "cómico", "alegría", "regocijo", "reír", "entretenimiento", "risueño", "jocoso", "diversión desenfrenada", "risa contagiosa"],
        "orgullo": ["orgullo", "satisfacción", "elogio", "dignidad", "autoestima", "honor", "autoconfianza", "prestigio", "autoelogio", "triunfo", "respeto", "orgulloso", "satisfecho", "digno", "glorioso", "altivo"],
        "culpa": ["culpa", "remordimiento", "arrepentimiento", "penitencia", "vergüenza", "autoacusación", "autocrítica", "compunción", "pesar", "autoexamen", "autoreproche", "autocondena", "disculpa", "reparación", "arrepentido", "lamentable"],
        "emoción": ["emoción", "emocionado", "sentir", "experiencia", "sensación", "reacción", "respuesta emocional", "impresión", "estímulo", "pasión", "vivencia", "excitación", "involucración", "afecto", "entusiasmo"],
        "confusión": ["confusión", "desconcertado", "perplejo", "incomprensión", "desorientación", "ambigüedad", "desorden", "caos", "incertidumbre", "despiste", "atolondramiento", "caótico", "incompleto", "ininteligible", "desordenado", "mareado"],
        "aburrimiento": ["aburrimiento", "monótono", "tedio", "insípido", "aburrido", "desinterés", "desgana", "apatía", "tedioso", "fastidioso", "monotonía", "indiferencia", "rutina", "repetitivo", "poco interesante"],
        "tranquilidad": ["tranquilidad", "serenidad", "paz", "calma", "relajación", "quietud", "paciencia", "armonía", "equilibrio", "sosegado", "apacible", "sereno", "apaciguador", "reposado", "pausado", "relajado"],
        "indiferencia": ["indiferencia", "apático", "desinterés", "neutral", "me da lo mismo", "me da igual", "desinteresado", "pasividad", "frialdad", "desapego", "igual", "impasible", "neutralidad", "despreocupado", "insensible", "imperturbable", "desconexión"],
        "esperanza": ["esperanza", "optimismo", "esperanzado", "fe", "confianza", "positividad", "anticipación", "motivación", "positivo", "ilusión", "esperar", "optimista", "esperado", "esperanzador", "confiado", "esperanzadora"],
        "inquietud": ["inquietud", "nerviosismo", "ansiedad", "preocupación", "agitación", "tensión", "preocupado", "nervioso", "intriga", "aprensión", "intranquilidad", "desasosiego", "agitado", "angustioso", "turbado", "agitante"],

    }

    # Añadir la detección de emociones utilizando el diccionario
    emociones = {}  # Un diccionario para almacenar las emociones

    # Recorre el diccionario de emociones y palabras clave y aca se hace esto para que si por ejemplo la emocion que devuelve es disgusto no la tome tambien el diccionario como gusto , para que analice la palabra textual y devuelva en 1.0 sola la correcta
    for emocion, palabras_clave in emociones_dict.items():
        for palabra_clave in palabras_clave:
            # Divide el texto en palabras individuales
            palabras_en_texto = respuesta_formateada.split()
            # Comprueba si la palabra clave está en el texto como palabra completa
            if palabra_clave in palabras_en_texto:
                emociones[emocion] = 1.0  # Marca la emoción como 1.0 si la palabra clave se encuentra presente tal cual es

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
imagen = "banner3.jpg"
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
                # Mostrar la respuesta en negrita
                st.markdown(f"**{resultado_analisis}**")
                # Agregar una línea horizontal
                st.write('<hr>', unsafe_allow_html=True)
                # Mostrar el gráfico de barras con emociones
                #st.subheader("Emociones Detectadas:")
                #st.bar_chart(emociones)
                # Crear un gráfico de barras vertical con Matplotlib
                fig, ax = plt.subplots()
                ax.bar(emociones.keys(), emociones.values())
                ax.set_ylabel('Valor')
                ax.set_xlabel('Emoción')
                ax.set_title('Emociones Detectadas')
                plt.xticks(rotation=90)  # Rotar las etiquetas del eje x para que sean legibles
                # Personalizar el tamaño de la fuente
                #ax.tick_params(axis='x', labelrotation=45, labelsize=20)  # Aumentar el tamaño de la fuente en el eje x

                # Mostrar el gráfico en Streamlit
                st.pyplot(fig)
    except Exception as e:
        st.error(f"Acceso Denegado: {e}")

st.divider()

st.write("<h1 style='color: #66b3ff;font-size: 28px;'>Análisis Gráfico:</h1>", unsafe_allow_html=True)

with st.container():
    st.write("En cuanto al gráfico el resultado puede tener diferentes enfoques, ya que el modelo trabaja "
             "bajo probabilidades por lo que un mismo texto puede tener diferentes puntos de vista."
             "Puede buscar variantes con el botón de Analizar Gráfico Nuevamente")

    if st.button("Analizar Gráfico Nuevamente"):
        try:
            # Agregar una línea horizontal
            st.write('<hr>', unsafe_allow_html=True)
            resultado_analisis, emociones = analizar_sentimientos(texto_a_analizar)
            fig, ax = plt.subplots()
            ax.bar(emociones.keys(), emociones.values())
            ax.set_ylabel('Valor')
            ax.set_xlabel('Emoción')
            ax.set_title('Emociones Detectadas')
            plt.xticks(rotation=90)  # Rotar las etiquetas del eje x para que sean legibles
            # Personalizar el tamaño de la fuente
            #ax.tick_params(axis='x', labelrotation=45, labelsize=20)  # Aumentar el tamaño de la fuente en el eje x

            # Mostrar el gráfico en Streamlit
            st.pyplot(fig)
            #grafico anterior el que trae x defecto streamlit
            #st.subheader("Emociones Detectadas:")
            #st.bar_chart(emociones)
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

# Botón para cerrar la sesión
if st.button("Cerrar Sesión"):
    reset_session()


