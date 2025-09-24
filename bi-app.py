import streamlit as st
import pandas as pd
import ast
import plotly.express as px
import plotly.graph_objects as go

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

# --- CÁLCULO DE PROMEDIOS GENERALES ---
# Convertimos la columna de diccionarios en un DataFrame limpio
ratings_df = pd.json_normalize(df['ratings_parsed'])

# Nos aseguramos de que todas las columnas de ratings sean numéricas
for col in ratings_df.columns:
    ratings_df[col] = pd.to_numeric(ratings_df[col], errors='coerce')

# Calculamos el promedio de cada columna (atributo)
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

    # --- Columna 2: Gráfico de Barras Comparativo ---
    with col2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        
        original_ratings_dict = row.get("ratings_parsed", {}).copy()
        
        if original_ratings_dict:
            # Convertimos los ratings del hotel actual a un DataFrame
            df_hotel = pd.DataFrame(list(original_ratings_dict.items()), columns=['Atributo', 'Puntaje Hotel'])
            df_hotel['Puntaje Hotel'] = pd.to_numeric(df_hotel['Puntaje Hotel'], errors='coerce')
            df_hotel.dropna(inplace=True)

            if not df_hotel.empty:
                # Preparamos los datos del promedio para unirlos
                df_avg = average_ratings.reindex(df_hotel['Atributo']).reset_index()
                df_avg.columns = ['Atributo', 'Promedio General']
                
                # Unimos los dos DataFrames
                df_comparison = pd.merge(df_hotel, df_avg, on='Atributo')
                
                # Creamos la figura
                fig = go.Figure()

                # 1. Barra del Hotel Actual
                fig.add_trace(go.Bar(
                    x=df_comparison['Atributo'],
                    y=df_comparison['Puntaje Hotel'],
                    name='Hotel Actual',
                    marker_color='#007bff',
                    text=df_comparison['Puntaje Hotel'],
                    textposition='auto'
                ))

                # 2. Barra del Promedio General
                fig.add_trace(go.Bar(
                    x=df_comparison['Atributo'],
                    y=df_comparison['Promedio General'],
                    name='Promedio General',
                    marker_color='#ffc107',
                    text=df_comparison['Promedio General'],
                    textposition='auto'
                ))

                # Configuramos el diseño como 'group' (lado a lado)
                fig.update_layout(
                    barmode='group',
                    xaxis_title="",
                    yaxis_title="Puntaje",
                    yaxis=dict(range=[0, 5.5]),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(l=20, r=20, t=30, b=20),
                    height=350,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#2C3E50")
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No hay ratings numéricos para graficar.")
        else:
            st.write("No hay ratings disponibles.")
            
        st.markdown('</div>', unsafe_allow_html=True)
