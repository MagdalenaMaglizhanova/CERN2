import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Физика: Сблъсък и импулс", layout="centered")
st.title("💥 Симулация на сблъсък: Импулс и Енергия")

st.markdown("## 1. Параметри на частиците")
m1 = st.number_input("Маса на частица 1 (kg)", 1.0, 10.0, 2.0)
v1 = st.number_input("Начална скорост на частица 1 (m/s)", -10.0, 10.0, 5.0)
m2 = st.number_input("Маса на частица 2 (kg)", 1.0, 10.0, 2.0)
v2 = st.number_input("Начална скорост на частица 2 (m/s)", -10.0, 10.0, -3.0)

# Изчисления след еластичен сблъсък
v1_final = (m1 - m2) / (m1 + m2) * v1 + (2 * m2) / (m1 + m2) * v2
v2_final = (m2 - m1) / (m1 + m2) * v2 + (2 * m1) / (m1 + m2) * v1

# Импулси и енергии
p1_i = m1 * v1
p2_i = m2 * v2
p_total_i = p1_i + p2_i

p1_f = m1 * v1_final
p2_f = m2 * v2_final
p_total_f = p1_f + p2_f

k1_i = 0.5 * m1 * v1**2
k2_i = 0.5 * m2 * v2**2
k_total_i = k1_i + k2_i

k1_f = 0.5 * m1 * v1_final**2
k2_f = 0.5 * m2 * v2_final**2
k_total_f = k1_f + k2_f

# Визуализация с plotly
frames = []
x1_start = np.linspace(-5, 0, 50)
x2_start = np.linspace(5, 0, 50)
x1_after = np.linspace(0, v1_final, 50)
x2_after = np.linspace(0, v2_final, 50)

for i in range(50):
    x1 = x1_start[i] if i < 25 else x1_after[i - 25]
    x2 = x2_start[i] if i < 25 else x2_after[i - 25]
    frames.append(go.Frame(data=[
        go.Scatter(x=[x1], y=[0], mode='markers', marker=dict(size=20, color='blue'), name='Частица 1'),
        go.Scatter(x=[x2], y=[0], mode='markers', marker=dict(size=20, color='red'), name='Частица 2')
    ]))

fig = go.Figure(
    data=frames[0].data,
    layout=go.Layout(
        title="Движение по оста X",
        xaxis=dict(range=[-10, 10]),
        yaxis=dict(range=[-1, 1]),
        updatemenus=[dict(type="buttons", buttons=[
            dict(label="▶️ Пусни симулацията", method="animate", args=[None])
        ])]
    ),
    frames=frames
)

st.markdown("## 2. Симулация")
st.plotly_chart(fig)

st.markdown("## 3. Резултати от сблъсъка")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔹 Преди сблъсъка:")
    st.write(f"Импулс 1: {p1_i:.2f} kg·m/s")
    st.write(f"Импулс 2: {p2_i:.2f} kg·m/s")
    st.write(f"Общ импулс: {p_total_i:.2f} kg·m/s")
    st.write(f"Кинетична енергия: {k_total_i:.2f} J")

with col2:
    st.markdown("### 🔸 След сблъсъка:")
    st.write(f"Импулс 1: {p1_f:.2f} kg·m/s")
    st.write(f"Импулс 2: {p2_f:.2f} kg·m/s")
    st.write(f"Общ импулс: {p_total_f:.2f} kg·m/s")
    st.write(f"Кинетична енергия: {k_total_f:.2f} J")

if round(p_total_i, 2) == round(p_total_f, 2):
    st.success("✅ Законът за запазване на импулса е спазен.")
else:
    st.error("❌ Има разлика в импулса.")

if round(k_total_i, 2) == round(k_total_f, 2):
    st.info("ℹ️ Кинетичната енергия се е запазила – сблъсъкът е еластичен.")
else:
    st.warning("⚠️ Има загуба на енергия – възможно нееластичен сблъсък.")

