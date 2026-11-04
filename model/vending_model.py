# model/vending_model.py
import pandas as pd
import os
import hashlib

class VendingModel:
    def __init__(self):
        self.csv_path = "dados_vending.csv"
        self.admin_csv_path = "dados_admin.csv"
        self.garantir_ficheiros_existem()

    def garantir_ficheiros_existem(self):
        """Garante que os ficheiros de dados locais existem na raiz do projeto."""
        if not os.path.exists(self.csv_path):
            df_inicial = pd.DataFrame({
                "produto": ["Água", "Refrigerante", "Salgado", "Chocolate"],
                "estoque_atual": [12, 3, 15, 2],
                "preco_unitario": [4.00, 6.00, 8.00, 5.00]
            })
            df_inicial.to_csv(self.csv_path, index=False)
            
        # Cria apenas a estrutura vazia para o admin, SEM NENHUMA SENHA NO CÓDIGO
        if not os.path.exists(self.admin_csv_path):
            df_admin = pd.DataFrame(columns=["usuario", "senha"])
            df_admin.to_csv(self.admin_csv_path, index=False)

    def verificar_login(self, usuario, senha):
        """Verifica o login comparando o hash da senha introduzida com o hash guardado no ficheiro local."""
        try:
            if os.path.exists(self.admin_csv_path):
                df_admin = pd.read_csv(self.admin_csv_path)
                if df_admin.empty:
                    return False
                
                # Cifra a palavra-passe introduzida para comparar com a que tens guardada no teu PC
                senha_digitada_cifrada = hashlib.sha256(senha.encode()).hexdigest()
                
                match = df_admin[
                    (df_admin['usuario'] == usuario) & 
                    (df_admin['senha'] == senha_digitada_cifrada)
                ]
                return not match.empty
        except Exception:
            pass
        return False

    def get_estoque_inicial(self):
        try:
            return pd.read_csv(self.csv_path)
        except Exception:
            return pd.DataFrame({
                "produto": ["Água", "Refrigerante", "Salgado", "Chocolate"],
                "estoque_atual": [12, 3, 15, 2],
                "preco_unitario": [4.00, 6.00, 8.00, 5.00]
            })

    def atualizar_estoque(self, produto_escolhido, qtd_comprada):
        df = self.get_estoque_inicial()
        if produto_escolhido in df['produto'].values:
            df.loc[df['produto'] == produto_escolhido, 'estoque_atual'] -= qtd_comprada
            df.loc[df['estoque_atual'] < 0, 'estoque_atual'] = 0
            df.to_csv(self.csv_path, index=False)

    def get_transacoes_iniciais(self):
        return pd.DataFrame({
            "timestamp": pd.date_range(start="2026-10-01", periods=20, freq="h"),
            "produto": ["Água", "Refrigerante", "Salgado", "Chocolate"] * 5,
            "quantidade": [1, 2, 1, 1] * 5,
            "preco_unitario": [4.00, 6.00, 8.00, 5.00] * 5
        })

    def calcular_ponto_de_pedido(self, df_trans, df_est, lead_time=2, estoque_seguranca=3):
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