import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sympy import symbols, diff, lambdify, sympify

# Título de la aplicación
st.title("Explorando el concepto de pendiente en un punto")
st.write("Esta aplicación ayuda a visualizar y entender el concepto de pendiente en un punto a una función, como introducción a la derivada.")

# Entrada de la función
x = symbols('x')
user_function = st.text_input("Ingresa una función en términos de x (por ejemplo, x**2, sin(x), etc.):", "x**2")

# Procesar la función
try:
    function = sympify(user_function)
    derivative = diff(function, x)
    f = lambdify(x, function, 'numpy')
    f_prime = lambdify(x, derivative, 'numpy')

    # Selección del punto
    point = st.number_input("Selecciona el punto donde deseas calcular la pendiente:", value=1.0)

    # Valores para la tabla y la gráfica
    x_values = np.linspace(point - 5, point + 5, 10)
    y_values = f(x_values)
    slopes = f_prime(x_values)

    # Crear tabla de valores
    data = pd.DataFrame({
        'x': x_values,
        'f(x)': y_values,
        "Pendiente (f'(x))": slopes
    })

    st.subheader("Tabla de valores")
    st.write(data)

    # Gráfica de la función y la tangente
    st.subheader("Gráfica de la función y la tangente en el punto seleccionado")
    fig, ax = plt.subplots()

    # Gráfica de la función
    x_plot = np.linspace(point - 5, point + 5, 500)
    y_plot = f(x_plot)
    ax.plot(x_plot, y_plot, label=f"f(x) = {function}")

    # Punto y tangente
    tangent_line = f_prime(point) * (x_plot - point) + f(point)
    ax.plot(x_plot, tangent_line, '--', label=f"Tangente en x = {point}")
    ax.scatter([point], [f(point)], color='red', label="Punto seleccionado")

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
    ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
    ax.legend()
    st.pyplot(fig)

except Exception as e:
    st.error(f"Error al procesar la función: {e}")
