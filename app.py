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
emoji_map = {"service": "🛎️",
            "cleanliness": "🧼",
            "overall": "⭐",
            "value": "💰",
            "location": "📍",
            "sleep_quality": "💤",
            "rooms": "🚪"}

# Estilo y diseño
st.markdown("""
<style>
        .stApp {
            background: #e61595;
            font-family: 'Segoe UI', sans-serif;
        }
        .card {
            background: #eaf0f7;
            padding: 22px;
            margin: 16px 0;
            border-radius: 14px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        }
        .content-box {
            background: white;
            padding: 18px;
            border-radius: 10px;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.07);
            margin-bottom: 12px;
            height: 100%;
        }
        .hotel-title {
            font-size: 22px;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
        }
        .review-text {
            font-size: 15px;
            color: #444;
            line-height: 1.5;
        }
        .ratings-title {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 10px;
            color: #2C3E50;
        }
        .rating-line {
            margin: 5px 0;
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
    filtered_df = filtered_df.drop_duplicates(subset=['name'])
filtered_df = filtered_df.head(n_reviews)


# Mostrar resultados
for idx, row in filtered_df.iterrows():
    # Creamos una copia para poder modificarla (con .pop()) sin afectar el dataframe original
    ratings_dict = row["ratings_parsed"].copy() if isinstance(row["ratings_parsed"], dict) else {}

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        # Título del hotel en su propio cuadro
        st.markdown(f"<div class='content-box hotel-title'>🏨 {row['name']}</div>", unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        # Columna 1: Review
        with col1:
            # Construimos todo el HTML en un solo string
            review_html = f"""
            <div class="content-box">
                <p class="review-text">{row['text']}</p>
            </div>
            """
            st.markdown(review_html, unsafe_allow_html=True)

        # Columna 2: Ratings (CON LA LÓGICA DE ORDENAMIENTO)
        with col2:
            # Empezamos a construir el string de HTML para los ratings
            ratings_html = '<div class="content-box">'
            ratings_html += '<p class="ratings-title">Ratings:</p>'
            
            if ratings_dict:
                # 1. Sacamos 'overall' para tratarlo primero. Si no existe, devuelve None.
                overall_value = ratings_dict.pop('overall', None)
                
                # 2. Si encontramos un valor para 'overall', lo añadimos al HTML.
                if overall_value is not None:
                    emoji = emoji_map.get('overall', "⭐")
                    ratings_html += f'<p class="rating-line">{emoji} Overall: {overall_value}/5</p>'
                
                # 3. Ahora, iteramos sobre el RESTO de los items en el diccionario.
                for key, value in ratings_dict.items():
                    emoji = emoji_map.get(key, "🔹")
                    ratings_html += f'<p class="rating-line">{emoji} {key.capitalize()}: {value}/5</p>'
            else:
                ratings_html += '<p class="rating-line">No hay ratings disponibles.</p>'
            
            # Cerramos el div
            ratings_html += '</div>'
            
            # Renderizamos todo el bloque de HTML de una vez
            st.markdown(ratings_html, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
