import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para calcular la alineación óptima
def calcular_alineacion(df, seleccion_usuario=None):
    atributos_clave = {
        'DEC Destructor': ['Defensa', 'Contacto físico', 'Entrada', 'Agresividad'],
        'DEC Creador de Juego': ['Defensa', 'Pase bombeado', 'Entrada', 'Dedicación defensiva'],
        'DEC Medio Escudo': ['Defensa', 'Dedicación defensiva', 'Agresividad', 'Contacto físico'],
        'DEC Lateral Defensivo': ['Defensa', 'Velocidad', 'Entrada', 'Resistencia'],
        'LD': ['Velocidad', 'Centros', 'Resistencia', 'Defensa'],
        'LI': ['Velocidad', 'Centros', 'Resistencia', 'Defensa'],
        'MCD': ['Defensa', 'Entrada', 'Agresividad', 'Dedicación defensiva', 'Contacto físico'],
        'MC': ['Resistencia', 'Pase bombeado', 'Control', 'Defensa'],
        'MO': ['Drible', 'Velocidad', 'Pase bombeado', 'Resistencia'],
        'MDI': ['Velocidad', 'Centros', 'Drible', 'Regates'],
        'MDD': ['Velocidad', 'Centros', 'Drible', 'Regates'],
        'CD': ['Remates', 'Potencia de tiro', 'Desmarques', 'Velocidad'],
        'SD': ['Pase bombeado', 'Control', 'Velocidad', 'Regates'],
        'EXI': ['Velocidad', 'Regates', 'Centros', 'Remates'],
        'EXD': ['Velocidad', 'Regates', 'Centros', 'Remates']
    }

    alineacion = {}
    datos_filtrados = df.copy()

    # Si el usuario selecciona automáticamente
    if seleccion_usuario is None:
        posiciones_seleccion = [
            'PT',
            'DEC Destructor', 'DEC Destructor', 'DEC Creador de Juego',
            'LD', 'LI',
            'MCD', 'MC',
            'MO', 'CD', 'SD'
        ]

        for posicion in posiciones_seleccion:
            atributos = atributos_clave.get(posicion, [])
            atributos_disponibles = [col for col in atributos if col in datos_filtrados.columns]
            if atributos_disponibles:
                datos_filtrados['Puntuacion'] = datos_filtrados[atributos_disponibles].mean(axis=1, skipna=True)
                if not datos_filtrados.empty:
                    mejor_jugador = datos_filtrados.loc[datos_filtrados['Puntuacion'].idxmax()]
                    alineacion[posicion] = mejor_jugador['Nombre']
                    datos_filtrados = datos_filtrados.drop(mejor_jugador.name)

    # Si el usuario selecciona manualmente
    else:
        for posicion, rol in seleccion_usuario.items():
            atributos = atributos_clave.get(rol, [])
            atributos_disponibles = [col for col in atributos if col in datos_filtrados.columns]
            if atributos_disponibles:
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

    # Selección automática o manual
    seleccion_tipo = st.radio("Selecciona el tipo de alineación:", ("Automática", "Manual"))

    if seleccion_tipo == "Automática":
        alineacion = calcular_alineacion(df)
    else:
        st.write("Selecciona los roles para cada posición:")
        roles_disponibles = {
            'DEC': ['Destructor', 'Creador de Juego', 'Medio Escudo', 'Lateral Defensivo'],
            'LD': ['Lateral Ofensivo', 'Lateral Defensivo', 'Especialista en Centros', 'Lateral Finalizador', 'Organizador'],
            'LI': ['Lateral Ofensivo', 'Lateral Defensivo', 'Especialista en Centros', 'Lateral Finalizador', 'Organizador'],
            'MCD': ['Destructor', 'Medio Escudo', 'Organizador', 'Omnipresente', 'Creador de Juego', 'Jugador de Huecos'],
            'MC': ['Destructor', 'Medio Escudo', 'Organizador', 'Omnipresente', 'Creador de Juego', 'Jugador de Huecos'],
            'MO': ['Destructor', 'Medio Escudo', 'Organizador', 'Omnipresente', 'Creador de Juego', 'Jugador de Huecos'],
            'CD': ['Cazagoles', 'Hombre de área', 'Hombre Objetivo', 'Jugador de Huecos', 'Diez Clásico', 'Segundo Delantero'],
            'SD': ['Cazagoles', 'Hombre de área', 'Hombre Objetivo', 'Jugador de Huecos', 'Diez Clásico', 'Segundo Delantero']
        }

        seleccion_usuario = {}
        for posicion in ['PT', 'DEC', 'DEC', 'DEC', 'LD', 'LI', 'MCD', 'MC', 'MO', 'CD', 'SD']:
            rol = st.selectbox(f"Selecciona el rol para {posicion}", roles_disponibles.get(posicion.split()[0], []))
            seleccion_usuario[posicion] = f"{posicion.split()[0]} {rol}"

        alineacion = calcular_alineacion(df, seleccion_usuario)

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
        'DEC Destructor': [(2, 3), (5, 3), (8, 3)],
        'LD': (1, 4),
        'LI': (9, 4),
        'MCD': (4, 5),
        'MC': (6, 5),
        'MO': (5, 7),
        'CD': (4, 9),
        'SD': (6, 9)
    }

    for posicion, coord in posiciones.items():
        if isinstance(coord, tuple):
            ax.text(coord[0], coord[1], alineacion.get(posicion, ""), ha='center', va='center', fontsize=10, bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round'))
        elif isinstance(coord, list):
            for i, c in enumerate(coord):
                pos_key = f"{posicion} ({i+1})"
                ax.text(c[0], c[1], alineacion.get(pos_key, ""), ha='center', va='center', fontsize=10, bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round'))

    st.pyplot(fig)
