# mapa_app.py

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- Configuración de la página ---
st.set_page_config(
    page_title="Mapa Interactivo",
    page_icon="🗺️",
    layout="wide"
)

# --- Título de la aplicación ---
st.title("🗺️ Mapa Interactivo con Folium en Streamlit")
st.markdown("Este es un ejemplo de cómo integrar un mapa personalizable en tu aplicación.")

# --- Creación de los Datos ---
# Puedes reemplazar esta sección para cargar tus propios datos desde un CSV, Excel, etc.
# Por ejemplo: df = pd.read_csv('tus_datos.csv')
data = {
    'Nombre': ['Ciudad de México', 'Guadalajara', 'Monterrey', 'Cancún', 'Tijuana'],
    'Descripcion': [
        'La capital del país, un centro cultural y financiero.',
        'Conocida por el tequila y la música mariachi.',
        'Importante centro industrial y de negocios.',
        'Destino turístico famoso por sus playas caribeñas.',
        'Una de las ciudades fronterizas más visitadas del mundo.'
    ],
    'lat': [19.432608, 20.659698, 25.686613, 21.161908, 32.514947],
    'lon': [-99.133209, -103.349609, -100.316116, -86.851524, -117.038246],
    'icono': ['star', 'music', 'industry', 'umbrella-beach', 'car']
}
df = pd.DataFrame(data)

st.write("### Datos de las Ubicaciones")
st.dataframe(df)

# --- Creación del Mapa ---

# 1. Calcular el centro del mapa para que todas las ubicaciones sean visibles.
map_center = [df['lat'].mean(), df['lon'].mean()]

# 2. Crear el objeto de mapa base con Folium.
#    - location: Coordenadas donde se centrará el mapa.
#    - zoom_start: Nivel de zoom inicial.
#    - tiles: Estilo del mapa de fondo (otras opciones: 'Stamen Terrain', 'CartoDB dark_matter').
m = folium.Map(location=map_center, zoom_start=5, tiles='CartoDB positron')

# 3. Añadir un marcador para cada fila en el DataFrame.
for index, row in df.iterrows():
    # Crear el contenido del pop-up (lo que se ve al hacer clic)
    popup_content = f"""
    <h5><b>{row['Nombre']}</b></h5>
    <p>{row['Descripcion']}</p>
    """

    folium.Marker(
        # Coordenadas del marcador
        location=[row['lat'], row['lon']],
        
        # Pop-up que aparece al hacer clic
        popup=folium.Popup(popup_content, max_width=300),
        
        # Tooltip que aparece al pasar el mouse
        tooltip=f"Clic para ver más sobre <b>{row['Nombre']}</b>",
        
        # Icono personalizado
        icon=folium.Icon(color='blue', prefix='fa', icon=row['icono'])
    ).add_to(m)


# --- Mostrar el Mapa en Streamlit ---
st.write("### Mapa de Ubicaciones")

# Usamos st_folium para renderizar el mapa de Folium.
# El parámetro `returned_objects` puede capturar eventos como clics en el mapa.
map_data = st_folium(m, width='100%', height=500)

st.write("---")
st.info("💡 **Tip:** Pasa el mouse sobre un marcador para ver su nombre y haz clic para obtener más detalles.")
