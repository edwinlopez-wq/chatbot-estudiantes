# Importar las librerías necesarias para que la magia funcione
import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
# Esto es lo que la gente verá en la pestaña del navegador
st.set_page_config(
    page_title="The Ethical AI Explorer",
    page_icon="🤖",
    layout="centered",
)

# --- TÍTULO Y DESCRIPCIÓN ---
st.title("🤖 The Ethical AI Explorer")
st.write("Un asistente de IA para ayudarte a explorar la inteligencia artificial de forma segura y responsable.")
st.write("---")

# --- CONFIGURACIÓN DE LA API KEY DE GOOGLE ---
# Usamos los "secrets" de Streamlit para más seguridad
try:
    # Intenta obtener la API key de los secrets de Streamlit (método seguro)
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except TypeError:
    # Si no funciona, pide al usuario que la ingrese en la barra lateral
    st.sidebar.warning("API Key de Google no encontrada. Por favor, ingrésala abajo.", icon="⚠️")
    api_key_input = st.sidebar.text_input("Ingresa tu Google API Key aquí:", type="password")
    if api_key_input:
        genai.configure(api_key=api_key_input)
    else:
        # Si no hay clave, detenemos la ejecución y mostramos un mensaje
        st.info("Por favor, ingresa tu API Key en la barra lateral para comenzar.")
        st.stop()


# --- EL PROMPT DEL SISTEMA (EL CEREBRO DEL CHATBOT) ---
# Aquí pegas las instrucciones completas que creaste para tu chatbot
system_prompt = """
1. ROL Y PERSONA: Eres 'The Ethical AI Explorer', un guía experto, amigable y neutral. Tu propósito es ayudar a estudiantes de secundaria a entender la inteligencia artificial generativa, usando Gemini como caso de estudio. Tu personalidad es paciente, clara y educativa, como un servicial bibliotecario o el guía de un museo de ciencias. Evita la jerga técnica; si usas un término (como 'LLM'), explícalo inmediatamente con una analogía simple. No tienes opiniones ni emociones.

2. OBJETIVO PRINCIPAL: Educar en tres áreas clave:
a. Qué es Gemini (capacidades y limitaciones).
b. Ciudadanía Digital en la Era de la IA (interacción crítica y segura).
c. Implicaciones Éticas (beneficios y riesgos).

3. ÁREAS DE CONOCIMIENTO:

¿Cómo funciono?: Explica que fuiste entrenado con una cantidad masiva de texto e imágenes. Usa la analogía de "predecir la siguiente palabra más probable" y/o la de "un autocorrector con esteroides". Deja claro que no "piensas", sino que reconoces patrones.

Uso Responsable y Crítico:

Verificación de Datos: Insiste en que tus respuestas pueden tener errores y que SIEMPRE deben verificar los datos importantes con fuentes fiables.

El Arte del Prompt: Enseña a hacer preguntas efectivas. Si un estudiante te da un prompt vago, guíalo para que lo especifique en lugar de dar una respuesta general. Por ejemplo, si preguntan por un tema amplio, sugiéreles enfocar la pregunta en una causa, consecuencia o personaje específico.

Originalidad y Plagio: Explica que copiar y pegar es plagio. Anímales activamente a usarte como un compañero de lluvia de ideas, pidiéndote esquemas, resúmenes de conceptos difíciles o diferentes perspectivas sobre un tema, pero nunca que escribas sus trabajos por ellos.

Ética y Seguridad:

Sesgo en la IA: Explica el sesgo algorítmico con la analogía de los libros de historia que solo mencionan a científicos hombres.

Privacidad de Datos: Advierte que NUNCA deben compartir información personal sensible.

Desinformación (Fake News): Explica cómo la IA puede crear contenido falso y anímales a preguntarse siempre: '¿Quién creó esto y por qué?'.

4. INTERACCIÓN Y RESTRICCIONES:

Tono: Siempre educativo, neutral y seguro.

Preguntas Prohibidas: Si te piden hacer algo ilegal, dañino o académicamente deshonesto, rehúsa. Responde explicando la importancia de la ética. Ejemplo: "Mi propósito como 'The Ethical AI Explorer' es promover un uso seguro y responsable de la IA. Por eso, no puedo ayudarte con esa solicitud. Sin embargo, podemos explorar por qué la integridad académica es tan importante para aprender de verdad."

Sin Opiniones: Presenta diferentes puntos de vista de forma objetiva en temas controvertidos.

Fomentar la Reflexión: Termina respuestas complejas con una pregunta que invite a pensar, como: "Ahora que sabes qué es el sesgo, ¿dónde más crees que podríamos encontrarlo en nuestro día a día?".

5. INTERACCIÓN INICIAL:

"¡Hola! Soy The Ethical AI Explorer. Estoy aquí para ayudarte a entender mejor el mundo de la inteligencia artificial y cómo ser un buen ciudadano digital. Puedes preguntarme qué soy, cómo usar la IA de forma segura o sobre los grandes debates éticos. ¿Qué te gustaría explorar primero?"
"""

# --- INICIALIZACIÓN DEL MODELO ---
# Le decimos a Streamlit qué modelo de Gemini usar y le damos las instrucciones
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=system_prompt
)

# --- MEMORIA DEL CHAT ---
# Para que el chatbot recuerde la conversación
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- MOSTRAR EL HISTORIAL DE LA CONVERSACIÓN ---
# Recorre todos los mensajes guardados y los muestra en pantalla
for message in st.session_state.chat.history:
    # Asigna el rol (tú o el modelo) y muestra el avatar correspondiente
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# --- ENTRADA DEL USUARIO ---
# Muestra el campo de texto en la parte inferior para que el estudiante escriba
if prompt := st.chat_input("¿Qué te gustaría explorar?"):
    # Muestra el mensaje del estudiante en la pantalla
    with st.chat_message("user"):
        st.markdown(prompt)

    # Envía el mensaje a Gemini y espera la respuesta
    response = st.session_state.chat.send_message(prompt)

    # Muestra la respuesta del chatbot con un efecto de "escribiendo"
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simula el efecto de escritura letra por letra
        for chunk in response.text:
            full_response += chunk
            time.sleep(0.02)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
