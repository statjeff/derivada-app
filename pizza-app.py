import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def perimeter_slice(theta, r):
    """
    Perímetro de la rebanada (sector) = r*theta + 2*r
    """
    return r*theta + 2*r

def area_slice(theta, r):
    """
    Área de la rebanada (sector) = (1/2) * r^2 * theta
    """
    return 0.5 * r**2 * theta

# Streamlit layout config
st.set_page_config(
    page_title="Pizza Slice with Fixed Perimeter",
    layout="centered",
)

st.title("Rebanada de Pizza con Perímetro Fijo")
st.write(
    "Este ejemplo muestra cómo, dados un perímetro fijo (32 pulgadas) para una "
    "rebanada de pizza (un sector circular), se determina qué **diámetro** maximiza "
    "el área de dicha rebanada."
)

# Perímetro fijo de la rebanada
PERIM_FIXED = 32

st.header("Parámetros y Explicación")
st.markdown(
    """
- Sea \( r \) el radio de la pizza.  
- Sea \( \\theta \) (en radianes) el **ángulo** del sector.  
- El **perímetro** de la rebanada es  
  \[
    r\,\theta + 2r = 32.
  \\]  
- El **área** de ese sector es  
  \\[
    A = \\frac{1}{2}\\,r^2\\,\\theta.
  \\]

La relación del perímetro fijo te da  
\\[
r = \\frac{32}{\\theta + 2}.
\\]

Entonces el área, en función de \\( \\theta \\), se convierte en  
\\[
A(\\theta) = \\frac{1}{2}\\left(\\frac{32}{\\theta + 2}\\right)^2\\theta.
\\]

**Queremos maximizar** \\( A(\\theta) \\) con \\( \\theta > 0 \\).
"""
)

st.header("Explora el área según θ")
st.write(
    "En esta sección, puedes mover el ángulo \\(\\theta\\) e inspeccionar el radio, el diámetro y el área "
    "resultantes, siempre cumpliendo con el perímetro fijo de 32."
)

theta = st.slider("Ángulo (θ, radianes)", min_value=0.1, max_value=6.28, step=0.01, value=2.0)
# Calculamos el radio a partir de la ecuación r*(theta+2)=32
r_calculated = PERIM_FIXED / (theta + 2)

# Evitar r < 0:
if r_calculated <= 0:
    st.warning("Con este valor de θ, el radio resultaría no positivo, lo cual no es factible.")
else:
    # Área resultante
    area_val = area_slice(theta, r_calculated)
    diameter_val = 2 * r_calculated

    st.write(f"**Radio (r):** {r_calculated:.2f} pulgadas")
    st.write(f"**Diámetro (D):** {diameter_val:.2f} pulgadas")
    st.write(f"**Área de la rebanada:** {area_val:.2f} pulgadas²")

# Graficamos A(θ) para un rango de θ
st.subheader("Gráfica del área en función de θ")

theta_vals = np.linspace(0.01, 6.28, 300)  # un rango de 0.01 a ~2π radianes
r_vals = PERIM_FIXED / (theta_vals + 2)
area_vals = 0.5 * (r_vals**2) * theta_vals

fig, ax = plt.subplots(figsize=(6,4))
ax.plot(theta_vals, area_vals, label="A(θ)")
ax.set_xlabel("θ (radianes)")
ax.set_ylabel("Área de la rebanada")
ax.set_title("Área vs. θ (perímetro fijo = 32)")
ax.grid(True)

# Si queremos mostrar la derivada = 0 => θ=2 como punto máximo
theta_opt = 2
r_opt = PERIM_FIXED/(theta_opt + 2)  # = 8
area_opt = 0.5 * (r_opt**2) * theta_opt
ax.axvline(theta_opt, color="red", linestyle="--", label="θ óptimo = 2 rad")
ax.plot(theta_opt, area_opt, "ro")
ax.legend()

st.pyplot(fig)

st.markdown(
    f"""
**Conclusión teórica**  
Al derivar y maximizar el área \\( A(\\theta) \\), se llega a \\( \\theta = 2 \\) radianes.  
Esto da \\( r = 8 \\) pulgadas, luego el **diámetro** \\( D = 16 \\) pulgadas.  
Por tanto, la pizza que te brindará la **rebanada más grande** (para perímetro 32) 
debe tener \\( \\boxed{{16\\text{{ pulgadas de diámetro}}}} \\).
"""
)

st.write("---")
st.write(
    "_¡Prueba mover el deslizador para ver cómo el radio y el área cambian!_  \n"
    "Observa que cuando \\( \\theta \\) se acerca a 2, el área se maximiza."
)
