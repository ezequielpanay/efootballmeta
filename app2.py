import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para calcular la alineación óptima
def calcular_alineacion(df):
    atributos_clave = {
        'PT': ['Reflejos', 'Posicionamiento', 'Agilidad'],
        'DEC Destructor': ['Defensa', 'Contacto físico', 'Entrada'],
        'DEC Creador de Juego': ['Defensa', 'Pase al ras', 'Pases clave'],
        'LI': ['Defensa', 'Velocidad', 'Entrada'],
        'LD Defensivo': ['Defensa', 'Velocidad', 'Resistencia'],
        'MCD': ['Defensa', 'Pase al ras', 'Dedicación defensiva'],
        'MC': ['Resistencia', 'Pases', 'Control'],
        'MO Izquierdo': ['Drible', 'Pases clave', 'Visión'],
        'MO Derecho': ['Velocidad', 'Regate', 'Centros'],
        'CD': ['Remates', 'Control', 'Desmarques'],
        'SD': ['Aceleración', 'Finalización', 'Pase bombeado']
    }

    alineacion = {}
    datos_filtrados = df.copy()

    for posicion, atributos in atributos_clave.items():
        atributos_disponibles = [col for col in atributos if col in datos_filtrados.columns]
        if atributos_disponibles:
            datos_filtrados['Puntuacion'] = datos_filtrados[atributos_disponibles].mean(axis=1, skipna=True)
            mejor_jugador = datos_filtrados.loc[datos_filtrados['Puntuacion'].idxmax()]
            alineacion[posicion] = mejor_jugador['Nombre']
            datos_filtrados = datos_filtrados.drop(mejor_jugador.name)

    return alineacion

# Configurar la aplicación de Streamlit
st.title("Alineación Óptima de Jugadores")
st.write("Sube tu base de datos en formato Excel y visualiza la alineación óptima.")

# Cargar el archivo
archivo = st.file_uploader("Sube tu archivo de Excel", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    st.write("Datos cargados exitosamente:")
    st.dataframe(df.head())

    # Calcular la alineación
    alineacion = calcular_alineacion(df)

    st.write("### Alineación Óptima:")
    for posicion, jugador in alineacion.items():
        st.write(f"**{posicion}:** {jugador}")

    # Visualización de la alineación en un campo
    st.write("### Visualización de la Alineación:")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    posiciones = {
        'PT': (5, 1),
        'DEC Destructor': [(3, 3), (5, 3)],
        'DEC Creador de Juego': (7, 3),
        'LI': (2, 4),
        'LD Defensivo': (8, 4),
        'MCD': (5, 4),
        'MC': (5, 6),
        'MO Izquierdo': (3, 8),
        'MO Derecho': (7, 8),
        'CD': (4, 9),
        'SD': (6, 9)
    }

    for posicion, coord in posiciones.items():
        if isinstance(coord, tuple):
            ax.text(coord[0], coord[1], alineacion.get(posicion, ""), ha='center', va='center', fontsize=10, bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round'))
        else:
            for i, c in enumerate(coord):
                ax.text(c[0], c[1], alineacion.get(f"{posicion}", ""), ha='center', va='center', fontsize=10, bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round'))

    st.pyplot(fig)
