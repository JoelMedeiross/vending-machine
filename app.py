# app.py
import streamlit as st
from controller.vending_controller import VendingController

st.set_page_config(
    page_title="Sistema Inteligente de Vending Machine",
    page_icon="🤖",
    layout="wide"
)

if __name__ == "__main__":
    controller = VendingController()
    controller.executar()
