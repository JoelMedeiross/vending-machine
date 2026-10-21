# view/vending_view.py
import streamlit as st

class VendingView:
    def render_sidebar(self):
        st.sidebar.title("📌 Navegação do Sistema (MVC)")
        return st.sidebar.radio(
            "Selecione o Módulo:", 
            ["Visão do Cliente (Simulador)", "Visão do Gestor (Dashboard)"]
        )

    def render_cliente_view(self, session_state, controller):
        st.title("🛒 Simulador de Compras - Vending Machine")
        df_est = session_state.estoque_produtos
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Selecione seu Produto")
            produto_escolhido = st.selectbox("Produto:", df_est['produto'].tolist())
            quantidade = st.number_input("Quantidade:", min_value=1, max_value=5, value=1)
            
            preco_unit = df_est.loc[df_est['produto'] == produto_escolhido, 'preco_unitario'].values[0]
            st.info(f"Preço Unitário: R$ {preco_unit:.2f} | **Total: R$ {preco_unit * quantidade:.2f}**")
            
            if st.button("Confirmar Compra", type="primary"):
                sucesso, msg = controller.realizar_compra(session_state, produto_escolhido, quantidade)
                if sucesso:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")
                    
        with col2:
            st.subheader("📦 Disponibilidade na Máquina")
            st.dataframe(df_est, use_container_width=True)

    def render_gestor_view(self, session_state, analise_estoque, controller):
        st.title("📊 Painel Gerencial (Dashboard & KPIs)")
        
        df_trans = session_state.transacoes
        faturamento_total = (df_trans['quantidade'] * df_trans['preco_unitario']).sum()
        total_vendas = df_trans['quantidade'].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Faturamento Total", f"R$ {faturamento_total:,.2f}")
        col2.metric("📦 Itens Vendidos", int(total_vendas))
        col3.metric("📋 Transações", len(df_trans))
        st.divider()

        st.subheader("⚙️ Controle de Ponto de Pedido e Alertas")
        st.dataframe(analise_estoque, use_container_width=True)

        itens_criticos = analise_estoque[analise_estoque['status_alerta'] == 'CRÍTICO']
        if not itens_criticos.empty:
            for _, row in itens_criticos.iterrows():
                st.error(f"🚨 ALERTA: {row['produto']} em nível crítico! Atual: {row['estoque_atual']} | Ponto de Pedido: {row['ponto_de_pedido']}")
        else:
            st.success("✅ Todos os estoques seguros.")

        st.markdown("### ➕ Reposição de Estoque")
        c1, c2, c3 = st.columns(3)
        with c1:
            prod_rep = st.selectbox("Produto:", analise_estoque['produto'].tolist(), key="rep_p")
        with c2:
            qtd_rep = st.number_input("Qtd:", min_value=1, max_value=50, value=10, key="rep_q")
        with c3:
            st.write("")
            st.write("")
            if st.button("Confirmar Reposição"):
                controller.repor_estoque(session_state, prod_rep, qtd_rep)
                st.success("Estoque atualizado!")
                st.rerun()

        st.markdown("### 📈 Distribuição de Vendas")
        st.bar_chart(df_trans, x='produto', y='quantidade')