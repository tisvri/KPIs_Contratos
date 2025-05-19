
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import dados
import graficos
import altair as alt
import itertools


# TODO Configuração da página
st.set_page_config(page_title="KPIs", layout="wide")

# TODO Carregamento de dados
df_geral = dados.df_geral.copy()
df_modificado = df_geral.copy()

hoje = pd.Timestamp.today()

today = pd.to_datetime(date.today()) 

#TODO Fazendo a clacificacao dos deltas
df_modificado['Data do recebimento do contrato'] = pd.to_datetime(df_modificado['Data do recebimento do contrato'], errors='coerce')
df_modificado['Tempo até resposta'] = pd.to_timedelta(df_modificado['Tempo até resposta'], errors='coerce')
df_modificado['Tempo até aprovação'] = pd.to_timedelta(df_modificado['Tempo até aprovação'], errors='coerce')
df_modificado['Tempo da aprovação até a assinatura'] = pd.to_timedelta(df_modificado['Tempo da aprovação até a assinatura'], errors='coerce')
df_modificado['Tempo até a assinatura'] = pd.to_timedelta(df_modificado['Tempo até a assinatura'], errors='coerce')

# Criando listas para armazenar os resultados

tempo_resposta = []
tempo_aprovacao = []
tempo_ate_assinatura = []
tempo_total_assinatura = []

for cad, resp, apro, ateassi, assina, resporçã, ateapro, temporça in itertools.zip_longest(df_modificado['Data do recebimento do contrato'], df_modificado['Tempo até resposta'], df_modificado['Tempo até aprovação'], df_modificado['Tempo da aprovação até a assinatura'], df_modificado['Tempo até a assinatura'], df_modificado['Tempo até resposta do orçamento'], df_modificado['Tempo decorrido de resposta até aprovado em orçamento'], df_modificado['Tempo no orçamento']):
    # Tempo até resposta
    if pd.isna(resp):
        if pd.isna(cad):
            tempo_resposta.append('Sem informação')
        else:
            diff = hoje - cad
            if diff < pd.Timedelta(days=5):
                tempo_resposta.append('No prazo')
            elif diff <= pd.Timedelta(days=9):
                tempo_resposta.append('Alerta')
            elif diff <= pd.Timedelta(days=14):
                tempo_resposta.append('Urgente')
            else:
                tempo_resposta.append('Atrasado')
    elif resp < pd.Timedelta(days=5):
        tempo_resposta.append('No prazo') 
    elif pd.Timedelta(days=5) <= resp <= pd.Timedelta(days=9):
        tempo_resposta.append('Alerta')
    elif pd.Timedelta(days=10) <= resp <= pd.Timedelta(days=14):
        tempo_resposta.append('Urgente')
    elif resp >= pd.Timedelta(days=15):
        tempo_resposta.append('Atrasado')

    # Tempo até aprovação
    if pd.isna(apro):
        if pd.isna(resp):
            tempo_aprovacao.append('Sem informação')
        else:
            diff = hoje - resp
            if diff < pd.Timedelta(days=15):
                tempo_aprovacao.append('No prazo')
            elif pd.Timedelta(days=15) <= diff <= pd.Timedelta(days=29):
                tempo_aprovacao.append('Alerta')
            elif diff >= pd.Timedelta(days=30):
                tempo_aprovacao.append('Urgente')
    else:
        base = resp if not pd.isna(resp) else pd.Timedelta(0)
        diferenca = apro - base
        if diferenca < pd.Timedelta(days=15):
            tempo_aprovacao.append('No prazo') 
        elif pd.Timedelta(days=15) <= diferenca <= pd.Timedelta(days=29):
            tempo_aprovacao.append('Alerta')
        elif diferenca >= pd.Timedelta(days=30):
            tempo_aprovacao.append('Urgente')

    # Tempo da aprovação até a assinatura
    if pd.isna(ateassi):
        if pd.isna(apro):
            tempo_ate_assinatura.append('Sem informação') 
        else:
            base = resp if not pd.isna(resp) else pd.Timedelta(0)
            diferenca = apro - base
            if diferenca < pd.Timedelta(days=5):
                tempo_ate_assinatura.append('No prazo') 
            elif pd.Timedelta(days=5) <= diferenca <= pd.Timedelta(days=9):
                tempo_ate_assinatura.append('Alerta')
            elif pd.Timedelta(days=10) <= diferenca <= pd.Timedelta(days=14):
                tempo_ate_assinatura.append('Urgente')
            elif diferenca >= pd.Timedelta(days=30):
                tempo_ate_assinatura.append('Atrasado')

    elif ateassi < pd.Timedelta(days=5):
        tempo_ate_assinatura.append('No prazo') 
    elif pd.Timedelta(days=5) <= ateassi <= pd.Timedelta(days=9):
        tempo_ate_assinatura.append('Alerta')
    elif pd.Timedelta(days=10) <= ateassi <= pd.Timedelta(days=14):
        tempo_ate_assinatura.append('Urgente')
    elif ateassi >= pd.Timedelta(days=15):
        tempo_ate_assinatura.append('Atrasado')

    # Tempo total até a assinatura
    if pd.isna(assina):
        tempo_total_assinatura.append('Sem informação')
    elif (assina) < pd.Timedelta(days=25):
        tempo_total_assinatura.append('Bom') 
    elif pd.Timedelta(days=25) <= (assina) <= pd.Timedelta(days=59):
        tempo_total_assinatura.append('Atenção')
    elif (assina) >= pd.Timedelta(days=60):
        tempo_total_assinatura.append('Atrasado')

