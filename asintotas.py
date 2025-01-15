import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Visualización de Asíntotas de Funciones Racionales")

# Descripción
st.markdown(
    """
    Esta aplicación interactiva te permite visualizar las **asíntotas verticales**, **horizontales** y/o **oblicuas** de una función racional. 
    Ingresa los coeficientes de los polinomios del numerador y denominador para explorar cómo se comporta la función.
    """
)

# Entrada de datos
st.sidebar.header("Configuración de la función")

def input_polynomial(name):
    st.sidebar.subheader(f"Coeficientes del {name}")
    degree = st.sidebar.number_input(f"Grado del {name}", min_value=0, step=1, value=1)
    coefficients = []
    for i in range(degree, -1, -1):
        coef = st.sidebar.number_input(f"Coeficiente de x^{i} en el {name}", value=1.0)
        coefficients.append(coef)
    return np.array(coefficients)

numerator = input_polynomial("Numerador")
denominator = input_polynomial("Denominador")

# Generación de la función racional
def rational_function(x):
    num = np.polyval(numerator, x)
    den = np.polyval(denominator, x)
    return num / den

# Identificar asíntotas verticales
roots_denominator = np.roots(denominator)
vertical_asymptotes = roots_denominator[np.isreal(roots_denominator)].real

# Identificar asíntotas horizontales y oblicuas
deg_num = len(numerator) - 1
deg_den = len(denominator) - 1

if deg_num < deg_den:
    horizontal_asymptote = 0
    oblique_asymptote = None
elif deg_num == deg_den:
    horizontal_asymptote = numerator[0] / denominator[0]
    oblique_asymptote = None
else:
    horizontal_asymptote = None
    oblique_coefficients = np.polydiv(numerator, denominator)[0]
    oblique_asymptote = np.poly1d(oblique_coefficients)

# Visualización interactiva
st.subheader("Gráfica de la función")
x = np.linspace(-10, 10, 1000)
y = rational_function(x)

fig, ax = plt.subplots()
ax.plot(x, y, label="Función Racional")

# Añadir asíntotas verticales
for va in vertical_asymptotes:
    ax.axvline(va, color="red", linestyle="--", label=f"Asíntota Vertical: x = {va:.2f}")

# Añadir asíntota horizontal
if horizontal_asymptote is not None:
    ax.axhline(horizontal_asymptote, color="blue", linestyle="--", label=f"Asíntota Horizontal: y = {horizontal_asymptote:.2f}")

# Añadir asíntota oblicua
if oblique_asymptote is not None:
    y_oblique = np.polyval(oblique_asymptote, x)
    ax.plot(x, y_oblique, color="green", linestyle="--", label="Asíntota Oblicua")

ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
ax.axvline(0, color="black", linewidth=0.5, linestyle="--")
ax.legend()
ax.set_title("Función Racional y sus Asíntotas")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")

st.pyplot(fig)

# Mostrar asíntotas calculadas
st.subheader("Información de las Asíntotas")

st.markdown("### Asíntotas Verticales")
if len(vertical_asymptotes) > 0:
    st.write(", ".join([f"x = {va:.2f}" for va in vertical_asymptotes]))
else:
    st.write("No hay asíntotas verticales.")

st.markdown("### Asíntotas Horizontales")
if horizontal_asymptote is not None:
    st.write(f"y = {horizontal_asymptote:.2f}")
else:
    st.write("No hay asíntotas horizontales.")

st.markdown("### Asíntotas Oblicuas")
if oblique_asymptote is not None:
    st.write(f"y = {oblique_asymptote}")
else:
    st.write("No hay asíntotas oblicuas.")
