import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def plot_function_and_derivative(expr, derivative_expr, x_range=(-10, 10)):
    """
    Function to plot a given expression and its derivative over a specified range.
    """
    x = sp.symbols('x')
    func = sp.lambdify(x, expr, "numpy")
    deriv = sp.lambdify(x, derivative_expr, "numpy")

    x_vals = np.linspace(x_range[0], x_range[1], 500)
    y_vals = func(x_vals)
    dy_vals = deriv(x_vals)

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label=f"f(x) = {expr}")
    plt.plot(x_vals, dy_vals, label=f"f'(x) = {derivative_expr}", linestyle="--")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Función racional y su derivada")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid()
    st.pyplot(plt)

# Configuración básica de Streamlit
st.title("Aprende derivadas de funciones racionales")
st.write("Este programa interactivo te ayuda a aprender cómo calcular derivadas de funciones racionales.")

# Entrada de la función
st.header("Ingresa una función racional")
func_input = st.text_input("Función racional en términos de x (ejemplo: (x**2 + 1) / (x - 2))", "(x**2 + 1) / (x - 2)")

if func_input:
    try:
        # Define la variable simbólica y la función
        x = sp.symbols('x')
        func = sp.sympify(func_input)

        # Calcula la derivada
        derivative = sp.diff(func, x)

        # Muestra la función y su derivada
        st.subheader("Resultados")
        st.latex(f"f(x) = {sp.latex(func)}")
        st.latex(f"f'(x) = {sp.latex(derivative)}")

        # Selección del rango para graficar
        st.subheader("Gráficas")
        st.write("Selecciona el rango de valores de x para graficar.")
        x_min = st.number_input("Valor mínimo de x", value=-10.0)
        x_max = st.number_input("Valor máximo de x", value=10.0)

        if x_min < x_max:
            plot_function_and_derivative(func, derivative, (x_min, x_max))
        else:
            st.error("El valor mínimo de x debe ser menor que el máximo.")

        # Explicaciones adicionales
        st.subheader("Explicación paso a paso")
        st.write("Para derivar una función racional, usamos la regla del cociente:")
        st.latex(r"\frac{d}{dx}\left(\frac{u(x)}{v(x)}\right) = \frac{u'(x)v(x) - u(x)v'(x)}{[v(x)]^2}")
        st.write("1. Identifica el numerador y el denominador.\n"
                 "2. Deriva el numerador y el denominador.\n"
                 "3. Sustituye en la fórmula de la regla del cociente.")

    except Exception as e:
        st.error(f"Error al procesar la función: {e}")
