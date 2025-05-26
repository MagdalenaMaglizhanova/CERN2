import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("🔬 3D Симулация на сблъсък на частици")

# Параметри
num_frames = 50
r = 0.2  # радиус на частиците
x1 = np.linspace(-5, 0, num_frames)
x2 = np.linspace(5, 0, num_frames)
y1 = np.zeros(num_frames)
y2 = np.zeros(num_frames)
z1 = np.zeros(num_frames)
z2 = np.zeros(num_frames)

frames = []
for i in range(num_frames):
    frames.append(go.Frame(
        data=[
            go.Scatter3d(
                x=[x1[i]], y=[y1[i]], z=[z1[i]],
                mode='markers',
                marker=dict(size=10, color='blue'),
                name='Частица 1'
            ),
            go.Scatter3d(
                x=[x2[i]], y=[y2[i]], z=[z2[i]],
                mode='markers',
                marker=dict(size=10, color='red'),
                name='Частица 2'
            )
        ]
    ))

fig = go.Figure(
    data=frames[0].data,
    layout=go.Layout(
        width=700,
        height=500,
        scene=dict(
            xaxis=dict(range=[-6, 6]),
            yaxis=dict(range=[-1, 1]),
            zaxis=dict(range=[-1, 1])
        ),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="▶️ Пусни", method="animate", args=[None])]
        )]
    ),
    frames=frames
)

st.plotly_chart(fig)
