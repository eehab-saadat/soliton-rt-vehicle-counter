import streamlit as st

def handle_show_vid() -> None:
    st.session_state.display_checkbox = not st.session_state.display_checkbox
    st.session_state.current_layout = "centered" if st.session_state.current_layout == "wide" else "wide" 