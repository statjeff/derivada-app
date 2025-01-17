import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------
# 1. Funciones para el caso ideal (sin resistencia)
# ------------------------------------------------------
def calcular_distancia(v, angulo, g=9.8):
    """
    Calcula la distancia (alcance) para un lanzamiento parabólico
    ideal con velocidad v (m/s), ángulo en grados y gravedad g (m/s^2).
    """
    theta = np.radians(angulo)
    distancia = (v**2 * np.sin(2 * theta)) / g
    return distancia

def calcular_trayectoria(v, angulo, g=9.8, num_points=100):
    """
    Devuelve (x, y) para la trayectoria ideal (sin resistencia).
    """
    theta = np.radians(angulo)
    T = 2 * v * np.sin(theta) / g  # tiempo total de vuelo
    t = np.linspace(0, T, num_points)
    x = v * np.cos(theta) * t
    y = v * np.sin(theta) * t - 0.5 * g * t**2
    return x, y

# ------------------------------------------------------
# 2. Funciones para el caso con resistencia del aire
# ------------------------------------------------------
def calcular_trayectoria_con_drag(v, angulo, k, g=9.8, dt=0.01):
    """
    Calcula la trayectoria (x, y) teniendo en cuenta una fuerza de arrastre
    proporcional a k * v^2.
    
    Utiliza un método de integración numérica sencillo (Euler).
    - v : velocidad inicial (m/s)
    - angulo : ángulo de lanzamiento en grados
    - k : coeficiente de arrastre
    - g : aceleración de la gravedad (m/s^2)
    - dt : paso de tiempo para la integración
    """
    # Convertimos ángulo a radianes
    theta = np.radians(angulo)
    
    # Velocidades iniciales en x e y
    vx = v * np.cos(theta)
    vy = v * np.sin(theta)

    # Posición inicial
    x = 0.0
    y = 0.0

    # Listas para guardar los puntos de la trayectoria
    x_vals = [x]
    y_vals = [y]
    
    # Iteramos mientras la pelota esté por encima de y=0
    while y >= 0:
        # Calculamos la magnitud de la velocidad
        v_mod = np.sqrt(vx**2 + vy**2)
        
        # Aceleración debida al arrastre (dirección opuesta a la velocidad)
        ax_drag = -k * v_mod * vx  
        ay_drag = -k * v_mod * vy
        
        # Aceleraciones totales
        ax = ax_drag
        ay = -g + ay_drag
        
        # Actualizamos velocidades
        vx = vx + ax * dt
        vy = vy + ay * dt
        
        # Actualizamos posiciones
        x = x + vx * dt
        y = y + vy * dt
        
        x_vals.append(x)
        y_vals.append(y)
        
    # Convertimos a arrays
    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)
    
    # Filtrar los valores negativos finales en y (para suavizar la curva)
    # Tomamos solo hasta donde la pelota cae al piso (y >= 0)
    indices_validos = np.where(y_vals >= 0)[0]
    x_vals = x_vals[indices_validos]
    y_vals = y_vals[indices_validos]
    
    return x_vals, y_vals

def calcular_distancia_con_drag(v, angulo, k, g=9.8, dt=0.01):
    """
    Devuelve la distancia alcanzada (último valor de x) con arrastre.
    """
    x_vals, y_vals = calcular_trayectoria_con_drag(v, angulo, k, g, dt)
    return x_vals[-1]  # el último valor de x

# ------------------------------------------------------
# 3. Configuración de la aplicación en Streamlit
# ------------------------------------------------------
st.title("Simulador de Tiro Parabólico con y sin Resistencia del Aire")

st.write("""
Esta aplicación te permite comparar la trayectoria de un balón de fútbol americano
pateado con **velocidad inicial de 20 m/s** y un **ángulo de lanzamiento** entre 
20° y 40°, tanto en el caso ideal (sin resistencia) como con resistencia del aire.
""")

# Parámetros fijos
v_inicial = 20.0   # m/s
g = 9.8            # m/s^2

# 3.1 Selección del ángulo
angulo = st.sidebar.slider(
    "Selecciona el ángulo de lanzamiento (°)",
    min_value=20,
    max_value=40,
    value=30,
    step=1
)

# 3.2 Selección del coeficiente de arrastre k
k = st.sidebar.slider(
    "Selecciona el coeficiente de arrastre (k)",
    min_value=0.0,
    max_value=0.2,
    value=0.05,
    step=0.01
)

