import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("Gráficas: círculo, elipse y línea")

figura = st.selectbox("Elige qué graficar", ["Círculo", "Elipse", "Línea", "Todas"])

t = np.linspace(0, 2 * np.pi, 400)
fig, ax = plt.subplots(figsize=(6, 6))

if figura in ("Círculo", "Todas"):
    st.sidebar.subheader("Círculo")
    r = st.sidebar.slider("Radio", 1.0, 10.0, 3.0, 0.5)
    ax.plot(r * np.cos(t), r * np.sin(t), label="Círculo")

if figura in ("Elipse", "Todas"):
    st.sidebar.subheader("Elipse")
    a = st.sidebar.slider("Semieje a (horizontal)", 1.0, 10.0, 5.0, 0.5)
    b = st.sidebar.slider("Semieje b (vertical)", 1.0, 10.0, 2.0, 0.5)
    ax.plot(a * np.cos(t), b * np.sin(t), label="Elipse")

if figura in ("Línea", "Todas"):
    st.sidebar.subheader("Línea")
    m = st.sidebar.slider("Pendiente (m)", -5.0, 5.0, 0.5, 0.1)
    c = st.sidebar.slider("Intercepto (b)", -10.0, 10.0, 1.0, 0.5)
    x = np.linspace(-10, 10, 100)
    ax.plot(x, m * x + c, label="Línea")

ax.set_aspect("equal", adjustable="datalim")
ax.axhline(0, color="gray", linewidth=0.5)
ax.axvline(0, color="gray", linewidth=0.5)
ax.grid(True)
ax.legend()
ax.set_title(figura)

st.pyplot(fig)
