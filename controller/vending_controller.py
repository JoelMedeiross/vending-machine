# controller/vending_controller.py
import streamlit as st
from model.vending_model import VendingModel
from view.vending_view import VendingView

class VendingController:
    def __init__(self):
        self.model = VendingModel()
        self.view = VendingView()
        
        if "autenticado" not in st.session_state:
            st.session_state.autenticado = False
        if "df_estoque" not in st.session_state:
            st.session_state.df_estoque = self.model.get_estoque_inicial()
        if "df_trans" not in st.session_state:
            st.session_state.df_trans = self.model.get_transacoes_iniciais()

    def executar(self):
        # Renderiza login na barra lateral
        user, senha, btn_login = self.view.render_sidebar_login()
        if btn_login:
            if self.model.verificar_login(user, senha):
                st.session_state.autenticado = True
                st.session_state.user_logado = user
                st.success("Login efetuado com sucesso!")
                st.rerun()
            else:
                st.error("Utilizador ou senha incorretos.")

        # Seleção de Módulo na Barra Lateral
        modo = st.sidebar.radio(
            "Selecione o Módulo:",
            ["Visão do Cliente (Simulador)", "Visão do Gestor (Dashboard)"]
        )

        if modo == "Visão do Cliente (Simulador)":
            prod, qtd, comprar = self.view.render_cliente(st.session_state.df_estoque)
            if comprar:
                # Atualiza o estoque localmente na sessão
                idx = st.session_state.df_estoque[st.session_state.df_estoque['produto'] == prod].index[0]
                estoque_atual = st.session_state.df_estoque.loc[idx, 'estoque_atual']
                
                if estoque_atual >= qtd:
                    st.session_state.df_estoque.loc[idx, 'estoque_atual'] -= qtd
                    st.success(f"Compra efetuada com sucesso! {qtd}x {prod} dispensados.")
                    st.rerun()
                else:
                    st.error("Quantidade indisponível em estoque!")

        elif modo == "Visão do Gestor (Dashboard)":
            if not st.session_state.autenticado:
                st.warning("🔒 **Acesso Restrito!** Por favor, faça login com o utilizador **admin** na barra lateral à esquerda para aceder ao painel do gestor.")
            else:
                df_analise = self.model.calcular_ponto_de_pedido(
                    st.session_state.df_trans, 
                    st.session_state.df_estoque
                )
                prod, qtd, repor = self.view.render_gestor(df_analise, st.session_state.df_trans)
                if repor:
                    idx = st.session_state.df_estoque[st.session_state.df_estoque['produto'] == prod].index[0]
                    st.session_state.df_estoque.loc[idx, 'estoque_atual'] += qtd
                    st.success(f"Estoque de {prod} reabastecido com sucesso em +{qtd} unidades!")
                    st.rerun()