# Atribuindo os resultados às novas colunas
df_modificado['Tempo ate a resposta'] = tempo_resposta
df_modificado['até aprovação'] = tempo_aprovacao
df_modificado['Aprovação até a assinatura'] = tempo_ate_assinatura
df_modificado['Até a assinatura'] = tempo_total_assinatura



#TODO FILTROS LATERAIS:
BaseDeDados = st.sidebar.radio("Selecione a base de dados",
                        ["Em andamento",
                        "Concluidos",
                        "Geral",],
                        index=None)

st.sidebar.write("---------------Contratos---------------")

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

st.sidebar.write("--------------Orçamentos--------------")


#TODO: Deltas selecionados

if BaseDeDados == "Em andamento":
    df_modificado = df_modificado[~df_modificado['Status do contrato'].isin(['Assinado']) & ~df_modificado['Status do contrato'].isin(['Não recebido'])]
elif BaseDeDados == "Concluidos":
    df_modificado = df_modificado[df_modificado['Status do contrato'].isin(['Assinado'])]

if Delta1Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Tempo ate a resposta'] == Delta1Filtro]

if Delta2Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['até aprovação'] == Delta2Filtro]

if Delta3Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Aprovação até a assinatura'] == Delta3Filtro]

if Delta4Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Até a assinatura'] == Delta4Filtro]

if PiFiltro:
        df_modificado = df_modificado[df_modificado['Investigador PI'].isin(PiFiltro)]

if sponsorFiltro:
    df_modificado = df_modificado[df_modificado['Nome do patrocinador'].isin(sponsorFiltro)]





