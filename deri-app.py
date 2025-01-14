import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

st.title("Aprende derivadas de funciones algebraicas")

# Entrada de la función
func_str = st.text_input("Ingresa una función algebraica en términos de x", "x**2 + 3*x")
x = sp.symbols('x')
func = sp.sympify(func_str)

# Cálculo de la derivada
derivative = sp.diff(func, x)
st.write(f"Derivada: {derivative}")

# Gráficos
func_lambdified = sp.lambdify(x, func, "numpy")
derivative_lambdified = sp.lambdify(x, derivative, "numpy")
x_vals = np.linspace(-10, 10, 500)
y_vals = func_lambdified(x_vals)
dy_vals = derivative_lambdified(x_vals)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x_vals, y_vals, label=f"f(x) = {func}")
ax.plot(x_vals, dy_vals, label=f"f'(x) = {derivative}", linestyle="--")
ax.axhline(0, color="black", linewidth=0.8)
ax.set_title("Función y su derivada")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
ax.grid()
st.pyplot(fig)
