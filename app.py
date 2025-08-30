# -----------------------------------------------------------------
# CÓDIGO PARA UNA PÁGINA WEB DE CHATBOT EDUCATIVO CON STREAMLIT
# -----------------------------------------------------------------

import streamlit as st
import google.generativeai as genai
import time

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
# Esto define el título, el ícono y el layout de tu página web.
# Es el primer toque para una buena UI/UX.
st.set_page_config(
    page_title="Asistente de IA Ética",
    page_icon="💡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. LA BARRA LATERAL (SIDEBAR) ---
# Aquí ponemos información importante sin saturar la pantalla principal.
with st.sidebar:
    st.title("💡 Asistente de IA Ética")
    st.markdown("---")
    st.markdown(
        "**¡Bienvenido/a!** Soy un asistente de IA diseñado para ayudarte a explorar el mundo de la inteligencia artificial de forma segura y responsable."
    )
    st.markdown("---")
    st.subheader("Reglas de Interacción:")
    st.markdown(
        """
        - ✅ **Pregunta sobre IA:** Ética, sesgos, cómo funciono, etc.
        - 🧐 **Sé crítico:** Verifica siempre la información importante.
        - 🔒 **Cuida tu privacidad:** No compartas datos personales.
        - ✍️ **Usa como herramienta:** Pídeme ideas, no que haga tu tarea por ti.
        """
    )
    st.markdown("---")
    st.info("Este es un espacio de aprendizaje seguro. ¡Explora con curiosidad!")

# --- 3. TÍTULO PRINCIPAL DEL CHAT ---
st.title("Chat con tu Asistente de IA Ética")
st.markdown("Escribe tu pregunta abajo para comenzar la conversación.")
st.markdown("---")

# --- 4. CONFIGURACIÓN DEL API KEY DE GOOGLE ---
# El código intenta obtener la API Key de los "Secrets" de Streamlit para mayor seguridad.
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except (KeyError, TypeError):
    # Si no la encuentra, muestra un error claro en la página principal.
    st.error("⚠️ No se ha configurado la API Key de Google. El administrador del sitio debe añadirla en los 'Secrets' de Streamlit.")
    st.stop()

# --- 5. EL CEREBRO DEL CHATBOT (PROMPT DEL SISTEMA) ---
# Aquí pegas las instrucciones completas que definiste en la Fase 1.
system_prompt = 
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

# --- 6. INICIALIZACIÓN DEL MODELO Y EL CHAT ---
# Creamos el modelo con las instrucciones y preparamos la memoria del chat.
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=system_prompt
)
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- 7. LÓGICA DE LA INTERFAZ DE CHAT ---
# Muestra los mensajes anteriores
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Mensaje de bienvenida del asistente si es la primera vez
if len(st.session_state.chat.history) == 0:
    st.chat_message("assistant").markdown("¡Hola! Soy tu Asistente de IA Ética. ¿Qué te gustaría explorar primero sobre la inteligencia artificial?")

# Input del usuario
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    st.chat_message("user").markdown(prompt)
    response = st.session_state.chat.send_message(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simula el efecto de "escribiendo" para una mejor UX
        for chunk in response.text:
            full_response += chunk
            time.sleep(0.01) # Ajusta este valor para controlar la velocidad
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
