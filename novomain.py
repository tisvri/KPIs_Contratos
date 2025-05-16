import streamlit as st
import dados
import pandas as pd
import itertools


# TODO Configuração da página
st.set_page_config(page_title="KPIs", layout="wide")
hoje = pd.Timestamp.today()


# TODO Carregamento de dados
df_geral = dados.df_geral.copy()
df_modificado = df_geral

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

for cad, resp, apro, ateassi, assina in itertools.zip_longest(df_modificado['Data do recebimento do contrato'], df_modificado['Tempo até resposta'], df_modificado['Tempo até aprovação'], df_modificado['Tempo da aprovação até a assinatura'], df_modificado['Tempo até a assinatura']):
    # Tempo até resposta
    if pd.isna(resp):
        if pd.isna(cad):
            tempo_resposta.append('sem dados')
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
            tempo_aprovacao.append('sem dados')
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
            tempo_ate_assinatura.append('sem dados') 
        else:
            pass

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
        if pd.isna(ateassi):
            tempo_total_assinatura.append('sem dados')
        else:
            pass
         
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

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#TODO FILTROS LATERAIS:
BaseDeDados = st.sidebar.radio("Selecione a base de dados",
                        ["Em andamento",
                        "Concluidos",
                        "Geral",],
                        index=None)


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


#TODO: Deltas selecionados

if BaseDeDados == "Em andamento":
    df_modificado = df_modificado[~df_modificado['Status do contrato'].isin(['Assinado']) & ~df_modificado['Status do contrato'].isin(['Não recebido'])]
elif BaseDeDados == "Concluidos":
    df_modificado = df_modificado[df_modificado['Status do contrato'].isin(['Assinado'])]

if Delta1Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Tempo até resposta'] == Delta1Filtro]

if Delta2Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Tempo até aprovação'] == Delta2Filtro]

if Delta3Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Tempo da aprovação até a assinatura'] == Delta3Filtro]

if Delta4Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Tempo até a assinatura'] == Delta4Filtro]

if PiFiltro:
        df_modificado = df_modificado[df_modificado['Investigador PI'].isin(PiFiltro)]

if sponsorFiltro:
    df_modificado = df_modificado[df_modificado['Nome do patrocinador'].isin(sponsorFiltro)]





#TODO TABELA
st.subheader("Tabela Geral")
colunas_disponiveis = [col for col in [
        "Protocolo",
        "Tempo até resposta", "Tempo até aprovação", "Tempo da aprovação até a assinatura", "Tempo até a assinatura", "Obsevações do contrato", "Tempo ate a resposta",
        "até aprovação", "Aprovação até a assinatura","Até a assinatura"
    ] if col in df_modificado.columns]

colunas_selecionadas = st.multiselect("Selecione as colunas para visualizar:", colunas_disponiveis, default=colunas_disponiveis)
st.dataframe(df_modificado[colunas_selecionadas])