import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la aplicación
st.title("Demostración de Reflexión y Refracción de la Luz")
st.sidebar.header("Parámetros de la simulación")

# Parámetros ajustables
modo = st.sidebar.selectbox("Seleccionar fenómeno", ["Reflexión", "Refracción"])
angulo_incidencia = st.sidebar.slider("Ángulo de incidencia (°)", 0, 90, 45)
n1 = st.sidebar.number_input("Índice de refracción del medio 1 (n1)", min_value=1.0, value=1.0, step=0.1)
n2 = st.sidebar.number_input("Índice de refracción del medio 2 (n2)", min_value=1.0, value=1.5, step=0.1)

# Conversión del ángulo a radianes
angulo_incidencia_rad = np.radians(angulo_incidencia)

# Cálculos de reflexión y refracción
angulo_reflexion_rad = angulo_incidencia_rad
angulo_reflexion = np.degrees(angulo_reflexion_rad)

# Verificación para refracción
if n1 <= n2:
    angulo_refraccion_rad = np.arcsin((n1 / n2) * np.sin(angulo_incidencia_rad))
else:
    try:
        angulo_refraccion_rad = np.arcsin((n1 / n2) * np.sin(angulo_incidencia_rad))
    except ValueError:
        angulo_refraccion_rad = np.nan
angulo_refraccion = np.degrees(angulo_refraccion_rad)

# Visualización
fig, ax = plt.subplots(figsize=(8, 6))

if modo == "Reflexión":
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    
    # Rayo incidente
    ax.arrow(0, 0, np.cos(angulo_incidencia_rad), np.sin(angulo_incidencia_rad),
             head_width=0.1, head_length=0.1, fc='blue', ec='blue', label="Rayo incidente")

    # Rayo reflejado
    ax.arrow(0, 0, np.cos(angulo_reflexion_rad), -np.sin(angulo_reflexion_rad),
             head_width=0.1, head_length=0.1, fc='red', ec='red', label="Rayo reflejado")

    # Etiquetas
    ax.text(0.5, 0.5, f"Incidencia: {angulo_incidencia}°", color="blue")
    ax.text(0.5, -0.5, f"Reflexión: {angulo_reflexion}°", color="red")
    ax.set_title("Simulación de Reflexión de la Luz")

elif modo == "Refracción":
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")

    # Rayo incidente
    ax.arrow(0, 0, np.cos(angulo_incidencia_rad), np.sin(angulo_incidencia_rad),
             head_width=0.1, head_length=0.1, fc='blue', ec='blue', label="Rayo incidente")

    # Rayo refractado
    if not np.isnan(angulo_refraccion):
        ax.arrow(0, 0, np.cos(angulo_refraccion_rad), -np.sin(angulo_refraccion_rad),
                 head_width=0.1, head_length=0.1, fc='green', ec='green', label="Rayo refractado")

    # Rayo reflejado
    ax.arrow(0, 0, np.cos(angulo_reflexion_rad), -np.sin(angulo_reflexion_rad),
             head_width=0.1, head_length=0.1, fc='red', ec='red', label="Rayo reflejado")

    # Etiquetas
    ax.text(0.5, 0.5, f"Incidencia: {angulo_incidencia}°", color="blue")
    if not np.isnan(angulo_refraccion):
        ax.text(0.5, -0.5, f"Refracción: {angulo_refraccion:.2f}°", color="green")
    ax.text(-1, -0.5, f"Reflexión: {angulo_reflexion}°", color="red")
    ax.set_title("Simulación de Refracción de la Luz")

# Ajustes del gráfico
ax.legend()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.set_xlabel("Eje X")
ax.set_ylabel("Eje Y")

# Mostrar gráfico
st.pyplot(fig)

# Explicaciones teóricas
st.subheader("Explicación teórica")
if modo == "Reflexión":
    st.write("""
    **Ley de Reflexión:**
    - El ángulo de incidencia es igual al ángulo de reflexión.
    - Ambos ángulos se miden con respecto a la normal de la superficie.
    """)
elif modo == "Refracción":
    st.write("""
    **Ley de Snell:**
    \[ n_1 \sin(\theta_1) = n_2 \sin(\theta_2) \]
    - Donde:
        - \( n_1 \): Índice de refracción del primer medio.
        - \( n_2 \): Índice de refracción del segundo medio.
        - \( \theta_1 \): Ángulo de incidencia.
        - \( \theta_2 \): Ángulo de refracción.
    - Si el rayo pasa de un medio más denso a uno menos denso (\( n_1 > n_2 \)), puede ocurrir reflexión interna total.
    """)
