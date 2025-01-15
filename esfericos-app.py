import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import sph_harm

# Título de la app
st.title("Visualización de Esféricos Armónicos")

# Descripción
st.markdown(
    """
    Esta aplicación permite visualizar funciones esféricas armónicas.
    Puedes ajustar los valores de los números cuánticos \(l\) y \(m\), así como rotar y acercar la visualización 3D.
    """
)

# Sidebar para parámetros
st.sidebar.header("Parámetros")
l = st.sidebar.slider("Selecciona l (grado)", 0, 10, 2)
m = st.sidebar.slider("Selecciona m (orden)", -l, l, 0)

# Generar coordenadas esféricas
phi = np.linspace(0, 2 * np.pi, 100)
theta = np.linspace(0, np.pi, 100)
phi, theta = np.meshgrid(phi, theta)

# Calcular los esféricos armónicos
Y_lm = sph_harm(m, l, phi, theta)

# Convertir a coordenadas cartesianas para la visualización
r = np.abs(Y_lm)
x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)

# Crear figura 3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Graficar
norm = plt.Normalize(np.min(r), np.max(r))
colors = plt.cm.viridis(norm(r.real))
ax.plot_surface(x, y, z, facecolors=colors, rstride=1, cstride=1, antialiased=True, alpha=0.8)
ax.set_title(f"Esférico Armónico Y({l},{m})")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

# Ajustes visuales
ax.view_init(elev=30, azim=45)
plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap='viridis'), ax=ax, shrink=0.5, aspect=10, label='|Y(l,m)|')

# Mostrar la gráfica en Streamlit
st.pyplot(fig)

# Información adicional
st.markdown(
    """
    Los esféricos armónicos son funciones complejas que aparecen en la solución de la ecuación de Laplace en coordenadas esféricas.
    Son ampliamente utilizados en física, química y matemáticas para problemas de simetría esférica.
    """
)
