import streamlit as st
import pandas as pd
import ast

# Cargar dataset
df = pd.read_csv("https://github.com/melody-10/Proyecto_Hoteles_California/blob/main/final_database.csv?raw=true")

# Convertir columna ratings a diccionario
def parse_ratings(val):
    try:
        return ast.literal_eval(val) if isinstance(val, str) else {}
    except (ValueError, SyntaxError):
        return {}

df["ratings_parsed"] = df["ratings"].apply(parse_ratings)
# Asegurar que el texto sea siempre un string para evitar errores
df['text'] = df['text'].astype(str)

# Emojis para cada atributo
emoji_map = {"service": "🛎️", 
             "cleanliness": "🧼", 
             "overall": "⭐",
             "value": "💰", 
             "location": "📍", 
             "sleep_quality": "💤", 
             "rooms": "🚪"}

# Estilos y diseño base
st.markdown("""
    <style>
    /* Fondo general */
        .stApp { background: #f4f6f9; font-family: 'Segoe UI', sans-serif; }
    /* Caja título hotel */
        .content-box { background: white; padding: 18px; border-radius: 10px; box-shadow: 0px 2px 8px rgba(0,0,0,0.07); margin-bottom: 12px; height: 100%; }
    /* Título hotel */  
        .hotel-title { font-size: 22px; font-weight: bold; color: #2C3E50; text-align: center; }
    /* Review */  
        .review-text { font-size: 15px; color: #444; line-height: 1.5; }
    /* Título 'Ratings' */  
        .ratings-title { font-weight: bold; font-size: 16px; margin-bottom: 10px; color: #2C3E50; }
    </style>
""", unsafe_allow_html=True)

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

# --- Mostrar resultados ---
for idx, row in filtered_df.iterrows():
    ratings_dict = row.get("ratings_parsed", {}).copy() if isinstance(row.get("ratings_parsed"), dict) else {}

    # El div "card" es nuestro contenedor principal, no necesitamos st.container()
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.markdown(f"<div class='content-box hotel-title'>🏨 {row['name']}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    # --- Columna 1: Review ---
    with col1:
        review_html = f"""
        <div class="content-box">
            <p class="review-text">{row['text']}</p>
        </div>
        """
        st.markdown(review_html, unsafe_allow_html=True)

    # --- Columna 2: Ratings ---
    with col2:
        ratings_html = '<div class="content-box">'
        ratings_html += '<p class="ratings-title">Ratings:</p>'
        
        if ratings_dict:
            overall_value = ratings_dict.pop('overall', None)
            if overall_value is not None:
                emoji = emoji_map.get('overall', "⭐")
                ratings_html += f'<p class="rating-line">{emoji} Overall: {overall_value}/5</p>'
            
            for key, value in sorted(ratings_dict.items()):
                emoji = emoji_map.get(key, "🔹")
                ratings_html += f'<p class="rating-line">{emoji} {key.capitalize()}: {value}/5</p>'
        else:
            ratings_html += '<p class="rating-line">No hay ratings disponibles.</p>'
        
        ratings_html += '</div>'
        st.markdown(ratings_html, unsafe_allow_html=True)

    # Cierre del div "card"
    st.markdown('</div>', unsafe_allow_html=True)
