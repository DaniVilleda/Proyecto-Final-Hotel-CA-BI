import streamlit as st
import pandas as pd
import ast  # para convertir strings tipo diccionario a dict real

# Cargar dataset
df = pd.read_csv("https://github.com/melody-10/Proyecto_Hoteles_California/blob/main/final_database.csv?raw=true")

# Convertir la columna 'ratings' (que parece string con dict) a dict
def parse_ratings(val):
    try:
        return ast.literal_eval(val) if isinstance(val, str) else val
    except:
        return {}

df["ratings_parsed"] = df["ratings"].apply(parse_ratings)

# Diccionario de emojis por atributo
emoji_map = {
    "service": "🛎️",
    "cleanliness": "🧼",
    "overall": "⭐",
    "value": "💰",
    "location": "📍",
    "sleep_quality": "😴",
    "rooms": "🚪"
}

# Estilos globales
st.markdown("""
    <style>
        /* Fondo general */
        .stApp {
            background: #f9f9f9;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Título principal */
        h1 {
            color: #2C3E50;
            text-align: center;
            margin-bottom: 30px;
        }

        /* Subtítulos (hoteles) */
        h3 {
            color: #2C3E50;
            font-size: 20px;
            margin-bottom: 5px;
            border-left: 6px solid #3498db;
            padding-left: 10px;
        }

        /* Tarjetas */
        .review-card {
            background: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 12px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
            transition: transform 0.2s ease-in-out;
        }
        .review-card:hover {
            transform: translateY(-3px);
            box-shadow: 0px 6px 14px rgba(0,0,0,0.12);
        }

        /* Texto de review */
        .review-text {
            font-size: 15px;
            color: #555;
            margin-top: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("🏨 Explorador de Reviews por Tópico y Hotel")

# Filtros
topics = df['topic_label'].unique().tolist()
selected_topic = st.selectbox("📌 Selecciona un tópico", topics)

hotel_options = ['Todos'] + sorted(df['name'].unique().tolist())
selected_hotel = st.selectbox("🏩 Selecciona un hotel", hotel_options)

n_reviews = st.slider("📊 Número máximo de reviews a mostrar", min_value=1, max_value=20, value=5)

# Filtrado
filtered_df = df[df['topic_label'] == selected_topic]

if selected_hotel != 'Todos':
    filtered_df = filtered_df[filtered_df['name'] == selected_hotel]
else:
    filtered_df = filtered_df.groupby('name').head(1).reset_index(drop=True)

filtered_df = filtered_df.head(n_reviews)

# Mostrar resultados
for idx, row in filtered_df.iterrows():
    ratings_dict = row["ratings_parsed"]

    st.markdown(f"<div class='review-card'><h3>🏨 {row['name']}</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])  # review más ancho, ratings más angosto

    with col1:
        st.markdown(f"<p class='review-text'>{row['text']}</p>", unsafe_allow_html=True)

    with col2:
        st.markdown("**Ratings:**")
        for key, value in ratings_dict.items():
            emoji = emoji_map.get(key, "🔹")
            st.write(f"{emoji} {key.capitalize()}: {value}/5")

    st.markdown("</div>", unsafe_allow_html=True)