#TODO: Abas
Contratos, ORCAMENTOS, REGULATORIO, GERAL = st.tabs(["**Contratos**", "**ORÇAMENTOS**", "**REGULATÓRIO**", "**GERAL**"])

    
# TODO: Aba Contratos
with Contratos:

    #TODO: Delta 1
    with st.expander("Delta 1"):
        st.markdown("Tempo até resposta:<br>< 5 dias No prazo<br>5 - 9 dias Alerta<br>10 - 14 dias Urgente<br>15+ dias Atrasado", unsafe_allow_html=True)

    graf1, graf2 = st.columns(2)
    with graf1:
        contagem = df_modificado['Tempo ate a resposta'].value_counts().reindex(status_opcoes[1:], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação do Delta 1", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True)
    with graf2:
        st.plotly_chart(graficos.grafico_horizontal_por_coluna(df_modificado,'Investigador PI', 'Contratos por Investigador PI'), use_container_width=True)

    #TODO: Delta 2
    with st.expander("Delta 2"):
        st.markdown("Tempo até aprovação:<br>< 15 dias No prazo<br>15 - 29 dias Alerta<br>30+ dias Urgente", unsafe_allow_html=True)

    graf3, graf4 = st.columns(2)
    with graf3:
        contagem = df_modificado['até aprovação'].value_counts().reindex(["Sem informação", "No prazo", "Alerta", "Urgente"], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação do Delta 2", ["gray", "green", "orange", "red"]), use_container_width=True)
    with graf4:
        st.plotly_chart(graficos.grafico_horizontal_por_coluna(df_modificado,'Nome do patrocinador', 'Contratos por Sponsor'), use_container_width=True)

    #TODO: Delta 3
    with st.expander("Delta 3"):
        st.markdown("Tempo da aprovação até a assinatura:<br>< 5 dias No prazo<br>5 - 9 dias Alerta<br>10 - 14 dias Urgente<br>15+ dias Atrasado", unsafe_allow_html=True)

    graf5, graf6 = st.columns(2)
    with graf5:
        contagem = df_modificado['Aprovação até a assinatura'].value_counts().reindex(status_delta3[1:], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação do Delta 3", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True)
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
        contagem = df_modificado['Até a assinatura'].value_counts().reindex(["Sem informação","Tempo bom", "Atenção", "Atrasado"], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação do Delta 4", ["gray","green", "orange", "red"]), use_container_width=True)
    with graf8:
        # Agrupamento e contagem
        df_grouped = df_modificado.groupby(['Status do contrato', 'Tempo ate a resposta']).size().reset_index(name='Quantidade')

        # Renomeia colunas para facilitar o uso no Streamlit
        df_grouped = df_grouped.rename(columns={
            'Status do contrato': 'Status',
            'Tempo ate a resposta': 'Tempo ate a resposta'
        })

        # Gráfico de barras horizontais com Altair
        chart = alt.Chart(df_grouped).mark_bar().encode(
            y=alt.Y('Status:N', sort='-x', title='Status do Contrato'),
            x=alt.X('Quantidade:Q', title='Quantidade'),
            color=alt.Color('Tempo ate a resposta:N', title='Tempo ate a resposta'),
            tooltip=['Status', 'Tempo ate a resposta', 'Quantidade']
        ).properties(
            width='container',
            height=500,
            title='Quantidade por Status do Contrato e Tempo ate a resposta'
        )

        # Exibe o gráfico no Streamlit
        st.altair_chart(chart, use_container_width=True)

    #TODO: SLA

    sla1, sla2, sla3, sla4 = st.columns(4)
    with sla1:
        # Dados de contagem
        contagem = df_modificado['Tempo ate a resposta'].value_counts().reindex(status_opcoes[1:], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            graficos.grafico_pizza(contagem, "Distribuição do Tempo até Resposta (Delta 1)", 
                        ["gray", "green", "orange", "red", "lightblue"]),
            use_container_width=True
        )

    with sla2:
        # Dados de contagem
        contagem = df_modificado['até aprovação'].value_counts().reindex(status_opcoes[1:], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            graficos.grafico_pizza(contagem, "Distribuição do Tempo até aprovação (Delta 2)", 
                        ["gray", "green", "orange", "red", "lightblue"]),
            use_container_width=True
        )

    with sla3:
        # Dados de contagem
        contagem = df_modificado['Aprovação até a assinatura'].value_counts().reindex(status_opcoes[1:], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            graficos.grafico_pizza(contagem, "Distribuição do Tempo da aprovação até a assinatura (Delta 3)", 
                        ["gray", "green", "orange", "red", "lightblue"]),
            use_container_width=True
        )
    with sla4:
        # Dados de contagem
        contagem = df_modificado['Até a assinatura'].value_counts().reindex(["Sem informação","Tempo bom", "Atenção", "Atrasado"], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            graficos.grafico_pizza(contagem, "Distribuição do Tempo até a assinatura (Delta )", 
                        [ "gray", "green","orange", "red", "lightblue"]),
            use_container_width=True
        )


    #TODO: tabela
    st.subheader("Tabela Geral")
    colunas_disponiveis = [col for col in [
        "Protocolo", "Centro coordenador", "Nome do patrocinador", "Investigador PI",
        "Status do contrato", "Tempo até resposta", "Tempo até aprovação", "Tempo da aprovação até a assinatura", "Tempo até a assinatura", "Obsevações do contrato", "Tempo ate a resposta",
        "até aprovação", "Aprovação até a assinatura","Até a assinatura"
    ] if col in df_modificado.columns]

    colunas_selecionadas = st.multiselect("Selecione as colunas para visualizar:", colunas_disponiveis, default=colunas_disponiveis)
    st.dataframe(df_modificado[colunas_selecionadas])

#TODO Aba Orcamentos
with ORCAMENTOS:
    st.sidebar.write("-------------------------------------------------------------")
    # orcamentos_delta1 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"]
    # orcamentos_Delta1Filtro = st.sidebar.selectbox("TEMPO ATÉ RESPOSTA DO ORÇAMENTO", orcamentos_delta1)

    # orcamentos_Delta2Filtro = st.sidebar.selectbox("DECORRIDO DE RESPOSTA ATÉ APROVADO EM ORÇAMENTO", orcamentos_delta1)

    # orcamentos_Delta3Filtro = st.sidebar.selectbox("TEMPO NO ORÇAMENTO", orcamentos_delta1)

    # if orcamentos_delta1 != "Geral":
    #     df_modificado = df_modificado[df_modificado['TEMPO ATÉ RESPOSTA DO ORÇAMENTO'] == orcamentos_delta1]

    #TODO: Delta 1
    with st.expander("Delta 1"):
        st.markdown("Tempo até resposta do orçamento:<br>", unsafe_allow_html=True)
        
    orca1, orca2 = st.columns(2)
    with orca1:
        contagem = df_modificado['Tempo ate a resposta'].value_counts().reindex(status_opcoes[1:], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação do Delta 1", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True)

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