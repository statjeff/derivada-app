import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constantes físicas
h = 6.626e-34  # Constante de Planck (Joule·s)
c = 3.0e8       # Velocidad de la luz (m/s)
k_B = 1.38e-23  # Constante de Boltzmann (Joule/K)

# Función de distribución de Planck
def planck(wavelength, temperature):
    """
    Calcula la radiancia espectral usando la ley de Planck.
    :param wavelength: Longitud de onda (m)
    :param temperature: Temperatura (K)
    :return: Radiancia espectral (W·sr⁻¹·m⁻³)
    """
    return (2 * h * c**2 / wavelength**5) / (np.exp(h * c / (wavelength * k_B * temperature)) - 1)

# Configuración de la aplicación
st.title("Ley de Planck: Radiación del Cuerpo Negro")
st.write("Explora cómo la radiación de un cuerpo negro varía con la temperatura y la longitud de onda.")

# Entrada de temperatura
st.sidebar.header("Parámetros")
temperature = st.sidebar.slider("Temperatura del cuerpo negro (K)", min_value=1000, max_value=10000, value=5000, step=100)

# Rango de longitud de onda
wavelength_min = st.sidebar.number_input("Longitud de onda mínima (nm)", min_value=1, max_value=1000, value=100)
wavelength_max = st.sidebar.number_input("Longitud de onda máxima (nm)", min_value=1, max_value=3000, value=2000)

# Verifica que los valores sean válidos
if wavelength_min >= wavelength_max:
    st.error("La longitud de onda mínima debe ser menor que la máxima.")
else:
    # Conversión a metros
    wavelengths = np.linspace(wavelength_min, wavelength_max, 500) * 1e-9

    # Cálculo de la radiancia espectral
    radiance = planck(wavelengths, temperature)

    # Gráfica de la radiancia espectral
    plt.figure(figsize=(10, 6))
    plt.plot(wavelengths * 1e9, radiance, label=f"T = {temperature} K")
    plt.title("Espectro de radiación del cuerpo negro")
    plt.xlabel("Longitud de onda (nm)")
    plt.ylabel("Radiancia espectral (W·sr⁻¹·m⁻³)")
    plt.grid(True)
    plt.legend()
    st.pyplot(plt)

    # Máximo de emisión según la ley de Wien
    wavelength_peak = 2.898e-3 / temperature  # Máxima emisión en metros
    st.write(f"El pico de emisión ocurre en aproximadamente {wavelength_peak * 1e9:.2f} nm (Ley de Wien).")

    # Explicación de la física detrás
    st.header("Física detrás del problema del cuerpo negro")
    st.write(
        "La radiación del cuerpo negro es la emisión de radiación electromagnética por un objeto en equilibrio térmico. "
        "La distribución de la intensidad de esta radiación depende únicamente de la temperatura del objeto."
    )
    st.write(
        "La ley de Planck describe esta distribución, y su fórmula es:"
    )
    st.latex(r"B_\lambda(T) = \frac{2hc^2}{\lambda^5} \frac{1}{e^{\frac{hc}{\lambda k_B T}} - 1}")
    st.write(
        "Donde:\n"
        "- \(B_\lambda(T)\): Radiancia espectral (W·sr⁻¹·m⁻³).\n"
        "- \(h\): Constante de Planck.\n"
        "- \(c\): Velocidad de la luz.\n"
        "- \(k_B\): Constante de Boltzmann.\n"
        "- \(\lambda\): Longitud de onda.\n"
        "- \(T\): Temperatura absoluta (K)."
    )
    st.write(
        "La ley de Wien nos indica la longitud de onda a la que ocurre la emisión máxima, según:"
    )
    st.latex(r"\lambda_{\text{máx}} = \frac{2.898 \times 10^{-3}}{T}")
    st.write(
        "Esta fórmula permite entender cómo objetos más calientes emiten radiación con picos a longitudes de onda más cortas, "
        "como la luz visible o ultravioleta."
    )
