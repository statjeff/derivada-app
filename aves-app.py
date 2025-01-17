import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------
# Funciones del modelo
# ----------------------------------------------------

def potencia(v, A, B, L):
    """
    Potencia requerida: P(v) = A*v^3 + (B*L^2)/v
    """
    return A*(v**3) + (B*(L**2))/v

def energia_por_distancia(v, A, B, L):
    """
    Energía por unidad de distancia: E(v) = P(v)/v = A*v^2 + (B*L^2)/v^2
    """
    return A*(v**2) + (B*(L**2))/(v**2)

def velocidad_minima_potencia(A, B, L):
    """
    v_min_P = ((B*L^2)/(3*A))^(1/4)
    """
    return ((B*(L**2))/(3*A))**0.25

def velocidad_minima_energia(A, B, L):
    """
    v_min_E = ((B*L^2)/A)^(1/4)
    """
    return ((B*(L**2))/A)**0.25

def potencia_promedio(x, v, Ab, Aw, B, m, g=9.81):
    """
    Potencia promedio cuando fracción x del tiempo el ave aletea y (1-x) planea:
    P_prom = A_b*v^3 + x*A_w*v^3 + (B*m^2*g^2)/( x*v )
    """
    return Ab*(v**3) + x*Aw*(v**3) + (B*(m**2)*(g**2))/(x*v)

def x_optimo(Ab, Aw, B, v, m, g=9.81):
    """
    x que minimiza la potencia promedio:
    x = sqrt( (B*m^2*g^2) / (A_w*v^4) )
    """
    if Aw <= 0:
        return None  # Evitamos división por 0
    return np.sqrt((B*(m**2)*(g**2)) / (Aw*(v**4)))


# ----------------------------------------------------
# Configuración de la página
# ----------------------------------------------------
st.set_page_config(
    page_title="Aves y Aviones: Energía Mínima",
    layout="centered",
)

st.title("Aves y Aviones: Energía Mínima")
st.write(
    "Esta aplicación interactiva muestra cómo, para un modelo de potencia "
    "aeronáutica simplificado, se determinan las velocidades que minimizan "
    "la **potencia** y la **energía por unidad de distancia**, y cómo una ave "
    "puede alternar entre aleteo y planeo."
)

# ----------------------------------------------------
# Sección 1: Parámetros y cálculo de v_min
# ----------------------------------------------------
st.header("1. Parámetros del modelo básico")

col1, col2, col3 = st.columns(3)
with col1:
    A = st.number_input("Constante A", value=1.0, min_value=0.0001, step=0.1)
with col2:
    B = st.number_input("Constante B", value=1.0, min_value=0.0001, step=0.1)
with col3:
    L = st.number_input("Sustentación (L)", value=1.0, min_value=0.0001, step=0.1)

v_min_P = velocidad_minima_potencia(A, B, L)
v_min_E = velocidad_minima_energia(A, B, L)

st.markdown(
    f"""
**Velocidad que minimiza la potencia**  
\\( v_{{\\min P}} = \\bigl(\\tfrac{{B\\,L^2}}{{3\\,A}}\\bigr)^{{1/4}} \\approx {v_min_P:.3f}\\)

**Velocidad que minimiza la energía por distancia**  
\\( v_{{\\min E}} = \\bigl(\\tfrac{{B\\,L^2}}{{A}}\\bigr)^{{1/4}} \\approx {v_min_E:.3f}\\)

Razón: \\( \\frac{{v_{{\\min E}}}}{{v_{{\\min P}}}} = (3)^{{1/4}} \\approx 1.316 \\)
"""
)

# ----------------------------------------------------
# Sección 2: Gráficas de P(v) y E(v)
# ----------------------------------------------------
st.header("2. Gráficas de Potencia y Energía por distancia")

st.write("Modifica el rango y la resolución de la gráfica para explorar la forma de las funciones.")

col_v1, col_v2, col_v3 = st.columns(3)
with col_v1:
    v_min = st.number_input("v mínimo (gráfica)", value=0.1, min_value=0.01, step=0.05)
with col_v2:
    v_max = st.number_input("v máximo (gráfica)", value=5.0, step=0.5)
with col_v3:
    n_points = st.number_input("N° de puntos", value=200, min_value=10, step=10)

# Generar arreglo de velocidades
v_vals = np.linspace(v_min, v_max, n_points)

