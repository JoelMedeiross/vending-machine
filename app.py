# app.py
import streamlit as st
from model.vending_model import VendingModel
from controller.vending_controller import VendingController
from view.vending_view import VendingView

st.set_page_config(page_title="Vending Machine MVC", layout="wide")

# Instancia as camadas do MVC
model = VendingModel()
controller = VendingController(model)
view = VendingView()

# Inicializa session_state com o Model
if 'transacoes' not in st.session_state:
    st.session_state.transacoes = model.get_transacoes_iniciais()

if 'estoque_produtos' not in st.session_state:
    st.session_state.estoque_produtos = model.get_estoque_inicial()

# Executa a navegação da View
menu = view.render_sidebar()

if menu == "Visão do Cliente (Simulador)":
    view.render_cliente_view(st.session_state, controller)
else:
    analise = model.calcular_ponto_de_pedido(st.session_state.transacoes, st.session_state.estoque_produtos)
    view.render_gestor_view(st.session_state, analise, controller)