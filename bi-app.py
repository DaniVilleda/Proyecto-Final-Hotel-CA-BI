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
    .rating-line { margin: 8px 0; font-size: 15px; color
