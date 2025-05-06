import dados
import streamlit as st
import pandas as pd
import plotly as pl
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


st.set_page_config(
    page_title="KPIs",
    layout="wide"
)


df_geral = dados.df_geral
df_modificado = df_geral

print(df_modificado)


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

def delta2():
    for i, val in df_geral["Tempo até aprovação"].items():
        if pd.isna(val):
            df_modificado.loc[i, "Tempo até aprovação"] = "Sem informação"
        else:
            dias = val.days  # converte Timedelta para número de dias
            if dias < 15:
                df_modificado.loc[i, "Tempo até aprovação"] = "No prazo"
            elif 15 <= dias < 29:
                df_modificado.loc[i, "Tempo até aprovação"] = "Alerta"
            else:
                df_modificado.loc[i, "Tempo até aprovação"] = "Urgente"

def deltaoverall():
    for i, val in df_geral["Tempo até a assinatura"].items():
        if pd.isna(val):
            df_modificado.loc[i, "Tempo até a assinatura"] = "Sem informação"
        else:
            dias = val.days  # converte Timedelta para número de dias
            if dias < 25:
                df_modificado.loc[i, "Tempo até a assinatura"] = "Tempo bom"
            elif 25 <= dias < 59:
                df_modificado.loc[i, "Tempo até a assinatura"] = "Atenção"
            else:
                df_modificado.loc[i, "Tempo até a assinatura"] = "Atrasado"





Contratos, ORÇAMENTOS, REGULATÓRIO, GERAL = st.tabs(["**Contratos**", "**ORÇAMENTOS**", "**REGULATÓRIO**", "**GERAL**"])

#TODO Contratos:
with Contratos:
    st.write("Delta 1")
    graf1, graf2 = st.columns(2)
    with graf1:
        # Aplica a função
        delta1e3('Tempo até resposta')

        # Conta as classificações
        contagem = df_modificado['Tempo até resposta'].value_counts().reindex(
            ["Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"], fill_value=0
        )

        # Gráfico de barras vertical
        fig = go.Figure(
            data=[go.Bar(
                x=contagem.index,
                y=contagem.values,
                marker_color=["gray", "green", "orange", "red", "lightblue"]
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
       # Contagem dos contratos por PI
        contagem_pi = df_modificado['Investigador PI'].value_counts()

        # Criando o gráfico de barras horizontal
        fig = go.Figure(go.Bar(
            x=contagem_pi.values,
            y=contagem_pi.index,
            orientation='h',
            marker_color='indianred'
        ))

        # Atualizando o layout do gráfico
        fig.update_layout(
            title='Contagem de contratos por Investigador PI',
            xaxis_title='Quantidade de contratos',
            yaxis_title='Investigador PI',
            template='plotly_white',
            yaxis=dict(autorange="reversed")  # Para mostrar os maiores no topo
        )

        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)








    st.write("Delta 2")
    graf3, graf4 = st.columns(2)
    with graf3:
        # Aplica a função
        delta2()

        # Conta as classificações
        contagem2 = df_modificado['Tempo até aprovação'].value_counts().reindex(
            ["Sem informação", "No prazo", "Alerta", "Urgente"], fill_value=0
        )

        # Gráfico de barras vertical
        fig = go.Figure(
            data=[go.Bar(
                x=contagem2.index,
                y=contagem2.values,
                marker_color=["gray", "green", "orange", "red"]
            )],
            layout=go.Layout(
                title="Frequência de cada classificação",
                xaxis_title="Classificação",
                yaxis_title="Quantidade",
                bargap=0.4
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    with graf4:
        # Contagem dos contratos por PI
        contagemsponsor = df_modificado['Nome do patrocinador'].value_counts()

        # Criando o gráfico de barras horizontal
        fig = go.Figure(go.Bar(
            x=contagemsponsor.values,
            y=contagemsponsor.index,
            orientation='h',
            marker_color='indianred'
        ))

        # Atualizando o layout do gráfico
        fig.update_layout(
            title='Contagem de contratos por Investigador PI',
            xaxis_title='Quantidade de contratos',
            yaxis_title='Sponsor',
            template='plotly_white',
            yaxis=dict(autorange="reversed")  # Para mostrar os maiores no topo
        )

        # Exibindo o gráfico no Streamlit
        st.plotly_chart(fig, use_container_width=True)







    st.write("Delta 3")
    graf5, graf6 = st.columns(2)
    with graf5:
        # Aplica a função
        delta1e3('Tempo da aprovação até a assinatura')

        # Conta as classificações
        contagem3 = df_modificado['Tempo da aprovação até a assinatura'].value_counts().reindex(
            ["Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"], fill_value=0
        )

        # Gráfico de barras vertical
        fig = go.Figure(
            data=[go.Bar(
                x=contagem3.index,
                y=contagem3.values,
                marker_color=["gray", "green", "orange", "red", "lightblue"]
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
        df_grouped = df_modificado.groupby(['Nome do patrocinador', 'Investigador PI']).size().reset_index(name='Quantidade')

        # Pivotar os dados para ficar no formato ideal
        pivot = df_grouped.pivot(index='Nome do patrocinador', columns='Investigador PI', values='Quantidade').fillna(0)

        # Dados
        sponsors = pivot.index.tolist()
        investigadores = pivot.columns.tolist()
        bar_width = 0.25
        x = np.arange(len(sponsors))

        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))

        # Desenhar cada Investigador PI com deslocamento
        for i, investigador in enumerate(investigadores):
            ax.bar(x + i * bar_width, pivot[investigador], bar_width, label=investigador)

        # Rótulos
        ax.set_xlabel('Sponsor')
        ax.set_ylabel('Quantidade de Contratos')
        ax.set_title('Contratos por Investigador PI agrupados por Sponsor')
        ax.set_xticks(x + bar_width * (len(investigadores) - 1) / 2)
        ax.set_xticklabels(sponsors, rotation=45, ha='right')
        ax.legend(title='Investigador PI')

        plt.tight_layout()
        st.pyplot(fig)


        # df_modificado.style()

























    st.write("Delta 4")
    graf7, graf8 = st.columns(2)
    with graf7:
         # Aplica a função
        deltaoverall()

        # Conta as classificações
        contagem4 = df_modificado['Tempo até a assinatura'].value_counts().reindex(
            ["Tempo bom", "Atenção", "Atrasado"], fill_value=0
        )

        # Gráfico de barras vertical
        fig = go.Figure(
            data=[go.Bar(
                x=contagem4.index,
                y=contagem4.values,
                marker_color=["green", "orange", "red"]
            )],
            layout=go.Layout(
                title="Frequência de cada classificação",
                xaxis_title="Classificação",
                yaxis_title="Quantidade",
                bargap=0.4
            )
        )
        st.plotly_chart(fig, use_container_width=True)
    with graf8:
        pass
        #st.bar("var_grafico")

    
    st.write("SLA")
    Delta1, Delta2, Delta3, Delta4 = st.columns(4)
    with Delta1:
        pass
    with Delta2:
        pass
    with Delta3:
        pass
    with Delta4:
        pass

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