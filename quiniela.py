import streamlit as st
import pandas as pd
import random
from io import BytesIO

# =========================
# Datos de los países
# =========================
data = {
    "Grupo": ["Grupo A"]*4 + ["Grupo B"]*4 + ["Grupo C"]*4 + ["Grupo D"]*4 +
             ["Grupo E"]*4 + ["Grupo F"]*4 + ["Grupo G"]*4 + ["Grupo H"]*4 +
             ["Grupo I"]*4 + ["Grupo J"]*4 + ["Grupo K"]*4 + ["Grupo L"]*4,
    "Pais": [
        "México","Sudáfrica","República de Corea","Chequia",
        "Canadá","Bosnia y Herzegovina","Catar","Suiza",
        "Brasil","Marruecos","Haití","Escocia",
        "EE. UU.","Paraguay","Australia","Turquía",
        "Alemania","Curazao","Costa de Marfil","Ecuador",
        "Países Bajos","Japón","Suecia","Túnez",
        "Bélgica","Egipto","RI de Irán","Nueva Zelanda",
        "España","Islas de Cabo Verde","Arabia Saudí","Uruguay",
        "Francia","Senegal","Irak","Noruega",
        "Argentina","Argelia","Austria","Jordania",
        "Portugal","RD Congo","Uzbekistán","Colombia",
        "Inglaterra","Croacia","Ghana","Panamá"
    ]
}
df = pd.DataFrame(data)

# =========================
# Interfaz Streamlit
# =========================
st.title("Quiniela Mundial - Asignación Equitativa de Países")

# Número de participantes
num_participantes = st.number_input("Número de participantes:", min_value=2, max_value=48, step=1)

# Nombres de los participantes
nombres = []
for i in range(num_participantes):
    nombre = st.text_input(f"Nombre del participante {i+1}:")
    if nombre:
        nombres.append(nombre)

# Botón para asignar
if st.button("Generar Quiniela") and len(nombres) == num_participantes:
    asignaciones = {p: [] for p in nombres}

    # Mezclar todos los países
    paises = df.sample(frac=1).reset_index(drop=True)

    # Asignar en orden circular (round-robin)
    for i, row in paises.iterrows():
        participante = nombres[i % num_participantes]
        asignaciones[participante].append({"Grupo": row["Grupo"], "Pais": row["Pais"]})

    # Construir DataFrame final
    resultado = []
    for participante, equipos in asignaciones.items():
        for equipo in equipos:
            resultado.append({"Participante": participante, "Grupo": equipo["Grupo"], "Pais": equipo["Pais"]})
    resultado_df = pd.DataFrame(resultado)

    # Mostrar resultados sin índice
    st.subheader("Resultados de la Quiniela")
    st.dataframe(resultado_df, use_container_width=True)

    # Exportar a Excel
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        resultado_df.to_excel(writer, index=False, sheet_name="Quiniela")
    st.download_button(
        label="📥 Descargar resultados en Excel",
        data=buffer.getvalue(),
        file_name="quiniela.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
