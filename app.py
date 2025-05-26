import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.markdown("## 🧪 3D Симулация на сблъсък")

m1, v1 = 5.0, 5.0
m2, v2 = 5.0, -3.0

v1_final = ((m1 - m2)/(m1 + m2)) * v1 + ((2 * m2)/(m1 + m2)) * v2
v2_final = ((2 * m1)/(m1 + m2)) * v1 + ((m2 - m1)/(m1 + m2)) * v2

# времеви интервал
t = np.linspace(0, 2, 30)
x1 = v1 * t
x2 = 10 + v2 * t

frames = []
for i in range(len(t)):
    frames.append(go.Frame(data=[
        go.Scatter3d(x=[x1[i]], y=[0], z=[0], mode='markers+text',
                     marker=dict(size=10, color='blue'),
                     text=["Частица 1"], textposition="top center"),
        go.Scatter3d(x=[x2[i]], y=[0], z=[0], mode='markers+text',
                     marker=dict(size=10, color='red'),
                     text=["Частица 2"], textposition="top center")
    ]))

layout = go.Layout(
    scene=dict(
        xaxis=dict(range=[-10, 30], title='Позиция X'),
        yaxis=dict(range=[-5, 5], title='Y'),
        zaxis=dict(range=[-5, 5], title='Z'),
    ),
    title="3D Анимация на сблъсък",
    margin=dict(l=0, r=0, b=0, t=40),
    height=500,
    updatemenus=[dict(type="buttons", showactive=False,
                      buttons=[dict(label="▶ Пусни",
                                    method="animate",
                                    args=[None, {"frame": {"duration": 100, "redraw": True},
                                                 "fromcurrent": True}])])]
)

fig = go.Figure(
    data=[
        go.Scatter3d(x=[x1[0]], y=[0], z=[0], mode='markers', marker=dict(size=10, color='blue')),
        go.Scatter3d(x=[x2[0]], y=[0], z=[0], mode='markers', marker=dict(size=10, color='red'))
    ],
    layout=layout,
    frames=frames
)

st.plotly_chart(fig)
