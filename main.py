import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
import dados

# TODO Configuração da página
st.set_page_config(page_title="KPIs", layout="wide")

# TODO Carregamento de dados
df_geral = dados.df_geral.copy()
df_modificado = df_geral.copy()

# TODO Funções para classificação de deltas
def classificar_delta(df, coluna, faixas):
    df[coluna] = pd.to_timedelta(df[coluna], errors='coerce')
    resultado = []
    for val in df[coluna]:
        if pd.isna(val):
            resultado.append("Sem informação")
        else:
            dias = val.days
            for rotulo, minimo, maximo in faixas:
                if minimo <= dias < maximo:
                    resultado.append(rotulo)
                    break
            else:
                resultado.append(faixas[-1][0])
    return resultado

# TODO Aplicando as classificações
df_modificado['Tempo até resposta'] = classificar_delta(df_geral, 'Tempo até resposta', [
    ("No prazo", 0, 5),
    ("Alerta", 5, 9),
    ("Urgente", 9, 14),
    ("Atrasado", 14, float('inf'))
])

df_modificado['Tempo até aprovação'] = classificar_delta(df_geral, 'Tempo até aprovação', [
    ("No prazo", 0, 15),
    ("Alerta", 15, 29),
    ("Urgente", 29, float('inf'))
])

df_modificado['Tempo da aprovação até a assinatura'] = classificar_delta(df_geral, 'Tempo da aprovação até a assinatura', [
    ("No prazo", 0, 5),
    ("Alerta", 5, 9),
    ("Urgente", 9, 14),
    ("Atrasado", 14, float('inf'))
])

df_modificado['Tempo até a assinatura'] = classificar_delta(df_geral, 'Tempo até a assinatura', [
    ("Tempo bom", 0, 25),
    ("Atenção", 25, 59),
    ("Atrasado", 59, float('inf'))
])

# TODO Filtro lateral
status_opcoes = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"]
Delta1Filtro = st.sidebar.selectbox("Status delta 1", status_opcoes)

status_delta2 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente"]
Delta2Filtro = st.sidebar.selectbox("Status delta 2", status_delta2)

status_delta3 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"]
Delta3Filtro = st.sidebar.selectbox("Status delta 3", status_delta3)

status_delta4 = ["Geral", "Tempo bom", "Atenção", "Atrasado"]
Delta4Filtro = st.sidebar.selectbox("Status delta 4", status_delta4)


if Delta1Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Tempo até resposta'] == Delta1Filtro]

if Delta2Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Tempo até aprovação'] == Delta2Filtro]

if Delta3Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Tempo da aprovação até a assinatura'] == Delta3Filtro]

if Delta4Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Tempo até a assinatura'] == Delta4Filtro]


# Abas
Contratos, ORCAMENTOS, REGULATORIO, GERAL = st.tabs(["**Contratos**", "**ORÇAMENTOS**", "**REGULATÓRIO**", "**GERAL**"])

# Função de gráfico de barras
def grafico_barras(contagem, titulo, cores):
    return go.Figure(
        data=[go.Bar(x=contagem.index, y=contagem.values, marker_color=cores)],
        layout=go.Layout(
            title=titulo,
            xaxis_title="Classificação",
            yaxis_title="Quantidade",
            bargap=0.4
        )
    )

# Função de gráfico horizontal por PI
def grafico_horizontal_por_coluna(coluna, titulo):
    contagem = df_modificado[coluna].value_counts()
    fig = go.Figure(go.Bar(
        x=contagem.values,
        y=contagem.index,
        orientation='h',
        marker_color='indianred'
    ))
    fig.update_layout(
        title=titulo,
        xaxis_title='Quantidade',
        yaxis_title=coluna,
        template='plotly_white',
        yaxis=dict(autorange="reversed")
    )
    return fig

# Função de gráfico agrupado por PI e sponsor
def grafico_agrupado():
    df_grouped = df_modificado.groupby(['Nome do patrocinador', 'Investigador PI']).size().reset_index(name='Quantidade')
    pivot = df_grouped.pivot(index='Nome do patrocinador', columns='Investigador PI', values='Quantidade').fillna(0)
    sponsors = pivot.index.tolist()
    investigadores = pivot.columns.tolist()
    bar_width = 0.12
    x = np.arange(len(sponsors))

    fig, ax = plt.subplots(figsize=(24, 12))
    for i, investigador in enumerate(investigadores):
        ax.bar(x + i * bar_width, pivot[investigador], bar_width, label=investigador)

    ax.set_xlabel('Sponsor')
    ax.set_ylabel('Quantidade de Contratos')
    ax.set_title('Contratos por Investigador PI agrupados por Sponsor')
    ax.set_xticks(x + bar_width * (len(investigadores) - 1) / 2)
    ax.set_xticklabels(sponsors, rotation=45, ha='right')
    ax.legend(title='Investigador PI')
    plt.tight_layout()
    return fig

# TODO: Aba Contratos
with Contratos:
    st.write("Delta 1")
    graf1, graf2 = st.columns(2)
    with graf1:
        contagem = df_modificado['Tempo até resposta'].value_counts().reindex(status_opcoes[1:], fill_value=0)
        st.plotly_chart(grafico_barras(contagem, "Classificação do Delta 1", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True)
    with graf2:
        st.plotly_chart(grafico_horizontal_por_coluna('Investigador PI', 'Contratos por Investigador PI'), use_container_width=True)

    st.write("Delta 2")
    graf3, graf4 = st.columns(2)
    with graf3:
        contagem = df_modificado['Tempo até aprovação'].value_counts().reindex(["Sem informação", "No prazo", "Alerta", "Urgente"], fill_value=0)
        st.plotly_chart(grafico_barras(contagem, "Classificação do Delta 2", ["gray", "green", "orange", "red"]), use_container_width=True)
    with graf4:
        st.plotly_chart(grafico_horizontal_por_coluna('Nome do patrocinador', 'Contratos por Sponsor'), use_container_width=True)

    st.write("Delta 3")
    graf5, graf6 = st.columns(2)
    with graf5:
        contagem = df_modificado['Tempo da aprovação até a assinatura'].value_counts().reindex(status_delta3[1:], fill_value=0)
        st.plotly_chart(grafico_barras(contagem, "Classificação do Delta 3", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True)
    with graf6:
        st.pyplot(grafico_agrupado())

    st.write("Delta 4")
    graf7, graf8 = st.columns(2)
    with graf7:
        contagem = df_modificado['Tempo até a assinatura'].value_counts().reindex(["Tempo bom", "Atenção", "Atrasado"], fill_value=0)
        st.plotly_chart(grafico_barras(contagem, "Classificação do Delta 4", ["green", "orange", "red"]), use_container_width=True)
    with graf8:
        pass  # Espaço reservado para futuros gráficos


    #TODO: tabela
    st.subheader("📋 Visualização da Tabela Geral")
    colunas_disponiveis = [col for col in [
        "Protocolo", "Centro coordenador", "Nome do patrocinador", "Investigador PI",
        "Status do contrato", "Tempo até a assinatura", "Tempo da aprovação até a assinatura", "Tempo até aprovação", "Tempo até resposta","Data do recebimento do orçamento",
        "Data da aprovação do orçamento", "Tempo no orçamento", "Obsevações do contrato"
    ] if col in df_modificado.columns]

    colunas_selecionadas = st.multiselect("Selecione as colunas para visualizar:", colunas_disponiveis, default=colunas_disponiveis)
    st.dataframe(df_modificado[colunas_selecionadas])

# Abas Orcamentos, Regulatorio e Geral permanecem como TODO