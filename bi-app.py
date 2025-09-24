import streamlit as st
import pandas as pd
import ast

# Configuración de la página para que ocupe todo el ancho
st.set_page_config(layout="wide")

# Cargar dataset
df = pd.read_csv("https://github.com/melody-10/Proyecto_Hoteles_California/blob/main/final_database.csv?raw=true")

# Convertir columna ratings a diccionario de forma segura
def parse_ratings(val):
    try:
        return ast.literal_eval(val) if isinstance(val, str) else {}
    except (ValueError, SyntaxError):
        return {}

df["ratings_parsed"] = df["ratings"].apply(parse_ratings)
df['text'] = df['text'].astype(str)

# --- CÁLCULO DE PROMEDIOS GENERALES (Lo seguimos necesitando) ---
ratings_df = pd.json_normalize(df['ratings_parsed'])
for col in ratings_df.columns:
    ratings_df[col] = pd.to_numeric(ratings_df[col], errors='coerce')
average_ratings = ratings_df.mean().round(1)
# ------------------------------------

# Estilos y diseño
st.markdown("""<style>
    .stApp { background: #f4f6f9; font-family: 'Segoe UI', sans-serif; }
    .content-box { background: white; padding: 18px; border-radius: 10px; box-shadow: 0px 2px 8px rgba(0,0,0,0.07); margin-bottom: 12px; height: 100%; }
    .hotel-title { font-size: 22px; font-weight: bold; color: #2C3E50; text-align: center; }
    .review-text { font-size: 15px; color: #444; line-height: 1.5; }
    </style>""", unsafe_allow_html=True)

# Título principal de la aplicación
st.title("🏨 Explorador de Reviews por Tópico y Hotel")

# Filtros y widgets respectivos
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

    # Creamos dos columnas: una para la review y otra para el gráfico
    col1, col2 = st.columns([1, 1])

    # --- Columna 1: Review ---
    with col1:
        review_html = f"""<div class="content-box"><p class="review-text">{row['text']}</p></div>"""
        st.markdown(review_html, unsafe_allow_html=True)

    # --- Columna 2: Gráfico Comparativo con st.bar_chart ---
    with col2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        
        ratings_dict = row.get("ratings_parsed", {})
        
        if ratings_dict:
            # Preparamos los datos del hotel actual
            hotel_scores = {}
            for key, value in ratings_dict.items():
                try:
                    hotel_scores[key] = float(value)
                except (ValueError, TypeError):
                    continue
            
            if hotel_scores:
                # Creamos un DataFrame para la comparación
                df_comparison = pd.DataFrame({
                    'Hotel Actual': pd.Series(hotel_scores),
                    'Promedio General': average_ratings
                })
                # Nos aseguramos de que solo se comparen los atributos presentes en esta review
                df_comparison.dropna(inplace=True) 

                st.write("#### Comparativa de Ratings")
                # Usamos el comando integrado de Streamlit
                st.bar_chart(df_comparison, height=300)
            else:
                st.write("No hay ratings numéricos para graficar.")
        else:
            st.write("No hay ratings disponibles.")
            
        st.markdown('</div>', unsafe_allow_html=True)
