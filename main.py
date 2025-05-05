import dados
import streamlit as st
import pandas as pd
import plotly as pl
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="KPIs",
    layout="wide"
)


df_geral = dados.df_geral
df_modificado = df_geral


#TODO: dias

cinco_dias = timedelta(days=5)
nove_dias = timedelta(days=9)
catorze_dias = timedelta(days=14)

def delta1e3(delta):
    for i, val in df_geral[delta].items():
        if pd.isna(val):
            df_modificado.loc[i, delta] = "Sem informação"
        else:
            dias = val.days  # converte Timedelta para número de dias
            if dias < 5:
                df_modificado.loc[i, delta] = "No prazo"
            elif 5 <= dias < 9:
                df_modificado.loc[i, delta] = "Alerta"
            elif 9 <= dias < 14:
                df_modificado.loc[i, delta] = "Urgente"
            else:
                df_modificado.loc[i, delta] = "Atrasado"


# Aplica a função
delta1e3('Tempo até resposta')

# Conta as classificações
contagem = df_modificado['Tempo até resposta'].value_counts().reindex(
    ["Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"], fill_value=0
)

# Aplica a função
delta1e3('Tempo da aprovação até a assinatura')

# Conta as classificações
contagem3 = df_modificado['Tempo da aprovação até a assinatura'].value_counts().reindex(
    ["Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"], fill_value=0
)


Contratos, ORÇAMENTOS, REGULATÓRIO, GERAL = st.tabs(["**Contratos**", "**ORÇAMENTOS**", "**REGULATÓRIO**", "**GERAL**"])

#TODO Contratos:
with Contratos:
    st.write("Delta 1")
    graf1, graf2 = st.columns(2)
    with graf1:
        # Gráfico de barras vertical
        fig = go.Figure(
            data=[go.Bar(
                x=contagem.index,
                y=contagem.values,
                marker_color=["green", "orange", "red", "gray", "lightblue"]
            )],
            layout=go.Layout(
                title="Frequência de cada classificação",
                xaxis_title="Classificação",
                yaxis_title="Quantidade",
                bargap=0.4
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    with graf2:
        #st.bar("var_grafico")
        pass

    st.write("Delta 2")
    graf3, graf4 = st.columns(2)
    with graf3:
        pass
        #st.bar("var_grafico")
    with graf4:
        pass
        #st.bar("var_grafico")

    st.write("Delta 3")
    graf5, graf6 = st.columns(2)
    with graf5:
        # Gráfico de barras vertical
        fig = go.Figure(
            data=[go.Bar(
                x=contagem3.index,
                y=contagem3.values,
                marker_color=["green", "orange", "red", "gray", "lightblue"]
            )],
            layout=go.Layout(
                title="Frequência de cada classificação",
                xaxis_title="Classificação",
                yaxis_title="Quantidade",
                bargap=0.4
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    with graf6:
        pass
        #st.bar("var_grafico")

    st.write("Delta 4")
    graf7, graf8 = st.columns(2)
    with graf7:
        pass
        #st.bar("var_grafico")
    with graf8:
        pass
        #st.bar("var_grafico")

    st.markdown("---")
    st.subheader("📋 Visualização da Tabela Geral")

    # Defina as colunas que você quer que o usuário possa selecionar
    colunas_disponiveis = ["Protocolo", "Centro coordenador", "Nome do patrocinador", "Investigador PI", "Status do contrato", "Tempo até a assinatura", "Data do recebimento do orçamento", "Data da aprovação do orçamento", "Tempo no orçamento", "Obsevações do contrato"]

    # Ajusta para exibir apenas as que existem de fato no DataFrame
    colunas_disponiveis = [col for col in colunas_disponiveis if col in df_modificado.columns]

    # Campo de seleção de colunas
    colunas_selecionadas = st.multiselect(
        "Selecione as colunas que deseja visualizar:",
        options=colunas_disponiveis,
        default=colunas_disponiveis  # ou selecione algumas por padrão
    )

    # Exibe apenas as colunas selecionadas
    st.dataframe(df_modificado[colunas_selecionadas])

#TODO Orcamentos:
with ORÇAMENTOS:
    st.write("Delta 1")
    graf1, graf2 = st.columns(2)
    with graf1:
        pass
        #st.bar("var_grafico")
    with graf2:
        pass
        #st.bar("var_grafico")

    st.write("Delta 2")
    graf3, graf4 = st.columns(2)
    with graf3:
        pass
        #st.bar("var_grafico")
    with graf4:
        pass
        #st.bar("var_grafico")

    st.write("Delta 3")
    graf5, graf6 = st.columns(2)
    with graf5:
        pass
        #st.bar("var_grafico")
    with graf6:
        pass
        #st.bar("var_grafico")
    
#TODO Regulatorio:
with REGULATÓRIO:
    st.write("Delta 1")
    graf1, graf2 = st.columns(2)
    with graf1:
        pass
        #st.bar("var_grafico")
    with graf2:
        pass
        #st.bar("var_grafico")

#TODO Geral:
with GERAL:
    pass