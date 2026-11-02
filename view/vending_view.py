# view/vending_view.py
import streamlit as st

class VendingView:
    def render_sidebar_login(self):
        st.sidebar.title("📌 Navegação do Sistema")
        st.sidebar.write("Selecione o Módulo:")
        
        # O gestor faz login na barra lateral
        if not st.session_state.get("autenticado", False):
            with st.sidebar.expander("🔑 Acesso Restrito (Gestor)", expanded=True):
                user_input = st.text_input("Utilizador", value="admin")
                pass_input = st.text_input("Senha", type="password")
                submit_btn = st.button("Entrar como Gestor")
                return user_input, pass_input, submit_btn
        else:
            st.sidebar.success(f"Gestor Logado: **{st.session_state.get('user_logado', 'admin')}**")
            if st.sidebar.button("Terminar Sessão"):
                st.session_state.autenticado = False
                st.rerun()
        return "", "", False

    def render_cliente(self, df_estoque):
        st.title("🛒 Simulador de Compras - Vending Machine do Campus")
        st.write("Selecione os itens desejados para simular a compra em tempo real.")
        
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            st.subheader("Selecione seu Produto")
            lista_produtos = df_estoque['produto'].tolist()
            produto_selecionado = st.selectbox("Produto:", lista_produtos)
            
            preco_unitario = df_estoque.loc[df_estoque['produto'] == produto_selecionado, 'preco_unitario'].values[0]
            estoque_disponivel = df_estoque.loc[df_estoque['produto'] == produto_selecionado, 'estoque_atual'].values[0]
            
            quantidade = st.number_input("Quantidade:", min_value=1, max_value=max(int(estoque_disponivel), 1), value=1)
            
            total = preco_unitario * quantidade
            st.info(f"Preço Unitário: R$ {preco_unitario:.2f}  |  **Total a Pagar: R$ {total:.2f}**")
            
            btn_comprar = st.button("Confirmar Compra")

        with col2:
            st.subheader("📦 Disponibilidade Atual na Máquina")
            st.dataframe(df_estoque, hide_index=True, use_container_width=True)
            
        return produto_selecionado, quantidade, btn_comprar

    def render_gestor(self, df_analise, df_trans):
        st.title("📊 Painel de Controle e Gestão de Estoque")
        st.write("Monitoramento de faturamento, fluxo de vendas e cálculo de Ponto de Pedido ($PP$).")
        
        # Métricas superiores
        faturamento_total = (df_trans['quantidade'] * df_trans['preco_unitario']).sum()
        itens_vendidos = df_trans['quantidade'].sum()
        total_trans = len(df_trans)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Faturamento Total", f"R$ {faturamento_total:.2f}")
        c2.metric("Itens Totais Vendidos", f"{itens_vendidos}")
        c3.metric("Transações Registradas", f"{total_trans}")
        
        st.divider()
        st.subheader("⚙️ Controle Estatístico de Estoque e Ponto de Pedido")
        st.dataframe(df_analise, hide_index=True, use_container_width=True)
        
        # Alertas de Reabastecimento
        criticos = df_analise[df_analise['status_alerta'] == 'CRÍTICO']
        if not criticos.empty:
            st.subheader("🚨 Alertas de Reabastecimento Imediato")
            for _, row in criticos.iterrows():
                st.error(f"ALERTA DE STOCKOUT: O produto **{row['produto']}** atingiu nível crítico! Estoque Atual: {row['estoque_atual']} | Ponto de Pedido Mínimo: {row['ponto_de_pedido']}.")
        
        st.divider()
        st.subheader("➕ Repor Estoque (Simulação de Reabastecimento)")
        col_r1, col_r2, col_r3 = st.columns([2, 2, 1])
        with col_r1:
            prod_repor = st.selectbox("Produto para repor:", df_analise['produto'].tolist(), key="repor_prod")
        with col_r2:
            qtd_repor = st.number_input("Quantidade a adicionar:", min_value=1, max_value=50, value=10, key="repor_qtd")
        with col_r3:
            st.write("")
            st.write("")
            btn_repor = st.button("Confirmar Reposição")
            
        st.divider()
        st.subheader("📈 Distribuição de Vendas por Produto")
        vendas_chart = df_trans.groupby('produto')['quantidade'].sum().reset_index()
        st.bar_chart(vendas_chart.set_index('produto'))
        
        return prod_repor, qtd_repor, btn_repor
