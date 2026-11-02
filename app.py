import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Vending Machine Intelligent Management",
    page_icon="🤖",
    layout="wide"
)

# Guardar estado de autenticação
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

def fazer_login(usuario, senha):
    # Credenciais fixas solicitadas: utilizador "admin"
    if usuario == "admin" and senha == "1234":
        st.session_state.autenticado = True
        st.success("Login efetuado com sucesso!")
        st.rerun()
    else:
        st.error("Utilizador ou senha incorretos.")

def fazer_logout():
    st.session_state.autenticado = False
    st.rerun()

# ---------------------------------------------------------
# BARRA LATERAL (Navegação & Login do Gestor)
# ---------------------------------------------------------
st.sidebar.title("🤖 Vending Machine")

if not st.session_state.autenticado:
    st.sidebar.subheader("🔑 Área do Gestor")
    with st.sidebar.form("form_login_gestor"):
        user_input = st.text_input("Utilizador", value="admin")
        pass_input = st.text_input("Senha", type="password")
        submit_btn = st.form_submit_button("Entrar como Gestor")
        
        if submit_btn:
            fazer_login(user_input, pass_input)
else:
    st.sidebar.success("Sessão Ativa: **admin**")
    if st.sidebar.button("Terminar Sessão (Logout)"):
        fazer_logout()

# Seleção de Modo
modo = st.sidebar.radio(
    "Navegação:",
    ["🛒 Modo Cliente (Comprar)", "📊 Painel do Gestor"]
)

# ---------------------------------------------------------
# VISÃO 1: MODO CLIENTE (Sem necessidade de login)
# ---------------------------------------------------------
if modo == "🛒 Modo Cliente (Comprar)":
    st.title("🥤 Máquina de Vendas - Comprar Produto")
    st.write("Escolha o seu produto e simule a compra abaixo:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🥤 Coca-Cola")
        st.write("Preço: R$ 5,00")
        st.write("Stock: 10 unid.")
        if st.button("Comprar Coca-Cola"):
            st.success("Produto dispensado com sucesso!")
            
    with col2:
        st.subheader("🍫 Chocolate")
        st.write("Preço: R$ 4,00")
        st.write("Stock: 8 unid.")
        if st.button("Comprar Chocolate"):
            st.success("Produto dispensado com sucesso!")

    with col3:
        st.subheader("💧 Água Mineral")
        st.write("Preço: R$ 3,00")
        st.write("Stock: 15 unid.")
        if st.button("Comprar Água"):
            st.success("Produto dispensado com sucesso!")

# ---------------------------------------------------------
# VISÃO 2: PAINEL DO GESTOR (Protegido por Login)
# ---------------------------------------------------------
elif modo == "📊 Painel do Gestor":
    if not st.session_state.autenticado:
        st.warning("🔒 Acesso Restrito! Utilize a barra lateral à esquerda para fazer login com o utilizador **admin**.")
    else:
        st.title("📊 Painel Administrativo de Gestão")
        st.write("Gestor ativo: **admin**")
        
        st.divider()
        st.subheader("📈 Resumo de Vendas e Inventário")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Vendido", "R$ 150,00")
        c2.metric("Produtos em Stock", "33 unid.")
        c3.metric("Lucro Líquido", "R$ 45,00")
        
        st.divider()
        st.subheader("⚙️ Reposição de Stock")
        st.selectbox("Selecione o produto a reabastecer:", ["Coca-Cola", "Chocolate", "Água Mineral"])
        st.number_input("Quantidade a adicionar:", min_value=1, max_value=50, value=10)
        if st.button("Atualizar Stock"):
            st.success("Stock atualizado no sistema com sucesso!")
