import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para calcular la alineación óptima
def calcular_alineacion(df):
    atributos_clave = {
        'PT': ['Reflejos', 'Posicionamiento', 'Agilidad'],
        'DEC Destructor': ['Defensa', 'Contacto físico', 'Entrada', 'Agresividad'],
        'DEC Creador de Juego': ['Defensa', 'Pase bombeado', 'Entrada', 'Dedicación defensiva'],
        'DEC Medio Escudo': ['Defensa', 'Dedicación defensiva', 'Agresividad', 'Contacto físico'],
        'DEC Lateral Defensivo': ['Defensa', 'Velocidad', 'Entrada', 'Resistencia'],
        'LI Lateral Defensivo': ['Defensa', 'Velocidad', 'Entrada', 'Resistencia'],
        'LI Lateral Ofensivo': ['Velocidad', 'Resistencia', 'Centros', 'Regates'],
        'LI Lateral Finalizador': ['Velocidad', 'Potencia de tiro', 'Remates', 'Regates'],
        'LI Especialista en Centros': ['Velocidad', 'Centros', 'Resistencia', 'Pase bombeado'],
        'LI Organizador': ['Posesión', 'Pase bombeado', 'Entrada', 'Resistencia'],
        'LD Lateral Defensivo': ['Defensa', 'Velocidad', 'Entrada', 'Resistencia'],
        'LD Lateral Ofensivo': ['Velocidad', 'Resistencia', 'Centros', 'Regates'],
        'LD Lateral Finalizador': ['Velocidad', 'Potencia de tiro', 'Remates', 'Regates'],
        'LD Especialista en Centros': ['Velocidad', 'Centros', 'Resistencia', 'Pase bombeado'],
        'LD Organizador': ['Posesión', 'Pase bombeado', 'Entrada', 'Resistencia'],
        'MCD Destructor': ['Defensa', 'Entrada', 'Agresividad', 'Dedicación defensiva', 'Contacto físico'],
        'MCD Medio Escudo': ['Defensa', 'Dedicación defensiva', 'Agresividad', 'Contacto físico'],
        'MCD Organizador': ['Pase bombeado', 'Posesión', 'Defensa', 'Entrada', 'Dedicación defensiva']
    }

    alineacion = {}
    datos_filtrados = df.copy()

    for posicion, atributos in atributos_clave.items():
        atributos_disponibles = [col for col in atributos if col in datos_filtrados.columns]
        if atributos_disponibles:
            if "MCD" in posicion:
                # Filtrar jugadores con valores defensivos mayores o iguales a 88
                defensivos = ['Actitud defensiva', 'Entrada', 'Agresividad', 'Dedicación defensiva', 'Contacto físico']
                if all(attr in datos_filtrados.columns for attr in defensivos):
                    jugadores_defensivos = datos_filtrados[(datos_filtrados[defensivos].mean(axis=1, skipna=True) >= 88)]
                    if jugadores_defensivos.empty:
                        # Si no hay jugadores que cumplan, usar los mejores disponibles
                        jugadores_defensivos = datos_filtrados
                else:
                    jugadores_defensivos = datos_filtrados

                datos_filtrados = jugadores_defensivos

            datos_filtrados['Puntuacion'] = datos_filtrados[atributos_disponibles].mean(axis=1, skipna=True)
            if not datos_filtrados.empty:
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
        'DEC Destructor': [(3, 3), (7, 3)],
        'DEC Creador de Juego': (5, 3),
        'LI Lateral Defensivo': (2, 4),
        'LD Lateral Defensivo': (8, 4),
        'DEC Medio Escudo': (5, 2),
        'MCD Destructor': (4, 4),
        'MCD Organizador': (6, 4),
        # Otras posiciones ofensivas y defensivas
    }

    for posicion, coord in posiciones.items():
        if isinstance(coord, tuple):
            ax.text(coord[0], coord[1], alineacion.get(posicion, ""), ha='center', va='center', fontsize=10, bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round'))
        else:
            for i, c in enumerate(coord):
                ax.text(c[0], c[1], alineacion.get(f"{posicion}", ""), ha='center', va='center', fontsize=10, bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round'))

    st.pyplot(fig)
