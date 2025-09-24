import streamlit as st
import pandas as pd

# Cargar dataset
df = pd.read_csv("https://github.com/melody-10/Proyecto_Hoteles_California/blob/main/final_database.csv?raw=true")

# Estilos globales con Markdown y CSS
st.markdown("""
    <style>
        /* Fondo general */
        .stApp {
            background: linear-gradient(135deg, #e8e5e3 0%, #d3dfe0 100%);
            font-family: 'Segoe UI', sans-serif;
        }

        /* Títulos */
        h1, h2, h3 {
            color: #2C3E50;
        }

        /* Subtítulos */
        .stMarkdown h2 {
            border-left: 5px solid #3498db;
            padding-left: 10px;
        }

        /* Tarjetas para cada review */
        .review-card {
            background: white;
            padding: 15px;
            margin: 12px 0;
            border-radius: 12px;
            box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
        }

        /* Rating destacado */
        .rating {
            font-weight: bold;
            color: #e67e22;
        }

        /* Separadores */
        hr {
            border: 1px solid #ddd;
            margin: 20px 0;
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

# Mostrar resultados con tarjetas
for idx, row in filtered_df.iterrows():
    st.markdown(f"""
        <div class="review-card">
            <h3>🏨 {row['name']}</h3>
            <p class="rating">⭐ {row['ratings']}/5</p>
            <p>{row['text']}</p>
        </div>
    """, unsafe_allow_html=True)
