import streamlit as st
import pandas as pd
import ast
import plotly.express as px
import plotly.graph_objects as go # <--- ESTA ES LA LÍNEA QUE FALTABA

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


# Emojis para cada atributo
emoji_map = {"service": "🛎️", "cleanliness": "🧼", "overall": "⭐","value": "💰", "location": "📍", "sleep_quality": "💤", "rooms": "🚪"}

# Estilos y diseño
st.markdown("""<style>
    .stApp { background: #f4f6f9; font-family: 'Segoe UI', sans-serif; }
    .content-box { background: white; padding: 18px; border-radius: 10px; box-shadow: 0px 2px 8px rgba(0,0,0,0.07); margin-bottom: 12px; height: 100%; }
    .hotel-title { font-size: 22px; font-weight: bold; color: #2C3E50; text-align: center; }
    .review-text { font-size: 15px; color: #444; line-height: 1.5; }
    .ratings-title { font-weight: bold; font-size: 16px; margin-bottom: 10px; color: #2C3E50; }
    .rating-line { margin: 5px 0; font-size: 15px; color: #333; }
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
    ratings_dict = row.get("ratings_parsed", {}).copy() if isinstance(row.get("ratings_parsed"), dict) else {}
    
    st.markdown(f"<div class='content-box hotel-title'>🏨 {row['name']}</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])

    # Columna 1: Review
    with col1:
        review_html = f"""<div class="content-box"><p class="review-text">{row['text']}</p></div>"""
        st.markdown(review_html, unsafe_allow_html=True)

    # Columna 2: Ratings
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

    # Columna 3: Gráfico Comparativo con Promedios
    with col3:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        
        original_ratings_dict = row.get("ratings_parsed", {}).copy()
        
        if original_ratings_dict:
            # Convertimos los ratings del hotel actual a un DataFrame
            df_hotel = pd.DataFrame(list(original_ratings_dict.items()), columns=['Atributo', 'Puntaje'])
            df_hotel['Puntaje'] = pd.to_numeric(df_hotel['Puntaje'], errors='coerce')
            df_hotel.dropna(inplace=True)

            if not df_hotel.empty:
                # Creamos la figura usando graph_objects para tener más control
                fig = go.Figure()

                # 1. Añadimos las BARRAS del hotel actual
                fig.add_trace(go.Bar(
                    y=df_hotel['Atributo'],
                    x=df_hotel['Puntaje'],
                    name='Hotel Actual',
                    orientation='h',
                    text=df_hotel['Puntaje'],
                    textposition='outside',
                    marker_color='#007bff'
                ))

                # 2. Añadimos los MARCADORES del promedio general
                df_avg = average_ratings.reindex(df_hotel['Atributo']).reset_index()
                df_avg.columns = ['Atributo', 'Promedio']
                
                fig.add_trace(go.Scatter(
                    y=df_avg['Atributo'],
                    x=df_avg['Promedio'],
                    name='Promedio General',
                    mode='markers',
                    marker_symbol='diamond',
                    marker_size=12,
                    marker_color='rgba(255, 82, 82, 0.8)'
                ))

                # Personalizamos el diseño
                fig.update_layout(
                    barmode='overlay',
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    xaxis=dict(range=[0, 5.5]),
                    yaxis=dict(autorange="reversed"),
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=250,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                fig.update_xaxes(showticklabels=False)

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No hay ratings numéricos para graficar.")
        else:
            st.write("No hay ratings disponibles.")
            
        st.markdown('</div>', unsafe_allow_html=True)
