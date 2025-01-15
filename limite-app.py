import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, limit, sympify, lambdify

# Título de la aplicación
st.title("Entendiendo el concepto de límite de una función")
st.write("Esta aplicación interactiva te ayuda a comprender el concepto de límite en cálculo diferencial.")

# Entrada de la función
x = symbols('x')
user_function = st.text_input("Ingresa una función en términos de x (por ejemplo, sin(x)/x, (x**2 - 1)/(x - 1), etc.):", "(x**2 - 1)/(x - 1)")

# Punto donde evaluar el límite
try:
    function = sympify(user_function)
    f = lambdify(x, function, 'numpy')

    point = st.number_input("Ingresa el punto al que x tiende (por ejemplo, 1):", value=1.0)

    # Calcular el límite usando SymPy
    limit_value = limit(function, x, point)
    st.write(f"El valor del límite cuando x tiende a {point} es: {limit_value}")

    # Valores para visualizar la función
    delta = 0.5  # Define un intervalo alrededor del punto
    x_values = np.linspace(point - delta, point + delta, 500)
    y_values = f(x_values)

    # Evitar que la función explote en valores no definidos
    y_values[np.isinf(y_values) | np.isnan(y_values)] = np.nan

    # Gráfica del comportamiento de la función
    st.subheader("Gráfica del comportamiento de la función")
    fig, ax = plt.subplots()

    ax.plot(x_values, y_values, label=f"f(x) = {function}")
    ax.axvline(point, color='red', linestyle='--', label=f"x = {point}")
    ax.scatter([point], [limit_value], color='green', label=f"Límite = {limit_value}")

    ax.set_title("Visualización del límite")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
    ax.legend()

    st.pyplot(fig)

    # Explicación didáctica
    st.subheader("Explicación del concepto de límite")
    st.write(
        f"El límite de una función describe el valor al que se aproxima la función "
        f"cuando x se acerca a un punto dado. En este caso, cuando x tiende a {point}, "
        f"la función {function} se aproxima al valor {limit_value}.")
    st.write(
        "El comportamiento de la función cerca de este punto puede observarse en la gráfica, "
        "donde los valores de f(x) (en azul) se acercan al valor límite (en verde) cuando x se "
        "acerca al valor especificado.")

except Exception as e:
    st.error(f"Error al procesar la función: {e}")
