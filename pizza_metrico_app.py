import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ===============================================
# FUNCIONES DEL MODELO
# ===============================================

def perimeter_slice(theta, r):
    """
    Perímetro de la rebanada (sector): P = r*theta + 2*r
    """
    return r*theta + 2*r

def area_slice(theta, r):
    """
    Área de la rebanada (sector): A = (1/2)*r^2*theta
    """
    return 0.5 * r**2 * theta

# Perímetro fijo (ahora en centímetros)
PERIM_FIXED = 32  # 32 cm

# ===============================================
# CONFIGURACIÓN BÁSICA DE STREAMLIT
# ===============================================

st.set_page_config(
    page_title="Rebanada de Pizza con Perímetro Fijo (cm)",
    layout="centered",
)

st.title("Rebanada de Pizza con Perímetro Fijo = 32 cm")

st.write(
    "Este ejemplo ilustra cómo, imponiendo un **perímetro fijo** de 32 cm "
    "para una rebanada (sector circular), se determina qué diámetro de pizza "
    "permite que esa rebanada tenga **el área más grande**."
)

# ===============================================
# SECCIÓN TEÓRICA Y FÓRMULAS EN LATEX
# ===============================================
st.header("1. Formulación del Problema")

st.markdown(
    r"""
**Sea** \(r\) el radio de la pizza, y \(\theta\) el ángulo de la rebanada en radianes.

- El **perímetro** de esa rebanada (sector) es:
$$
r\,\theta \;+\; 2r \;=\; 32.
$$

- El **área** de la rebanada es:
$$
A(\theta) \;=\; \tfrac{1}{2}\;r^2\,\theta.
$$

Como \(r\,\theta + 2r = 32\), se deduce \(r = \frac{32}{\theta + 2}\).  
Por tanto, el área se puede escribir en función de \(\theta\) únicamente:
$$
A(\theta) \;=\;
\tfrac12 \left(\frac{32}{\theta + 2}\right)^2 \theta
\;=\;
\frac{512\,\theta}{(\theta + 2)^2}.
$$

El **objetivo** es hallar el valor de \(\theta\) que **maximiza** \(A(\theta)\).  
La derivada lleva a \(\theta = 2\ \text{rad}\).  
Así, el radio resulta ser \(r=8\) y el **diámetro** de la pizza, \(D=16\) (todo en cm).
""",
    unsafe_allow_html=False
)

# ===============================================
# SECCIÓN INTERACTIVA
# ===============================================
st.header("2. Interactúa con el Ángulo θ")

st.write(
    "Puedes usar el deslizador para elegir un ángulo \\(\\theta\\) y ver "
    "cómo cambian el **radio**, el **diámetro** y el **área** de la rebanada, "
    "bajo la restricción de que el perímetro debe ser 32 cm."
)

theta = st.slider(
    "Ángulo (θ, en radianes):",
    min_value=0.01,
    max_value=6.28,
    step=0.01,
    value=2.00
)

# Cálculo del radio a partir de la condición r*(theta + 2) = 32
r_calc = PERIM_FIXED / (theta + 2)

if r_calc <= 0:
    st.error("Para este valor de θ, el radio calculado no es positivo. Elige otro θ.")
else:
    area_val = area_slice(theta, r_calc)
    diameter_val = 2 * r_calc

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Radio (r)", f"{r_calc:.2f} cm")
    with col2:
        st.metric("Diámetro (D)", f"{diameter_val:.2f} cm")
    with col3:
        st.metric("Área del sector", f"{area_val:.2f} cm²")

# ===============================================
# GRÁFICA DEL ÁREA EN FUNCIÓN DE θ
# ===============================================
st.subheader("Gráfica: Área vs. θ (0 < θ ≤ 2π)")

theta_vals = np.linspace(0.01, 6.28, 300)  # de 0.01 a ~ 2π
r_vals = PERIM_FIXED / (theta_vals + 2)
area_vals = 0.5 * r_vals**2 * theta_vals

fig, ax = plt.subplots(figsize=(6,4))
ax.plot(theta_vals, area_vals, label="Área A(θ)")
ax.set_xlabel(r"Ángulo θ (rad)")
ax.set_ylabel(r"Área de la rebanada (cm²)")
ax.set_title("A(θ) = (1/2) * [r(θ)]^2 * θ,   con   r(θ)·(θ+2) = 32 cm")
ax.grid(True)

# Punto máximo teórico (θ=2)
theta_opt = 2.0
r_opt = PERIM_FIXED/(theta_opt + 2.0)  # = 8
area_opt = 0.5 * (r_opt**2) * theta_opt

ax.axvline(theta_opt, color="red", linestyle="--", label="θ óptimo = 2 rad")
ax.plot(theta_opt, area_opt, 'ro')

# Punto actual según slider
if r_calc > 0:
    curr_area = 0.5 * (r_calc**2) * theta
    ax.plot(theta, curr_area, 'go', label="θ actual")

ax.legend()

st.pyplot(fig)

st.markdown(
    r"""
**Observaciones**:
- La línea roja discontinua marca el **ángulo óptimo** \(\theta=2\) rad, 
  donde el área se maximiza. Esto da \(r=8\) cm y, por ende, 
  el **diámetro** \(D=16\) cm.
- El punto verde representa el **valor actual** del ángulo 
  que has elegido en el deslizador, y la respectiva área.
"""
)

st.write("---")
st.write(
    "Cuando \\(\\theta=2\\) rad, la rebanada es maximal en área: "
    "**diámetro = 16 cm**."
)
