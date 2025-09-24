import streamlit as st
import pandas as pd
import ast

# Cargar dataset
df = pd.read_csv("https://github.com/melody-10/Proyecto_Hoteles_California/blob/main/final_database.csv?raw=true")

# Convertir columna ratings a diccionario
def parse_ratings(val):
    try:
        return ast.literal_eval(val) if isinstance(val, str) else val
    except:
        return {}

df["ratings_parsed"] = df["ratings"].apply(parse_ratings)

# Emojis para cada atributo
emoji_map = {
    "service": "🛎️",
    "cleanliness": "🧼",
    "overall": "⭐",
    "value": "💰",
    "location": "📍",
    "sleep_quality": "😴",
    "rooms": "🚪"
}

# Estilos
st.markdown("""
    <style>
        .stApp {
            background: #f4f6f9;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Tarjetas generales */
        .card {
            background: white;
            padding: 18px;
            margin: 12px 0;
            border-radius: 12px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
        }

        /* Título del hotel */
        .hotel-title {
            font-size: 22px;
            font-weight: bold;
            color: #2C3E50;
            border-left: 6px solid #3498db;
            padding-left: 12px;
            margin-bottom: 0;
        }

        /* Texto de review */
        .review-text {
            font-size: 15px;
            color: #444;
            line-height: 1.5;
        }

        /* Título de Ratings */
        .ratings-title {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 8px;
        }

        /* Cada línea de rating */
        .rating-line {
            margin: 4px 0;
            font-size: 15px;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# Título global
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

    # Título en su tarjeta
    st.markdown(f"""
        <div class="card">
            <p class="hotel-title">🏨 {row['name']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Texto de review en otra tarjeta
    st.markdown(f"""
        <div class="card">
            <p class="review-text">{row['text']}</p>
        </div>
    """, unsafe_allow_html=True)

    # Ratings en su propia tarjeta
    st.markdown("""
        <div class="card">
            <p class="ratings-title">Ratings:</p>
    """, unsafe_allow_html=True)

    for key, value in ratings_dict.items():
        emoji = emoji_map.get(key, "🔹")
        st.markdown(f"<p class='rating-line'>{emoji} {key.capitalize()}: {value}/5</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
