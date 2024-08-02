import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_theme import st_theme

@st.cache_data()
def draw_chart(data: pd.DataFrame, theme: dict):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor(theme["backgroundColor"])
    wedges, texts, autotexts = ax.pie(data["counts"], labels=data["class"], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    for text in texts + autotexts:
        text.set_color(theme["textColor"])
    return fig

def render_statistics():
    data = pd.read_csv("counts.csv")
    tabs = st.tabs(["✉️ Table", "📈 Visualization"])

    with tabs[0]:
        st.dataframe(data, use_container_width=True, hide_index=True)

    with tabs[1]:
        
        layout = st.columns(2)

        series = data["counts"].values.tolist()

        with layout[0]:
            theme = st_theme()
            if theme is None:
                theme = {
                    "backgroundColor": "#FFFFFF",
                    "textColor": "#000000"
                }
                
            fig = draw_chart(data, theme)
            st.pyplot(fig)

        with layout[1]:
            st.bar_chart(data, x="class", y="counts")

render_statistics()