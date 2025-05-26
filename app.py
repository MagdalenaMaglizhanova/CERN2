import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("🧪 Симулация на сблъсък на частици с динамична анимация и резултати")

# Входни параметри
col1, col2 = st.columns(2)
with col1:
    m1 = st.number_input("Маса на частица 1 (kg)", min_value=0.1, value=5.0, step=0.1)
    v1 = st.number_input("Начална скорост на частица 1 (m/s)", value=5.0, step=0.1)
with col2:
    m2 = st.number_input("Маса на частица 2 (kg)", min_value=0.1, value=5.0, step=0.1)
    v2 = st.number_input("Начална скорост на частица 2 (m/s)", value=-3.0, step=0.1)

# Изчисляваме крайни скорости при идеален еластичен сблъсък
v1_final = ((m1 - m2) / (m1 + m2)) * v1 + ((2 * m2) / (m1 + m2)) * v2
v2_final = ((2 * m1) / (m1 + m2)) * v1 + ((m2 - m1) / (m1 + m2)) * v2

# Параметри за симулация
x1_start = 0
x2_start = 10
t_total = 4.0  # общо време
frames = 50

t = np.linspace(0, t_total, frames)

# Изчисляваме време на сблъсък (когато x1 и x2 се срещнат)
if v1 == v2:
    t_collision = t_total  # никога не се сблъскват
else:
    t_collision = (x2_start - x1_start) / (v1 - v2)
    if t_collision < 0 or t_collision > t_total:
        t_collision = t_total  # ако сблъсъкът е извън времевия интервал

# Позиции на частиците в 1D (x-ос)
x1_positions = np.zeros_like(t)
x2_positions = np.zeros_like(t)

for i, time in enumerate(t):
    if time <= t_collision:
        x1_positions[i] = x1_start + v1 * time
        x2_positions[i] = x2_start + v2 * time
    else:
        x1_positions[i] = x1_start + v1 * t_collision + v1_final * (time - t_collision)
        x2_positions[i] = x2_start + v2 * t_collision + v2_final * (time - t_collision)

# Създаваме фигура за Plotly 3D (движение само по X, Y=0, Z=0)
frames_list = []
for i in range(frames):
    frame = go.Frame(data=[
        go.Scatter3d(x=[x1_positions[i]], y=[0], z=[0], mode='markers+text',
                     marker=dict(size=12, color='blue'),
                     text=["Частица 1"], textposition="top center"),
        go.Scatter3d(x=[x2_positions[i]], y=[0], z=[0], mode='markers+text',
                     marker=dict(size=12, color='red'),
                     text=["Частица 2"], textposition="top center"),
    ])
    frames_list.append(frame)

fig = go.Figure(
    data=[
        go.Scatter3d(x=[x1_positions[0]], y=[0], z=[0], mode='markers+text',
                     marker=dict(size=12, color='blue'),
                     text=["Частица 1"], textposition="top center"),
        go.Scatter3d(x=[x2_positions[0]], y=[0], z=[0], mode='markers+text',
                     marker=dict(size=12, color='red'),
                     text=["Частица 2"], textposition="top center"),
    ],
    layout=go.Layout(
        scene=dict(
            xaxis=dict(range=[-5, 15], title='Позиция (m)'),
            yaxis=dict(range=[-5, 5], title='Y'),
            zaxis=dict(range=[-5, 5], title='Z'),
        ),
        title="3D Анимация на сблъсък на частици",
        margin=dict(l=0, r=0, b=0, t=40),
        height=500,
        updatemenus=[dict(type="buttons", showactive=False,
                          y=1,
                          x=1.15,
                          xanchor="right",
                          yanchor="top",
                          buttons=[dict(label="▶ Пусни анимацията",
                                        method="animate",
                                        args=[None, {"frame": {"duration": 100, "redraw": True},
                                                     "fromcurrent": True,
                                                     "transition": {"duration": 0}}])])]
    ),
    frames=frames_list
)

st.plotly_chart(fig, use_container_width=True)

# Състояние за показване на резултати
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

if st.button("Покажи резултатите от сблъсъка"):
    st.session_state.show_results = True

if st.session_state.show_results:
    impulse_before = m1 * v1 + m2 * v2
    impulse_after = m1 * v1_final + m2 * v2_final

    energy_before = 0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2
    energy_after = 0.5 * m1 * v1_final ** 2 + 0.5 * m2 * v2_final ** 2

    st.markdown("## Резултати от сблъсъка")
    st.write(f"**Импулс преди сблъсъка:** {impulse_before:.2f} kg·m/s")
    st.write(f"**Импулс след сблъсъка:** {impulse_after:.2f} kg·m/s")
    st.write(f"**Кинетична енергия преди сблъсъка:** {energy_before:.2f} J")
    st.write(f"**Кинетична енергия след сблъсъка:** {energy_after:.2f} J")

    st.markdown("""
    ### Въпроси за размисъл
    - Запазва ли се импулсът?
    - Запазва ли се кинетичната енергия?
    - Как масата и скоростта на частиците влияят на резултата?
    - Какъв тип сблъсък е това (еластичен, нееластичен)?
    """)

    hypothesis = st.text_area("Въведи своя хипотеза за резултата от сблъсъка:")
    if st.button("Изпрати хипотезата"):
        if hypothesis.strip() == "":
            st.warning("Моля, въведи текст за хипотезата си.")
        else:
            st.success("Хипотезата ти е изпратена! Много добре, че мислиш активно!")

