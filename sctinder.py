import streamlit as st
import pandas as pd
import re
import urllib.parse
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="SC Match", page_icon="🚀")

# --- ESTADO DE AUDIO EN SESSION STATE ---
if 'audio_on' not in st.session_state:
    st.session_state.audio_on = False

# --- BARRA LATERAL: LOGO Y CONFIGURACIÓN ---
# Usamos el link directo del logo que proporcionaste
logo_url = "https://wsrv.nl/?url=https://drive.google.com/uc?id=1bIXfJj65oD7IUVaiKXnJNGrFQLqveILW"
st.sidebar.image(logo_url, use_container_width=True)

st.sidebar.title("Configuración")
audio_toggle = st.sidebar.button("🔊 Activar Música" if not st.session_state.audio_on else "🔇 Mutear Música")

if audio_toggle:
    st.session_state.audio_on = not st.session_state.audio_on
    st.rerun()

# --- MÚSICA DE FONDO (Terran One) ---
def musica_de_fondo():
    video_id = "qtg7rd9yUWI"
    if st.session_state.audio_on:
        components.html(
            f"""
            <div id="player"></div>
            <script>
              var tag = document.createElement('script');
              tag.src = "https://www.youtube.com/iframe_api";
              var firstScriptTag = document.getElementsByTagName('script')[0];
              firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

              var player;
              function onYouTubeIframeAPIReady() {{
                player = new YT.Player('player', {{
                  height: '0', width: '0', videoId: '{video_id}',
                  playerVars: {{ 'autoplay': 1, 'loop': 1, 'playlist': '{video_id}', 'controls': 0 }},
                  events: {{
                    'onReady': function(event) {{ event.target.playVideo(); }},
                    'onStateChange': function(event) {{ if (event.data === YT.PlayerState.ENDED) {{ player.playVideo(); }} }}
                  }}
                }});
              }}
            </script>
            <style> iframe {{ display: none; }} </style>
            """,
            height=0,
        )

musica_de_fondo()

# --- LÓGICA DE ANIMACIÓN (ZERGLINGS) ---
def lluvia_zerglings():
    zerg_url = "https://www.pngkey.com/png/full/421-4219746_lien-direct-starcraft-2-carbot-zergling.png"
    zerglings_html = ""
    for i in range(15):
        left = random.randint(0, 90)
        duration = random.uniform(2, 4)
        delay = random.uniform(0, 2)
        size = random.randint(50, 100)
        zerglings_html += f'<img src="{zerg_url}" class="zerg" style="left:{left}%; animation-duration:{duration}s; animation-delay:{delay}s; width:{size}px;">'

    components.html(
        f"""
        <style>
            .zerg-container {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999; overflow: hidden; }}
            .zerg {{ position: absolute; bottom: -150px; animation: fly linear forwards; }}
            @keyframes fly {{ 0% {{ transform: translateY(0) rotate(0deg); opacity: 1; }} 100% {{ transform: translateY(-120vh) rotate(360deg); opacity: 0; }} }}
        </style>
        <div class="zerg-container">{zerglings_html}</div>
        """,
        height=0,
    )

# --- LÓGICA DE AUDIO (EFECTOS) ---
def reproducir_sonido():
    if st.session_state.audio_on:
        audio_url = "https://www.myinstants.com/media/sounds/starcraft-confirm.mp3"
        components.html(f'<audio autoplay><source src="{audio_url}" type="audio/mp3"></audio>', height=0)

# --- CONFIGURACIÓN DE DATOS ---
sheet_id = "11qlEV5hQakPVczBRWWbiT9TF-m1FIrbK82gl7-yV8to"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

def get_image_url(drive_url):
    try:
        match = re.search(r'(?:id=|/d/|file/d/)([-\w]{25,})', str(drive_url))
        if match:
            doc_id = match.group(1)
            return f"https://wsrv.nl/?url=https://drive.google.com/uc?id={doc_id}"
    except: return None
    return None

try:
    df = pd.read_csv(url).dropna(subset=['Nombre', 'Sube tu fotito'])
    mi_nombre = st.sidebar.selectbox("¿Quién eres?", df['Nombre'].unique())
    mi_faccion = df[df['Nombre'] == mi_nombre]['Facción'].values[0]
    objetivo = "Zerg" if mi_faccion == "Terran" else "Terran"
    candidatos = df[(df['Facción'] == objetivo) & (df['Nombre'] != mi_nombre)].to_dict('records')

    if 'idx' not in st.session_state: st.session_state.idx = 0
    st.title(f"Buscando pareja {objetivo} 🚀")

    if st.session_state.idx < len(candidatos):
        persona = candidatos[st.session_state.idx]
        with st.container(border=True):
            foto_url = get_image_url(persona['Sube tu fotito'])
            if foto_url: st.image(foto_url, use_container_width=True)
            st.subheader(persona['Nombre'])
            st.write(f"Facción: **{persona['Facción']}**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("❌ Pasar", key="p_v6", use_container_width=True):
                    reproducir_sonido(); st.session_state.idx += 1; st.rerun()
            with col2:
                if st.button("❤️ Match", key="m_v6", use_container_width=True):
                    reproducir_sonido(); st.session_state.match_detectado = True; lluvia_zerglings()

            if st.session_state.get('match_detectado'):
                st.success(f"¡Match con {persona['Nombre']}!")
                try:
                    telefono = str(persona['WhatsApp']).replace(" ", "").replace("+", "")
                    mensaje = f"Hola {persona['Nombre']}, ¡hicimos match en SC Tinder! ¿Quieres compartir caja conmigo? uwu"
                    mensaje_encoded = urllib.parse.quote(mensaje)
                    wa_link = f"https://wa.me/{telefono}?text={mensaje_encoded}"
                    if st.link_button("💬 WhatsApp", wa_link, use_container_width=True, type="primary"): reproducir_sonido()
                except: st.warning("⚠️ Revisa la columna 'WhatsApp'.")
                if st.button("Siguiente candidato", key="s_v6", use_container_width=True):
                    reproducir_sonido(); st.session_state.match_detectado = False; st.session_state.idx += 1; st.rerun()
    else:
        st.info("No hay más candidatos.")
        if st.button("Reiniciar lista"): st.session_state.idx = 0; st.rerun()
except Exception as e: 
    # Muestra el error real para poder debuguear si algo falla con el Excel
    st.error(f"Error detectado: {e}")