P_vals = potencia(v_vals, A, B, L)
E_vals = energia_por_distancia(v_vals, A, B, L)

fig, ax = plt.subplots(1, 2, figsize=(12,5))

# Gráfica P(v)
ax[0].plot(v_vals, P_vals, label="P(v)")
ax[0].axvline(v_min_P, color="r", linestyle="--", label="v_min_P")
ax[0].set_xlabel("Velocidad v")
ax[0].set_ylabel("Potencia P(v)")
ax[0].set_title("Potencia vs Velocidad")
ax[0].legend()
ax[0].grid(True)

# Gráfica E(v)
ax[1].plot(v_vals, E_vals, label="E(v)", color="purple")
ax[1].axvline(v_min_E, color="r", linestyle="--", label="v_min_E")
ax[1].set_xlabel("Velocidad v")
ax[1].set_ylabel("Energía por distancia E(v)")
ax[1].set_title("Energía por distancia vs Velocidad")
ax[1].legend()
ax[1].grid(True)

st.pyplot(fig)

# ----------------------------------------------------
# Sección 3: Aleteo-planeo
# ----------------------------------------------------
st.header("3. Aleteo y planeo: fracción de tiempo óptima")

st.write(
    "Supondremos que la potencia $A\\,v^3$ se divide en la parte del "
    "cuerpo $A_b\\,v^3$ y la de las alas $A_w\\,v^3$. "
    "Además, cuando el ave aletea (fracción $x$ del tiempo), "
    "tiene que generar toda la sustentación (peso $m g$)."
)

st.subheader("Parámetros adicionales del ave")
col4, col5, col6 = st.columns(3)
with col4:
    Ab = st.number_input("A_b", value=0.5, min_value=0.0, step=0.1)
with col5:
    Aw = st.number_input("A_w", value=0.5, min_value=0.0, step=0.1)
with col6:
    m_val = st.number_input("Masa del ave (m, en kg)", value=1.0, step=0.1)

g_val = 9.81

st.write(
    "La potencia promedio en un ciclo (aleteo + planeo) es: \n\n"
    "$$ P_{\\text{prom}} = A_b\\,v^3 + x\\,A_w\\,v^3 \\,+\\, \\frac{B\\,m^2\\,g^2}{x\\,v}. $$"
)

v_ave = st.slider("Velocidad del ave (v)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)

x_opt = x_optimo(Ab, Aw, B, v_ave, m_val, g_val)
if x_opt is not None and x_opt > 0:
    st.write(f"**Fracción de tiempo óptima (x):** {x_opt:.3f}")
    if x_opt >= 1:
        st.warning("El valor x ≥ 1 sugiere que el ave debería aletear todo el tiempo (modelo extrapolado).")
else:
    st.warning("No se puede calcular un valor positivo de x en este caso (verifica que A_w > 0).")

# Graficar P_promedio vs x para ilustrar
st.subheader("Gráfica de P_prom vs x")

x_range = np.linspace(0.01, 0.99, 200)  # fracción de tiempo 0 < x < 1
P_prom_vals = [potencia_promedio(xx, v_ave, Ab, Aw, B, m_val, g_val) for xx in x_range]

fig2, ax2 = plt.subplots(figsize=(6,4))
ax2.plot(x_range, P_prom_vals, label="P_prom(x)")
if x_opt is not None and 0 < x_opt < 1:
    P_opt = potencia_promedio(x_opt, v_ave, Ab, Aw, B, m_val, g_val)
    ax2.plot(x_opt, P_opt, 'ro', label="x óptimo")
ax2.set_xlabel("Fracción de tiempo aleteando (x)")
ax2.set_ylabel("Potencia promedio")
ax2.set_title("Potencia promedio vs fracción de aleteo")
ax2.legend()
ax2.grid(True)

st.pyplot(fig2)

st.markdown(
    "**Interpretación:** el punto rojo (si está en el rango 0 < x < 1) "
    "es donde la potencia promedio en el ciclo es menor. Fuera de ese rango, "
    "el modelo sugiere aleteo continuo o planeo continuo (dependiendo de los parámetros)."
)

st.write("---")
st.write(
    "_Esta aplicación es una demostración simplificada basada en el libro "
    "Optima for Animals de R. McNeill Alexander (Princeton University Press, 1996)._\n\n"
    "¡Experimenta modificando los parámetros para ver cómo cambia la velocidad óptima y la "
    "fracción de tiempo de aleteo!"
)
