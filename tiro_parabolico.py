import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calcular_distancia(v, angulo, g=9.8):
    """
    Calcula la distancia (alcance) para un lanzamiento parabólico
    con velocidad v (m/s), ángulo en grados y gravedad g (m/s^2).
    """
    # Convertimos el ángulo a radianes
    theta = np.radians(angulo)
    # Fórmula del alcance: (v^2 * sin(2*theta)) / g
    distancia = (v**2 * np.sin(2*theta)) / g
    return distancia

def calcular_trayectoria(v, angulo, g=9.8):
    """
    Devuelve los arreglos de valores (x, y) que describen la trayectoria del proyectil
    en función del tiempo hasta que vuelve a tocar el suelo (y=0).
    """
    theta = np.radians(angulo)
    
    # Tiempo total de vuelo: T = 2 * v * sin(theta) / g
    T = 2 * v * np.sin(theta) / g
    
    # Creamos un vector de tiempo desde 0 hasta T
    t = np.linspace(0, T, num=100)
    
    # Ecuaciones paramétricas de la posición
    x = v * np.cos(theta) * t
    y = v * np.sin(theta) * t - 0.5 * g * t**2
    
    return x, y

# Título principal de la app
st.title("Simulador de Tiro Parabólico: Pateador de Fútbol Americano")

st.write("""
Este programa te permitirá visualizar la trayectoria y la distancia alcanzada por un 
pateador que lanza el balón con una **velocidad inicial de 20 m/s** y un 
**ángulo variable entre 20° y 40°**. 
""")

# Parámetros fijos
v_inicial = 20.0  # m/s
g = 9.8           # m/s^2

# Barra lateral para seleccionar el ángulo
angulo = st.sidebar.slider(
    "Selecciona el ángulo de lanzamiento (°)", 
    min_value=20, 
    max_value=40, 
    value=30, 
    step=1
)

# Cálculo de la distancia para el ángulo actual
distancia_actual = calcular_distancia(v_inicial, angulo, g)

# Cálculo de la trayectoria
x, y = calcular_trayectoria(v_inicial, angulo, g)

# Gráfica de la trayectoria
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(x, y, label=f"Ángulo = {angulo}°")
ax.set_xlabel("Distancia (m)")
ax.set_ylabel("Altura (m)")
ax.set_title("Trayectoria del balón")
ax.grid(True)
ax.legend()

# Mostramos la gráfica en Streamlit
st.pyplot(fig)

# Mostramos la distancia alcanzada
st.write(f"**Distancia alcanzada con un ángulo de {angulo}°**: {distancia_actual:.2f} m")

# Cálculo de la distancia máxima en el rango [20°, 40°]
angulos = np.linspace(20, 40, 200)  # Probamos con más puntos para mayor precisión
distancias = [calcular_distancia(v_inicial, a, g) for a in angulos]
distancia_maxima = max(distancias)
angulo_maximo = angulos[np.argmax(distancias)]

# Mostramos la distancia máxima encontrada
st.write(f"La **distancia máxima** dentro del rango 20°-40° es de: {distancia_maxima:.2f} m")
st.write(f"Y se logra con un ángulo aproximado de: {angulo_maximo:.2f}°")

st.write("""
---
**¿Por qué ocurre esto?**

La distancia máxima para un lanzamiento parabólico sin restricciones suele alcanzarse 
alrededor de 45°. Sin embargo, en este problema, el ángulo está limitado 
entre 20° y 40°, por lo cual la distancia máxima se consigue cerca de los 40° 
debido a que un ángulo mayor (dentro del rango permitido) incrementa la componente 
vertical y, por ende, el tiempo de vuelo, resultando en un mayor alcance en el plano horizontal.
""")
