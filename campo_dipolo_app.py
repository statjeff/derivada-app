import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Título y descripción de la app
st.title("Campo Eléctrico de un Dipolo")
st.markdown(
    """
    Esta aplicación muestra el campo eléctrico de un dipolo formado por dos cargas
    \(+q\) y \(-q\) separadas una distancia \(d\) en el eje \(x\). Usa los controles de la barra lateral para modificar los parámetros.
    """
)

# Parámetros interactivos en la barra lateral
q = st.sidebar.number_input("Magnitud de la carga (q)", value=1.0, step=0.1)
d = st.sidebar.number_input("Separación (d)", value=1.0, step=0.1)
grid_size = st.sidebar.slider("Resolución de la cuadrícula", min_value=50, max_value=500, value=100)
extent = st.sidebar.slider("Extensión del dominio (en cada dirección)", min_value=3, max_value=10, value=5)

# Posiciones de las cargas: la carga positiva se ubica a la derecha y la negativa a la izquierda
pos_positive = np.array([ d/2, 0])
pos_negative = np.array([-d/2, 0])

# Constante de Coulomb (para visualización usamos k = 1)
k = 1

# Crear la malla de puntos
x = np.linspace(-extent, extent, grid_size)
y = np.linspace(-extent, extent, grid_size)
X, Y = np.meshgrid(x, y)

def electric_field(q, pos_charge, X, Y):
    """
    Calcula el campo eléctrico (Ex, Ey) generado por una carga q ubicada en pos_charge.
    Se añade una pequeña corrección para evitar divisiones por cero.
    """
    # Vectores de posición desde la carga hasta cada punto (x, y)
    Rx = X - pos_charge[0]
    Ry = Y - pos_charge[1]
    # Distancia con un pequeño offset para evitar singularidades
    R = np.sqrt(Rx**2 + Ry**2)
    # Evitar división por cero: se reemplazan los valores muy pequeños por un mínimo
    R = np.where(R < 0.1, 0.1, R)
    Ex = k * q * Rx / (R**3)
    Ey = k * q * Ry / (R**3)
    return Ex, Ey

# Calcular el campo eléctrico generado por cada carga
Ex_pos, Ey_pos = electric_field(q, pos_positive, X, Y)
Ex_neg, Ey_neg = electric_field(-q, pos_negative, X, Y)

# Campo eléctrico total (suma vectorial)
Ex_total = Ex_pos + Ex_neg
Ey_total = Ey_pos + Ey_neg

# Graficar el campo usando streamplot de Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))
# Se utiliza una escala logarítmica para el color en función de la magnitud del campo
magnitude = np.sqrt(Ex_total**2 + Ey_total**2)
strm = ax.streamplot(X, Y, Ex_total, Ey_total, color=np.log(magnitude), cmap='autumn', density=1.5)

# Dibujar las posiciones de las cargas
ax.scatter([pos_positive[0]], [pos_positive[1]], color='blue', s=100, label=r'$+q$')
ax.scatter([pos_negative[0]], [pos_negative[1]], color='red', s=100, label=r'$-q$')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Campo Eléctrico de un Dipolo')
ax.legend()
ax.set_aspect('equal')

# Mostrar la figura en la app de Streamlit
st.pyplot(fig)
