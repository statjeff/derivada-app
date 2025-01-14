import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def plot_function_and_critical_points(expr, x_range=(-10, 10)):
    """
    Function to plot a given expression and its critical points over a specified range.
    """
    x = sp.symbols('x')
    func = sp.lambdify(x, expr, "numpy")
    derivative = sp.diff(expr, x)
    deriv_func = sp.lambdify(x, derivative, "numpy")

    x_vals = np.linspace(x_range[0], x_range[1], 500)
    y_vals = func(x_vals)
    dy_vals = deriv_func(x_vals)

    # Find critical points
    critical_points = sp.solveset(derivative, x, domain=sp.S.Reals)
    critical_points_numeric = [float(p) for p in critical_points if p.is_real]
    critical_y_vals = [func(p) for p in critical_points_numeric]

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, label=f"f(x) = {expr}")
    plt.scatter(critical_points_numeric, critical_y_vals, color="red", label="Puntos críticos")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.title("Función y puntos críticos")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid()
    st.pyplot(plt)

# Configuración básica de Streamlit
st.title("Problemas de optimización usando cálculo diferencial")
st.write("Este programa interactivo te guía para resolver problemas de optimización paso a paso utilizando cálculo diferencial.")

# Entrada de la función
st.header("Ingresa una función para optimizar")
func_input = st.text_input("Función en términos de x (ejemplo: x**3 - 6*x**2 + 9*x + 1)", "x**3 - 6*x**2 + 9*x + 1")

if func_input:
    try:
        # Define la variable simbólica y la función
        x = sp.symbols('x')
        func = sp.sympify(func_input)

        # Calcula la derivada y puntos críticos
        derivative = sp.diff(func, x)
        critical_points = sp.solveset(derivative, x, domain=sp.S.Reals)

        # Verifica el tipo de cada punto crítico
        second_derivative = sp.diff(derivative, x)
        critical_point_types = []
        for point in critical_points:
            if point.is_real:
                second_derivative_value = second_derivative.subs(x, point)
                if second_derivative_value > 0:
                    critical_point_types.append((point, "Mínimo"))
                elif second_derivative_value < 0:
                    critical_point_types.append((point, "Máximo"))
                else:
                    critical_point_types.append((point, "Punto de inflexión"))

        # Muestra los resultados
        st.subheader("Resultados")
        st.latex(f"f(x) = {sp.latex(func)}")
        st.latex(f"f'(x) = {sp.latex(derivative)}")
        st.latex(f"f''(x) = {sp.latex(second_derivative)}")

        st.write("### Puntos críticos y su tipo:")
        for point, p_type in critical_point_types:
            st.write(f"x = {point}: {p_type}")

        # Selección del rango para graficar
        st.subheader("Gráfica de la función y puntos críticos")
        st.write("Selecciona el rango de valores de x para graficar.")
        x_min = st.number_input("Valor mínimo de x", value=-10.0)
        x_max = st.number_input("Valor máximo de x", value=10.0)

        if x_min < x_max:
            plot_function_and_critical_points(func, (x_min, x_max))
        else:
            st.error("El valor mínimo de x debe ser menor que el máximo.")

        # Explicación adicional
        st.subheader("Explicación paso a paso")
        st.write("1. Deriva la función para encontrar los puntos críticos (donde f'(x) = 0).\n"
                 "2. Usa la segunda derivada para determinar el tipo de cada punto crítico:\n"
                 "   - Si f''(x) > 0 en el punto, es un mínimo.\n"
                 "   - Si f''(x) < 0 en el punto, es un máximo.\n"
                 "   - Si f''(x) = 0, podría ser un punto de inflexión.")

    except Exception as e:
        st.error(f"Error al procesar la función: {e}")
