import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Concepto de Pendiente y Derivada")

# Introducción al concepto
st.markdown("""
### Bienvenidos
Esta aplicación te ayudará a entender el concepto de **pendiente de una curva** y cómo se relaciona con la derivada.
Sigue los pasos interactivos para visualizar y comprender mejor este concepto matemático.
""")

# Paso 1: Seleccionar una función
st.sidebar.header("Paso 1: Selecciona una función")
funcion = st.sidebar.selectbox("Elige una función:", ["f(x) = x²", "f(x) = sin(x)", "f(x) = ln(x)"])

# Generar la función seleccionada
def calcular_funcion(x):
    if funcion == "f(x) = x²":
        return x ** 2
    elif funcion == "f(x) = sin(x)":
        return np.sin(x)
    elif funcion == "f(x) = ln(x)":
        return np.log(x)

# Crear un rango de valores para x
x = np.linspace(0.1, 10, 500) if "ln" in funcion else np.linspace(-5, 5, 500)
y = calcular_funcion(x)

# Paso 2: Seleccionar un punto específico
st.sidebar.header("Paso 2: Selecciona un punto sobre la curva")
punto_x = st.sidebar.slider("Selecciona el valor de x:", float(x.min()), float(x.max()), 1.0)
punto_y = calcular_funcion(punto_x)

# Paso 3: Seleccionar un segundo punto para la pendiente
st.sidebar.header("Paso 3: Selecciona un segundo punto cercano")
punto_h = st.sidebar.slider("Selecciona un valor de h (distancia entre puntos):", 0.1, 2.0, 0.5)
segundo_x = punto_x + punto_h
segundo_y = calcular_funcion(segundo_x)

# Calcular la pendiente de la recta secante
pendiente = (segundo_y - punto_y) / (segundo_x - punto_x)

# Visualización de la curva, puntos y pendiente
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(x, y, label=f"{funcion}", color="blue")
ax.scatter([punto_x, segundo_x], [punto_y, segundo_y], color="red", label="Puntos seleccionados")
ax.plot([punto_x, segundo_x], [punto_y, segundo_y], color="green", linestyle="--", label=f"Secante: pendiente = {pendiente:.2f}")
ax.set_title("Visualización de la curva y la pendiente de la secante")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.legend()
ax.grid()

# Mostrar la gráfica
st.pyplot(fig)

# Paso 4: Introducción al límite
st.markdown("""
### Paso 4: ¿Qué sucede si reducimos h?
A medida que el valor de h se hace más pequeño, la pendiente de la recta secante se aproxima a la pendiente de la tangente en el punto seleccionado.
""")

# Deslizador interactivo para reducir h
h_reducido = st.slider("Reduce el valor de h para ver el límite:", 0.01, 0.5, 0.1)
segundo_x_reducido = punto_x + h_reducido
segundo_y_reducido = calcular_funcion(segundo_x_reducido)
pendiente_reducida = (segundo_y_reducido - punto_y) / (segundo_x_reducido - punto_x)

# Gráfica con h reducido
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.plot(x, y, label=f"{funcion}", color="blue")
ax2.scatter([punto_x, segundo_x_reducido], [punto_y, segundo_y_reducido], color="orange", label="Puntos con h reducido")
ax2.plot([punto_x, segundo_x_reducido], [punto_y, segundo_y_reducido], color="purple", linestyle="--", label=f"Pendiente aproximada = {pendiente_reducida:.2f}")
ax2.set_title("Aproximación de la pendiente de la tangente")
ax2.set_xlabel("x")
ax2.set_ylabel("f(x)")
ax2.legend()
ax2.grid()

# Mostrar la segunda gráfica
st.pyplot(fig2)

# Conclusión
st.markdown("""
### Conclusión
La **pendiente de la tangente** en un punto es el valor al que se aproxima la pendiente de la recta secante cuando h tiende a 0.
Este es el concepto fundamental de la derivada.
""")
