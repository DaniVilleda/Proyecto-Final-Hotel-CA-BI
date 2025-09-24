import streamlit as st
import pandas as pd
import ast
import plotly.express as px 

# Esta debe ser la primera commande de Streamlit en tu script
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

# Emojis para cada atributo
emoji_map = {
    "service": "🛎️", "cleanliness": "🧼", "overall": "⭐",
    "value": "💰", "location": "📍", "sleep_quality": "💤", "rooms": "🚪"
}

# Estilos CSS
st.markdown("""
    <style>
        .stApp { background: #f4f6f9; font-family: 'Segoe UI', sans-serif; }
        .card { background: #eaf0f7; padding: 22px; margin: 16px 0; border-radius: 14px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); }
        .content-box { background: white; padding: 18px; border-radius: 10px; box-shadow: 0px 2px 8px rgba(0,0,0,0.07); margin-bottom: 12px; height: 100%; }
        .hotel-title { font-size: 22px; font-weight: bold; color: #2C3E50; text-align: center; }
        .review-text { font-size: 15px; color: #444; line-height: 1.5; }
        .ratings-title { font-weight: bold; font-size: 16px; margin-bottom: 10px; color: #2C3E50; }
    </style>
""", unsafe_allow_html=True)

# Título principal de la aplicación
st.title("🏨 Explorador de Reviews por Tópico y Hotel")

# Filtros y lógica de datos...
topics = df['topic_label'].unique().tolist()
selected_topic = st.selectbox("📌 Selecciona un tópico", topics)
hotel_options = ['Todos'] + sorted(df['name'].unique().tolist())
selected_hotel = st.selectbox("🏩 Selecciona un hotel", hotel_options)
n_reviews = st.slider("📊 Número máximo de reviews a mostrar", 1, 20, 5)

filtered_df = df[df['topic_label'] == selected_topic]
if selected_hotel != 'Todos':
    filtered_df = filtered_df[filtered_df['name'] == selected_hotel]
else:
    filtered_df = filtered_df.drop_duplicates(subset=['name'])
filtered_df = filtered_df.head(n_reviews)

# --- Mostrar resultados ---
for idx, row in filtered_df.iterrows():
    ratings_dict = row.get("ratings_parsed", {}).copy() if isinstance(row.get("ratings_parsed"), dict) else {}

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"<div class='content-box hotel-title'>🏨 {row['name']}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        review_html = f"""
        <div class="content-box">
            <p class="review-text">{row['text']}</p>
        </div>
        """
        st.markdown(review_html, unsafe_allow_html=True)

    # --- Columna 2: AHORA CON GRÁFICO ---
    with col2:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<p class="ratings-title">Ratings:</p>', unsafe_allow_html=True)
        
        if ratings_dict:
            # 2. CONVERTIR EL DICCIONARIO DE RATINGS A UN DATAFRAME
            df_ratings = pd.DataFrame(list(ratings_dict.items()), columns=['Atributo', 'Puntaje'])
            df_ratings['Puntaje'] = pd.to_numeric(df_ratings['Puntaje'])
            
            # 3. CREAR EL GRÁFICO DE BARRAS HORIZONTAL
            fig = px.bar(
                df_ratings,
                x='Puntaje',
                y='Atributo',
                orientation='h',
                text='Puntaje',
                range_x=[0, 5] # Asegura que la escala sea siempre de 0 a 5
            )
            
            # 4. PERSONALIZAR EL DISEÑO DEL GRÁFICO PARA QUE SEA LIMPIO
            fig.update_layout(
                showlegend=False,
                xaxis_title="",
                yaxis_title="",
                yaxis=dict(autorange="reversed"), # Poner 'overall' arriba si está presente
                margin=dict(l=10, r=10, t=10, b=10),
                height=250,
                paper_bgcolor='rgba(0,0,0,0)', # Fondo transparente
                plot_bgcolor='rgba(0,0,0,0)'
            )
            fig.update_traces(
                marker_color='#007bff', # Color de las barras
                textposition='outside' # Posición del número
            )
            fig.update_xaxes(showticklabels=False) # Ocultar números del eje X
            
            # 5. MOSTRAR EL GRÁFICO EN STREAMLIT
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("No hay ratings disponibles.", unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
