import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Симулация: Сблъсък на частици", layout="centered")
st.title("💥 3D Симулация на сблъсък на частици")

st.markdown("Наблюдавай движението на частиците в 3D пространство и отговори на въпроса в края.")

# Параметри на сблъсъка
num_frames = 50
x1 = np.linspace(-5, 0, num_frames)
x2 = np.linspace(5, 0, num_frames)
y = np.zeros(num_frames)
z = np.zeros(num_frames)

# След сблъсъка (разделяне в различни посоки)
x1_after = np.linspace(0, 2, num_frames)
x2_after = np.linspace(0, -2, num_frames)
z1_after = np.linspace(0, 2, num_frames)
z2_after = np.linspace(0, -2, num_frames)

frames = []
for i in range(num_frames):
    x1_val = x1[i] if i < num_frames//2 else x1_after[i - num_frames//2]
    z1_val = 0 if i < num_frames//2 else z1_after[i - num_frames//2]
    x2_val = x2[i] if i < num_frames//2 else x2_after[i - num_frames//2]
    z2_val = 0 if i < num_frames//2 else z2_after[i - num_frames//2]

    frames.append(go.Frame(data=[
        go.Scatter3d(x=[x1_val], y=[0], z=[z1_val], mode='markers',
                     marker=dict(size=10, color='blue'), name='Частица 1'),
        go.Scatter3d(x=[x2_val], y=[0], z=[z2_val], mode='markers',
                     marker=dict(size=10, color='red'), name='Частица 2'),
    ]))

fig = go.Figure(
    data=frames[0].data,
    layout=go.Layout(
        width=700, height=500,
        scene=dict(xaxis=dict(range=[-6, 6]), yaxis=dict(range=[-1, 1]), zaxis=dict(range=[-3, 3])),
        title="Движение на частиците",
        updatemenus=[dict(type="buttons", showactive=False,
                          buttons=[dict(label="▶️ Пусни симулацията", method="animate", args=[None])])]
    ),
    frames=frames
)

st.plotly_chart(fig)

st.subheader("🧠 Въпрос: Какво се запазва при еластичен сблъсък?")
answer = st.radio("Избери верния отговор:", [
    "Само скоростите",
    "Само енергията",
    "Импулсът и кинетичната енергия",
    "Масата се удвоява"
])

if st.button("Изпрати отговор"):
    if answer == "Импулсът и кинетичната енергия":
        st.success("✅ Правилно! Това се запазва при еластичен сблъсък.")
    else:
        st.error("❌ Не е вярно. При еластичен сблъсък се запазва импулсът и кинетичната енергия.")

st.markdown("---")
st.markdown("📚 ЦЕРН изследва сблъсъци на частици с висока енергия, за да открие нови елементарни частици и да разбере по-добре Вселената.")
