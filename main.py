
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import dados
import altair as alt


# TODO Configuração da página
st.set_page_config(page_title="KPIs", layout="wide")

# TODO Carregamento de dados
df_geral = dados.df_geral.copy()
df_modificado = df_geral.copy()

today = pd.to_datetime(date.today()) 

# TODO Funções para classificação de deltas
def classificar_delta(df, coluna, faixas):
    df[coluna] = pd.to_datetime(df[coluna], errors='coerce')  # Era to_timedelta, corrigido para to_datetime
    df['Data do recebimento do contrato'] = pd.to_datetime(df['Data do recebimento do contrato'], errors='coerce')

    resultado = []
    for i, val in enumerate(df[coluna]):
        if pd.isna(val):
            if coluna == 'Tempo até resposta':
                recebimento = df.loc[i, 'Data do recebimento do contrato']
                if pd.notna(recebimento):
                    temporesp = today - recebimento
                    dias = temporesp.days
                    for rotulo, minimo, maximo in faixas:
                        if minimo <= dias < maximo:
                            resultado.append(rotulo)
                            break
                    else:
                        resultado.append(faixas[-1][0])
                else:
                    resultado.append("Sem informação")

            elif coluna == 'Tempo até aprovação':
                recebimento = df.loc[i, 'Data da resposta do contrato']
                if pd.notna(recebimento):
                    temporesp = today - recebimento
                    dias = temporesp.days
                    for rotulo, minimo, maximo in faixas:
                        if minimo <= dias < maximo:
                            resultado.append(rotulo)
                            break
                    else:
                        resultado.append(faixas[-1][0])
                else:
                    resultado.append("Sem informação")

            elif coluna == 'Tempo da aprovação até a assinatura':
                recebimento = df.loc[i, 'Data da aprovação do contrato']
                if pd.notna(recebimento):
                    temporesp = today - recebimento
                    dias = temporesp.days
                    for rotulo, minimo, maximo in faixas:
                        if minimo <= dias < maximo:
                            resultado.append(rotulo)
                            break
                    else:
                        resultado.append(faixas[-1][0])
                else:
                    resultado.append("Sem informação")  

            elif coluna == 'Tempo até a assinatura':
                recebimento = df.loc[i, 'Data da assinatura do contrato']
                if pd.notna(recebimento):
                    temporesp = today - recebimento
                    dias = temporesp.days
                    for rotulo, minimo, maximo in faixas:
                        if minimo <= dias < maximo:
                            resultado.append(rotulo)
                            break
                    else:
                        resultado.append(faixas[-1][0])
                else:
                    resultado.append("Sem informação")
                
            
            else:
                resultado.append("Sem informação")
        else:
            delta = val - df.loc[i, 'Data do recebimento do contrato']
            if pd.isna(delta):
                resultado.append("Sem informação")
            else:
                dias = delta.days
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
    ("Alerta", 5, 10),
    ("Urgente", 10, 15),
    ("Atrasado", 15, float('inf'))
])

df_modificado['Tempo até aprovação'] = classificar_delta(df_geral, 'Tempo até aprovação', [
    ("No prazo", 0, 15),
    ("Alerta", 15, 30),
    ("Urgente", 30, float('inf'))
])

df_modificado['Tempo da aprovação até a assinatura'] = classificar_delta(df_geral, 'Tempo da aprovação até a assinatura', [
    ("No prazo", 0, 5),
    ("Alerta", 5, 10),
    ("Urgente", 10, 15),
    ("Atrasado", 15, float('inf'))
])

df_modificado['Tempo até a assinatura'] = classificar_delta(df_geral, 'Tempo até a assinatura', [
    ("Tempo bom", 0, 25),
    ("Atenção", 25, 60),
    ("Atrasado", 60, float('inf'))
])

BaseDeDados = st.sidebar.radio("Selecione a base de dados",
                        ["Em andamento",
                        "Concluidos",
                        "Geral",],
                        index=None)





if BaseDeDados == "Em andamento":
    df_modificado = df_modificado[~df_modificado['Status do contrato'].isin(['Assinado']) & ~df_modificado['Status do contrato'].isin(['Não recebido'])]
elif BaseDeDados == "Concluidos":
    df_modificado = df_modificado[df_modificado['Status do contrato'].isin(['Assinado'])]


#TODO: Abas
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

def grafico_pizza(contagem, titulo, cores):
    total = contagem.sum()
    labels = contagem.index
    values = contagem.values
    text = [f'{(v/total)*100:.1f}%<br>({v} n)' for v in values]

    return go.Figure(
        data=[go.Pie(labels=labels,
                    values=values,
                    marker_colors=cores,
                    text=text,
                    textinfo='label+text',
                    hoverinfo='label+percent+value')],
        layout=go.Layout(
            title=titulo,
            margin=dict(l=0, r=0, t=40, b=0)
        )
    )
    
