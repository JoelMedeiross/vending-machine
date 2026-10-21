# model/vending_model.py
import pandas as pd
import datetime

class VendingModel:
    def __init__(self):
        # Inicializa o estado se não existir
        pass

    def get_transacoes_iniciais(self):
        return pd.DataFrame({
            "timestamp": pd.date_range(start="2026-10-01", periods=20, freq="h"),
            "produto": ["Água", "Refrigerante", "Salgado", "Chocolate"] * 5,
            "quantidade": [1, 2, 1, 1] * 5,
            "preco_unitario": [4.00, 6.00, 8.00, 5.00] * 5
        })

    def get_estoque_inicial(self):
        return pd.DataFrame({
            "produto": ["Água", "Refrigerante", "Salgado", "Chocolate"],
            "estoque_atual": [12, 3, 15, 2],
            "preco_unitario": [4.00, 6.00, 8.00, 5.00]
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