st.write(f"**Ángulo seleccionado:** {angulo}°")
st.write(f"**Coeficiente de arrastre seleccionado:** {k:.2f}")

# ------------------------------------------------------
# 4. Cálculos y Gráficas
# ------------------------------------------------------

# 4.1 Trayectoria ideal (sin drag)
x_ideal, y_ideal = calcular_trayectoria(v_inicial, angulo, g)

# 4.2 Trayectoria con drag
x_drag, y_drag = calcular_trayectoria_con_drag(v_inicial, angulo, k, g, dt=0.01)

# 4.3 Distancias alcanzadas
distancia_ideal = calcular_distancia(v_inicial, angulo, g)
distancia_con_drag = x_drag[-1]  # último valor de la lista en x_drag

# Crear la figura
fig, ax = plt.subplots(figsize=(6, 4))

# Graficar trayectoria ideal
ax.plot(x_ideal, y_ideal, label="Trayectoria ideal (sin drag)")

# Graficar trayectoria con drag
ax.plot(x_drag, y_drag, label=f"Trayectoria con drag (k={k:.2f})")

ax.set_xlabel("Distancia (m)")
ax.set_ylabel("Altura (m)")
ax.set_title("Comparación de Trayectorias")
ax.grid(True)
ax.legend()

# Mostrar la gráfica en Streamlit
st.pyplot(fig)

# Resultados numéricos
st.write(f"**Distancia sin resistencia:** {distancia_ideal:.2f} m")
st.write(f"**Distancia con resistencia:** {distancia_con_drag:.2f} m")

# ------------------------------------------------------
# 5. Hallar la distancia máxima en el rango de ángulos [20°, 40°]
#    tanto sin drag como con drag
# ------------------------------------------------------
angulos = np.linspace(20, 40, 200)
distancias_ideales = [calcular_distancia(v_inicial, a, g) for a in angulos]
distancias_drag = [calcular_distancia_con_drag(v_inicial, a, k, g) for a in angulos]

distancia_maxima_ideal = max(distancias_ideales)
angulo_max_ideal = angulos[np.argmax(distancias_ideales)]

distancia_maxima_drag = max(distancias_drag)
angulo_max_drag = angulos[np.argmax(distancias_drag)]

st.write("---")
st.write("### Máximos en el rango de ángulos (20° - 40°)")

col1, col2 = st.columns(2)

with col1:
    st.write("#### Caso Ideal (sin drag)")
    st.write(f"**Distancia máxima:** {distancia_maxima_ideal:.2f} m")
    st.write(f"**Ángulo óptimo:** {angulo_max_ideal:.2f}°")

with col2:
    st.write(f"#### Caso con Drag (k={k:.2f})")
    st.write(f"**Distancia máxima:** {distancia_maxima_drag:.2f} m")
    st.write(f"**Ángulo óptimo:** {angulo_max_drag:.2f}°")

# ------------------------------------------------------
# 6. Explicación
# ------------------------------------------------------
st.write("""
---
### Explicación de los resultados

1. **Caso Ideal (sin resistencia)**  
   El alcance se calcula mediante la fórmula:
   \[
   R = \frac{v^2 \sin(2\theta)}{g},
   \]
   y, sin restricciones, el ángulo óptimo sería 45°. Pero en nuestro rango limitado (20° a 40°), el máximo se da generalmente cerca de 40°, porque a mayor ángulo (en ese rango) mayor componente vertical, y por lo tanto mayor tiempo de vuelo.

2. **Caso con Resistencia del Aire**  
   El arrastre (drag) reduce la velocidad horizontal del balón conforme avanza.  
   - La aceleración en cada eje se ve afectada por un término proporcional a \(-k \|\mathbf{v}\| \cdot \mathbf{v}\).  
   - Esto hace que la velocidad horizontal disminuya más rápido y, por consiguiente, la distancia recorrida sea menor comparada con el caso ideal.

3. **Comparación y conclusiones**  
   - Al aumentar el valor de **k** (coeficiente de arrastre), se evidencia una mayor pérdida de velocidad durante la trayectoria, resultando en un alcance más corto.  
   - En la práctica, siempre existe algo de resistencia del aire, por lo que la distancia real estará por debajo de la ideal.  
   - En rangos de ángulos limitados, es común que el ángulo más alto del intervalo sea el que proporcione mayor alcance, aunque el arrastre puede cambiar ligeramente este ángulo óptimo.

¡Prueba modificando el ángulo y el coeficiente de arrastre en la barra lateral para observar cómo cambian las trayectorias y distancias!
""")
