import streamlit as st

@st.dialog(title="System Message")
def showDialogBox(icon: any = "⚠️", header: str = "Warning", message: str = "some error occurred. Please try again."):
    st.header(icon + " " + header)
    st.write(message)