# TODO: Aba Contratos
with Contratos:
    # TODO Filtro lateral de Contratos
    status_opcoes = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"]
    Delta1Filtro = st.sidebar.selectbox("Status delta 1", status_opcoes)

    pi_options = sorted(df_modificado['Investigador PI'].unique())
    PiFiltro = st.sidebar.multiselect("Selecione o PI", options=pi_options)

    status_delta2 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente"]
    Delta2Filtro = st.sidebar.selectbox("Status delta 2", status_delta2)

    sponsor_options = sorted(df_modificado['Nome do patrocinador'].unique())
    sponsorFiltro = st.sidebar.multiselect("Selecione o Sponsor", options=sponsor_options)

    status_delta3 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"]
    Delta3Filtro = st.sidebar.selectbox("Status delta 3", status_delta3)

    status_delta4 = ["Geral", "Tempo bom", "Atenção", "Atrasado"]
    Delta4Filtro = st.sidebar.selectbox("Status delta 4", status_delta4)

    st.sidebar.write("-------------------------------------------------------------------------------------------------")

    #TODO: deltas selecionados de contratos
    if Delta1Filtro != "Geral":
        df_modificado = df_modificado[df_modificado['Tempo até resposta'] == Delta1Filtro]

    if Delta2Filtro != "Geral":
        df_modificado = df_modificado[df_modificado['Tempo até aprovação'] == Delta2Filtro]

    if Delta3Filtro != "Geral":
        df_modificado = df_modificado[df_modificado['Tempo da aprovação até a assinatura'] == Delta3Filtro]

    if Delta4Filtro != "Geral":
        df_modificado = df_modificado[df_modificado['Tempo até a assinatura'] == Delta4Filtro]

    #TODO: Outros filtros selecionados de contratos
    if PiFiltro:
        df_modificado = df_modificado[df_modificado['Investigador PI'].isin(PiFiltro)]

    if sponsorFiltro:
        df_modificado = df_modificado[df_modificado['Nome do patrocinador'].isin(sponsorFiltro)]


    #TODO: Delta 1
    with st.expander("Delta 1"):
        st.markdown("Tempo até resposta:<br>< 5 dias No prazo<br>5 - 9 dias Alerta<br>10 - 14 dias Urgente<br>15+ dias Atrasado", unsafe_allow_html=True)

    graf1, graf2 = st.columns(2)
    with graf1:
        contagem = df_modificado['Tempo até resposta'].value_counts().reindex(status_opcoes[1:], fill_value=0)
        st.plotly_chart(grafico_barras(contagem, "Classificação do Delta 1", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True)
    with graf2:
        st.plotly_chart(grafico_horizontal_por_coluna('Investigador PI', 'Contratos por Investigador PI'), use_container_width=True)

    #TODO: Delta 2
    with st.expander("Delta 2"):
        st.markdown("Tempo até aprovação:<br>< 15 dias No prazo<br>15 - 29 dias Alerta<br>30+ dias Urgente", unsafe_allow_html=True)

    graf3, graf4 = st.columns(2)
    with graf3:
        contagem = df_modificado['Tempo até aprovação'].value_counts().reindex(["Sem informação", "No prazo", "Alerta", "Urgente"], fill_value=0)
        st.plotly_chart(grafico_barras(contagem, "Classificação do Delta 2", ["gray", "green", "orange", "red"]), use_container_width=True)
    with graf4:
        st.plotly_chart(grafico_horizontal_por_coluna('Nome do patrocinador', 'Contratos por Sponsor'), use_container_width=True)

    #TODO: Delta 3
    with st.expander("Delta 3"):
        st.markdown("Tempo da aprovação até a assinatura:<br>< 5 dias No prazo<br>5 - 9 dias Alerta<br>10 - 14 dias Urgente<br>15+ dias Atrasado", unsafe_allow_html=True)

    graf5, graf6 = st.columns(2)
    with graf5:
        contagem = df_modificado['Tempo da aprovação até a assinatura'].value_counts().reindex(status_delta3[1:], fill_value=0)
        st.plotly_chart(grafico_barras(contagem, "Classificação do Delta 3", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True)
    with graf6:

       # Agrupamento e contagem
        df_grouped = df_modificado.groupby(['Nome do patrocinador', 'Investigador PI']).size().reset_index(name='Quantidade')

        # Renomeia colunas para facilitar o uso no Streamlit
        df_grouped = df_grouped.rename(columns={
            'Nome do patrocinador': 'Sponsor',
            'Investigador PI': 'Investigador'
        })

        # Gráfico com Altair (barras horizontais)
        chart = alt.Chart(df_grouped).mark_bar().encode(
            y=alt.Y('Sponsor:N', sort='-x'),
            x='Quantidade:Q',
            color='Investigador:N',
            tooltip=['Sponsor', 'Investigador', 'Quantidade']
        ).properties(
            width='container',
            height=500
        )

        st.altair_chart(chart, use_container_width=True)

    #TODO: Delta 4
    with st.expander("Delta 4"):
        st.markdown("Tempo até resposta:<br><= 24 dias: Tempo Bom<br>25 - 59 dias: Atenção<br>60+ dias Atrasado", unsafe_allow_html=True)

    graf7, graf8 = st.columns(2)
    with graf7:
        contagem = df_modificado['Tempo até a assinatura'].value_counts().reindex(["Tempo bom", "Atenção", "Atrasado"], fill_value=0)
        st.plotly_chart(grafico_barras(contagem, "Classificação do Delta 4", ["green", "orange", "red"]), use_container_width=True)
    with graf8:
        # Agrupamento e contagem
        df_grouped = df_modificado.groupby(['Status do contrato', 'Tempo até resposta']).size().reset_index(name='Quantidade')

        # Renomeia colunas para facilitar o uso no Streamlit
        df_grouped = df_grouped.rename(columns={
            'Status do contrato': 'Status',
            'Tempo até resposta': 'Tempo até resposta'
        })

        # Gráfico de barras horizontais com Altair
        chart = alt.Chart(df_grouped).mark_bar().encode(
            y=alt.Y('Status:N', sort='-x', title='Status do Contrato'),
            x=alt.X('Quantidade:Q', title='Quantidade'),
            color=alt.Color('Tempo até resposta:N', title='Tempo até Resposta'),
            tooltip=['Status', 'Tempo até resposta', 'Quantidade']
        ).properties(
            width='container',
            height=500,
            title='Quantidade por Status do Contrato e Tempo até Resposta'
        )

        # Exibe o gráfico no Streamlit
        st.altair_chart(chart, use_container_width=True)

    #TODO: SLA

    sla1, sla2, sla3, sla4 = st.columns(4)
    with sla1:
        # Dados de contagem
        contagem = df_modificado['Tempo até resposta'].value_counts().reindex(status_opcoes[1:], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            grafico_pizza(contagem, "Distribuição do Tempo até Resposta (Delta 1)", 
                        ["gray", "green", "orange", "red", "lightblue"]),
            use_container_width=True
        )

    with sla2:
        # Dados de contagem
        contagem = df_modificado['Tempo até aprovação'].value_counts().reindex(status_opcoes[1:], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            grafico_pizza(contagem, "Distribuição do Tempo até aprovação (Delta 2)", 
                        ["gray", "green", "orange", "red", "lightblue"]),
            use_container_width=True
        )

    with sla3:
        # Dados de contagem
        contagem = df_modificado['Tempo da aprovação até a assinatura'].value_counts().reindex(status_opcoes[1:], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            grafico_pizza(contagem, "Distribuição do Tempo da aprovação até a assinatura (Delta 3)", 
                        ["gray", "green", "orange", "red", "lightblue"]),
            use_container_width=True
        )
    with sla4:
        # Dados de contagem
        contagem = df_modificado['Tempo até a assinatura'].value_counts().reindex(status_opcoes[1:], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            grafico_pizza(contagem, "Distribuição do Tempo até a assinatura (Delta )", 
                        ["gray", "green", "orange", "red", "lightblue"]),
            use_container_width=True
        )


    #TODO: tabela
    st.subheader("Tabela Geral")
    colunas_disponiveis = [col for col in [
        "Protocolo", "Centro coordenador", "Nome do patrocinador", "Investigador PI",
        "Status do contrato", "Tempo até resposta", "Tempo até aprovação", "Tempo da aprovação até a assinatura", "Tempo até a assinatura", "Obsevações do contrato"
    ] if col in df_modificado.columns]

    colunas_selecionadas = st.multiselect("Selecione as colunas para visualizar:", colunas_disponiveis, default=colunas_disponiveis)
    st.dataframe(df_modificado[colunas_selecionadas])

#TODO Aba Orcamentos
with ORCAMENTOS:

    orcamentos_delta1 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"]
    orcamentos_Delta1Filtro = st.sidebar.selectbox("Status delta 1", orcamentos_delta1)

    orcamentos_delta2 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"]
    orcamentos_Delta2Filtro = st.sidebar.selectbox("Status delta 2", orcamentos_delta2)

    orcamentos_delta3 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"]
    orcamentos_Delta3Filtro = st.sidebar.selectbox("Status delta 2", orcamentos_delta3)

    st.sidebar.write("---------------------------------------------------------")

    #TODO: Delta 1
    with st.expander("Delta 1"):
        st.markdown("Tempo até resposta do orçamento:<br>", unsafe_allow_html=True)
        

    with st.expander("Delta 2"):
        st.markdown("Tempo decorrido de resposta até aprovado em orçamento:<br>", unsafe_allow_html=True)

    with st.expander("Delta 3"):
        st.markdown("Tempo no orçamento:<br>", unsafe_allow_html=True)

#TODO Aba regulatorio
with REGULATORIO:
    with st.expander("Delta"):
        st.markdown("Tempo no regulatório:", unsafe_allow_html=True)

#TODO Aba geral
with GERAL:
    with st.expander("Geral"):
        st.markdown(".:", unsafe_allow_html=True)