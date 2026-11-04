# model/vending_model.py
import pandas as pd
import os

class VendingModel:
    def __init__(self):
        self.csv_path = "dados_vending.csv"
        self.admin_csv_path = "dados_admin.csv"
        self.garantir_ficheiros_existem()

    def garantir_ficheiros_existem(self):
        """Garante que os ficheiros de dados locais existem na raiz do projeto."""
        # Cria o CSV de produtos se não existir
        if not os.path.exists(self.csv_path):
            df_inicial = pd.DataFrame({
                "produto": ["Água", "Refrigerante", "Salgado", "Chocolate"],
                "estoque_atual": [12, 3, 15, 2],
                "preco_unitario": [4.00, 6.00, 8.00, 5.00]
            })
            df_inicial.to_csv(self.csv_path, index=False)
            
        # Cria o CSV de credenciais do gestor separadamente (fora do código Python)
        if not os.path.exists(self.admin_csv_path):
            df_admin = pd.DataFrame({
                "usuario": ["admin"],
                "senha": ["1234"]
            })
            df_admin.to_csv(self.admin_csv_path, index=False)

    def verificar_login(self, usuario, senha):
        #Verifica o login consultando o ficheiro CSV externo, sem dados fixos no código.
        try:
            if os.path.exists(self.admin_csv_path):
                df_admin = pd.read_csv(self.admin_csv_path)
                match = df_admin[(df_admin['usuario'] == usuario) & (df_admin['senha'] == senha)]
                return not match.empty
        except Exception:
            pass
        return False

    def get_estoque_inicial(self):
        #Lê os dados de stock diretamente da base de dados local em CSV.
        try:
            return pd.read_csv(self.csv_path)
        except Exception:
            return pd.DataFrame({
                "produto": ["Água", "Refrigerante", "Salgado", "Chocolate"],
                "estoque_atual": [12, 3, 15, 2],
                "preco_unitario": [4.00, 6.00, 8.00, 5.00]
            })

    def atualizar_estoque(self, produto_escolhido, qtd_comprada):
        #Atualiza o stock após uma compra e persiste os dados no ficheiro CSV local.
        df = self.get_estoque_inicial()
        if produto_escolhido in df['produto'].values:
            df.loc[df['produto'] == produto_escolhido, 'estoque_atual'] -= qtd_comprada
            df.loc[df['estoque_atual'] < 0, 'estoque_atual'] = 0
            df.to_csv(self.csv_path, index=False)

    def get_transacoes_iniciais(self):
        #Histórico de transações simulado para alimentar os gráficos do gestor.
        return pd.DataFrame({
            "timestamp": pd.date_range(start="2026-10-01", periods=20, freq="h"),
            "produto": ["Água", "Refrigerante", "Salgado", "Chocolate"] * 5,
            "quantidade": [1, 2, 1, 1] * 5,
            "preco_unitario": [4.00, 6.00, 8.00, 5.00] * 5
        })

    def calcular_ponto_de_pedido(self, df_trans, df_est, lead_time=2, estoque_seguranca=3):
        #Calcula o Ponto de Pedido (PP) e gera os alertas de stock crítico.
        vendas_agrupadas = df_trans.groupby('produto')['quantidade'].sum().reset_index()
        analise = df_est.merge(vendas_agrupadas, on='produto', how='left').fillna(0)
        analise['consumo_diario'] = analise['quantidade'] / 30
        analise['ponto_de_pedido'] = (
            (analise['consumo_diario'] * lead_time) + estoque_seguranca
        ).round().astype(int)
        
        analise['status_alerta'] = analise.apply(
            lambda row: 'CRÍTICO' if row['estoque_atual'] <= row['ponto_de_pedido'] else 'REGULAR', 
            axis=1
        )
        return analise