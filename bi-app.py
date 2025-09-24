import streamlit as st
import pandas as pd
import ast
import math

# Configuración de la página para que ocupe todo el ancho
st.set_page_config(layout="wide")

# Cargar dataset
df = pd.read_csv("https://github.com/melody-10/Proyecto_Hoteles_California/blob/main/final_database.csv?raw=true")

# --- FUNCIÓN PARA CREAR ESTRELLAS ---
def generate_stars(score):
    try:
        score = float(score)
        if 0 <= score <= 5:
            full_stars = math.floor(score)
            half_star = "★" if score - full_stars >= 0.5 else ""
            empty_stars = 5 - full_stars - len(half_star)
            return f"<span style='color: #FFD700;'>{'★' * full_stars}{half_star}{'☆' * empty_stars}</span> ({score})"
        else:
            return "N/A"
    except (ValueError, TypeError):
        return "N/A"
# ------------------------------------

# Convertir columna ratings a diccionario
def parse_ratings(val):
    try:
        return ast.literal_eval(val) if isinstance(val, str) else {}
    except (ValueError, SyntaxError):
        return {}

df["ratings_parsed"] = df["ratings"].apply(parse_ratings)
df['text'] = df['text'].astype(str)

# --- CÁLCULO DE PROMEDIOS POR HOTEL ---
df_for_avg = df[['name', 'ratings_parsed']].copy()
ratings_df = pd.json_normalize(df_for_avg['ratings_parsed'])
full_ratings_df = pd.concat([df_for_avg['name'], ratings_df], axis=1)
rating_columns = ratings_df.columns
for col in rating_columns:
    full_ratings_df[col] = pd.to_numeric(full_ratings_df[col], errors='coerce')
average_ratings_per_hotel = full_ratings_df.groupby('name')[rating_columns].mean().round(1)
# ------------------------------------

# Emojis para cada atributo
emoji_map = {"service": "🛎️", "cleanliness": "🧼", "overall": "⭐","value": "💰", "location": "📍", "sleep_quality": "💤", "rooms": "🚪"}

# Estilos y diseño
st.markdown("""<style>
    .stApp { background: #f4f6f9; font-family: 'Segoe UI', sans-serif; }
    .content-box { background: white; padding: 18px; border-radius: 10px; box-shadow: 0px 2px 8px rgba(0,0,0,0.07); margin-bottom: 12px; height: 100%; }
    .hotel-title { font-size: 22px; font-weight: bold; color: #2C3E50; text-align: center; }
    .review-text { font-size: 15px; color: #444; line-height: 1.5; }
    .ratings-title { font-weight: bold; font-size: 16px; margin-bottom: 10px; color: #2C3E50; }
    .rating-line { margin: 8px 0; font-size: 15px; color: #333; display: flex; align-items: center; justify-content: space-between; }
    </style>""", unsafe_allow_html=True)

# Título principal de la aplicación
st.title("🏨 Explorador de Reviews por Tópico y Hotel")

# Filtros
topics = df['topic_label'].unique().tolist()
selected_topic = st.selectbox("📌 Selecciona un tópico", topics)
hotel_options = ['Todos'] + sorted(df['name'].unique().tolist())
selected_hotel = st.selectbox("🏩 Selecciona un hotel", hotel_options)
n_reviews = st.slider("📊 Número máximo de reviews a mostrar", 1, 20, 5)

# Filtrado de datos
filtered_df = df[df['topic_label'] == selected_topic]
if selected_hotel != 'Todos':
    filtered_df = filtered_df[filtered_df['name'] == selected_hotel]
else:
    filtered_df = filtered_df.drop_duplicates(subset=['name'])
filtered_df = filtered_df.head(n_reviews)

# Mostrar resultados
for idx, row in filtered_df.iterrows():
    st.markdown(f"<div class='content-box hotel-title'>🏨 {row['name']}</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])

    # --- Columna 1: Review ---
    with col1:
        review_html = f"""<div class="content-box"><p class="review-text">{row['text']}</p></div>"""
        st.markdown(review_html, unsafe_allow_html=True)

    # --- Columna 2: Ratings con Estrellas ---
    with col2:
        ratings_dict = row.get("ratings_parsed", {}).copy()
        ratings_html = '<div class="content-box">'
        ratings_html += '<p class="ratings-title">Ratings de esta Review:</p>'
        
        if ratings_dict:
            overall_value = ratings_dict.pop('overall', None)
            if overall_value is not None:
                emoji = emoji_map.get('overall', "⭐")
                stars = generate_stars(overall_value)
                ratings_html += f'<div class="rating-line"><span>{emoji} Overall</span> <span>{stars}</span></div>'
            
            for key, value in sorted(ratings_dict.items()):
                # --- LÍNEA CORREGIDA AQUÍ ---
                emoji = emoji_map.get(key, "🔹")
                stars = generate_stars(value)
                ratings_html += f'<div class="rating-line"><span>{emoji} {key.capitalize()}</span> <span>{stars}</span></div>'
        else:
            ratings_html += '<p class="rating-line">No hay ratings disponibles.</p>'
        
        ratings_html += '</div>'
        st.markdown(ratings_html,
