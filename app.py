import streamlit as st
import pandas as pd

df = pd.read_csv("https://github.com/melody-10/Proyecto_Hoteles_California/blob/main/final_database.csv?raw=true")

st.title("Explorador de Reviews por Tópico y Hotel")

topics = df['topic_label'].unique().tolist()
selected_topic = st.selectbox("Selecciona un tópico", topics)

hotel_options = ['Todos'] + sorted(df['name'].unique().tolist())
selected_hotel = st.selectbox("Selecciona un hotel", hotel_options)

n_reviews = st.slider("Número máximo de reviews a mostrar", min_value=1, max_value=20, value=5)

filtered_df = df[df['topic_label'] == selected_topic]

if selected_hotel != 'Todos':
    filtered_df = filtered_df[filtered_df['name'] == selected_hotel]
else:
    # Mostrar solo una review representativa por hotel
    filtered_df = filtered_df.groupby('name').head(1).reset_index(drop=True)

filtered_df = filtered_df.head(n_reviews)

for idx, row in filtered_df.iterrows():
    st.subheader(row['name'])
    st.write("Rating:", row['ratings'])
    st.write("Review:", row['text'])
    st.write("---")

