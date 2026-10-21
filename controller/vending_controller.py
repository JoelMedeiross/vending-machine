# controller/vending_controller.py
import pandas as pd
import datetime

class VendingController:
    def __init__(self, model):
        self.model = model

    def realizar_compra(self, session_state, produto, quantidade):
        df_est = session_state.estoque_produtos
        idx = df_est[df_est['produto'] == produto].index[0]
        estoque_atual = df_est.loc[idx, 'estoque_atual']
        preco_unit = df_est.loc[idx, 'preco_unitario']

        if estoque_atual >= quantidade:
            # Atualiza estoque
            session_state.estoque_produtos.loc[idx, 'estoque_atual'] -= quantidade
            
            # Registra transação
            nova_linha = pd.DataFrame({
                "timestamp": [datetime.datetime.now()],
                "produto": [produto],
                "quantidade": [quantidade],
                "preco_unitario": [preco_unit]
            })
            session_state.transacoes = pd.concat([session_state.transacoes, nova_linha], ignore_index=True)
            return True, f"Compra de {quantidade}x {produto} efetuada com sucesso!"
        else:
            return False, "Estoque insuficiente na máquina!"

    def repor_estoque(self, session_state, produto, quantidade):
        df_est = session_state.estoque_produtos
        idx = df_est[df_est['produto'] == produto].index[0]
        session_state.estoque_produtos.loc[idx, 'estoque_atual'] += quantidade
        return True, f"Adicionado {quantidade} unidades de {produto}."