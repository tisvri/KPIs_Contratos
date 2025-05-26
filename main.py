
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import graficos
import deltas
import altair as alt


# TODO Configuração da página
st.set_page_config(page_title="KPIs", layout="wide")

# TODO Carregamento de dados
df_modi = deltas.deltaContratos()
df_modificado = df_modi.copy()
#print(df_modificado)

#TODO FILTROS LATERAIS:
BaseDeDados = st.sidebar.radio("Selecione a base de dados",
                        ["Em andamento",
                        "Assinado",
                        "Geral",],
                        index=None)

protocolo_options = sorted(df_modificado['Protocolo'].unique())
protocoloFiltro = st.sidebar.multiselect("Selecione o Protocolo", options=protocolo_options)

centro_options = sorted(df_modificado['Centro coordenador'].unique())
CentroFiltro = st.sidebar.multiselect("Selecione o Centro", options=centro_options, key=68)

pi_options = sorted(df_modificado['Investigador PI'].unique())
PiFiltro = st.sidebar.multiselect("Selecione o PI", options=pi_options)

sponsor_options = sorted(df_modificado['Nome do patrocinador'].unique())
sponsorFiltro = st.sidebar.multiselect("Selecione o Sponsor", options=sponsor_options)

st.sidebar.write("---------------Contratos---------------")

status_opcoes = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"]
Delta1Filtro = st.sidebar.selectbox("Status delta 1", status_opcoes)

status_delta2 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente"]
Delta2Filtro = st.sidebar.selectbox("Status delta 2", status_delta2)

status_delta3 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"]
Delta3Filtro = st.sidebar.selectbox("Status delta 3", status_delta3)

status_delta4 = ["Geral", "Sem informação","Tempo bom", "Atenção", "Atrasado"]
Delta4Filtro = st.sidebar.selectbox("Status delta 4", status_delta4)

st.sidebar.write("--------------Orçamentos--------------")

orcamentos_delta1 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente", "Atrasado"]
orcamentos_Delta1Filtro = st.sidebar.selectbox("TEMPO ATÉ RESPOSTA DO ORÇAMENTO", orcamentos_delta1)

orcamentos_delta2 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente"]
orcamentos_Delta2Filtro = st.sidebar.selectbox("DECORRIDO DE RESPOSTA ATÉ APROVADO EM ORÇAMENTO", ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente"])

orcamentos_delta3 = ["Geral", "Sem informação", "Bom", "Atenção", "Atrasado"]
orcamentos_Delta3Filtro = st.sidebar.selectbox("TEMPO NO ORÇAMENTO", orcamentos_delta3)

st.sidebar.write("--------------Regulatório--------------")

regulatorio_delta1 = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente"]
regulatorio_Delta1Filtro = st.sidebar.selectbox("Tempo no regulatório", regulatorio_delta1)

st.sidebar.write("--------------Geral--------------")

geral_ativacao = ["Geral", "Sem informação", "No prazo", "Alerta", "Urgente"]
geral_ativacaoFiltro = st.sidebar.selectbox("Tempo no regulatório", geral_ativacao, key=69)





#TODO: Deltas selecionados

if BaseDeDados == "Em andamento":
    df_modificado = df_modificado[~df_modificado['Status do contrato'].isin(['Assinado'])]
elif BaseDeDados == "Assinado":
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

#Orçamentos
if orcamentos_Delta1Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['resposta do orçamento'] == orcamentos_Delta1Filtro]

if orcamentos_Delta2Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['resposta até aprovado em orçamento'] == orcamentos_Delta2Filtro]

if orcamentos_Delta3Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Tempo geral no orçamento'] == orcamentos_Delta3Filtro]

#Regulatorio
if regulatorio_Delta1Filtro != "Geral":
    df_modificado = df_modificado[df_modificado['Tempo regulatório'] == regulatorio_Delta1Filtro]

#Geral 
if geral_ativacaoFiltro != "Geral":
    df_modificado = df_modificado[df_modificado['ativação do centro após todo o fluxo'] == geral_ativacaoFiltro]

if CentroFiltro:
        df_modificado = df_modificado[df_modificado['Centro coordenador'].isin(CentroFiltro)]

if protocoloFiltro:
        df_modificado = df_modificado[df_modificado['Protocolo'].isin(protocoloFiltro)]

#TODO: Abas
CONTRATOS, ORCAMENTOS, REGULATORIO, GERAL = st.tabs(["**CONTRATOS**", "**ORÇAMENTOS**", "**REGULATÓRIO**", "**GERAL**"])

    
# TODO: Aba Contratos
with CONTRATOS:

    #TODO: Delta 1
    with st.expander("Delta 1"):
        st.markdown("O delta 1 consiste no tempo decorido da data de recebimento do contrato ate o tempo de resposta:<br>< 5 dias No prazo<br>5 - 9 dias Alerta<br>10 - 14 dias Urgente<br>15+ dias Atrasado", unsafe_allow_html=True)

    graf1, graf2 = st.columns(2)
    with graf1:
        contagem = df_modificado['Tempo ate a resposta'].value_counts().reindex(status_opcoes[1:], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação do tempo até resposta", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True, key="1")
    with graf2:
        #       st.plotly_chart(graficos.grafico_horizontal_por_coluna(df_modificado,'Investigador PI', 'Contratos por Investigador PI'), use_container_width=True, key="2")

        # Agrupamento e contagem
        df_grouped = df_modificado.groupby(['Tempo ate a resposta', 'Investigador PI']).size().reset_index(name='Quantidade')

        # Renomeia colunas para facilitar o uso no Streamlit
        df_grouped = df_grouped.rename(columns={
            'Investigador PI': 'Investigador',
            'Tempo ate a resposta': 'status'
        })

        cores_personalizadas = {
            "Sem informação": "gray",
            "No prazo": "green",
            "Alerta": "orange",
            "Urgente": "red",
            "Atrasado": "lightblue"
        }
        
        # Gráfico com Altair (barras horizontais)
        chart = alt.Chart(df_grouped).mark_bar().encode(
            y=alt.Y('Investigador:N', sort='-x', axis=alt.Axis(grid=False, domain=False)),
            x=alt.X('Quantidade:Q', axis=alt.Axis(grid=False, domain=False)),
            #color='status:N',
            color=alt.Color('status:N', scale=alt.Scale(domain=list(cores_personalizadas.keys()), range=list(cores_personalizadas.values()))),

            tooltip=['Investigador', 'status', 'Quantidade']
        ).properties(
            width='container',
            height=500
        )

        st.altair_chart(chart, use_container_width=True, key="60")

    #TODO: Delta 2
    with st.expander("Delta 2"):
        st.markdown("O delta 2 consiste no tempo decorido da resposta do contrato até a data de aprovação:<br>< 15 dias No prazo<br>15 - 29 dias Alerta<br>30+ dias Urgente", unsafe_allow_html=True)

    graf3, graf4 = st.columns(2)
    with graf3:
        contagem = df_modificado['até aprovação'].value_counts().reindex(["Sem informação", "No prazo", "Alerta", "Urgente"], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação do tempo até aprovação", ["gray", "green", "orange", "red"]), use_container_width=True, key="3")
    with graf4:
        st.plotly_chart(graficos.grafico_horizontal_por_coluna(df_modificado,'Nome do patrocinador', 'Contratos por Sponsor'), use_container_width=True, key="4")

    #TODO: Delta 3
    with st.expander("Delta 3"):
        st.markdown("O delta 3 consistem na data de aprovação até a data de assinatura:<br>< 5 dias No prazo<br>5 - 9 dias Alerta<br>10 - 14 dias Urgente<br>15+ dias Atrasado", unsafe_allow_html=True)

    graf5, graf6 = st.columns(2)
    with graf5:
        contagem = df_modificado['Aprovação até a assinatura'].value_counts().reindex(status_delta3[1:], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação do tempo da aprovação até a assinatura", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True, key="5")
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
            y=alt.Y('Sponsor:N', sort='-x', axis=alt.Axis(grid=False, domain=False)),
            x=alt.X('Quantidade:Q', axis=alt.Axis(grid=False, domain=False)),
            color='Investigador:N',
            tooltip=['Investigador', 'Quantidade']
        ).properties(
            width='container',
            height=500
        )

        st.altair_chart(chart, use_container_width=True, key="6")

    #TODO: Delta 4
    with st.expander("Delta 4"):
        st.markdown("O delta 4 consiste no tempo que demorou ate a assinatura:<br><= 24 dias: Tempo Bom<br>25 - 59 dias: Atenção<br>60+ dias Atrasado", unsafe_allow_html=True)

    graf7, graf8 = st.columns(2)
    with graf7:
        contagem = df_modificado['Até a assinatura'].value_counts().reindex(["Sem informação","Tempo bom", "Atenção", "Atrasado"], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação do tempo até a assinatura", ["gray","green", "orange", "red"]), use_container_width=True, key="7")
    with graf8:
        # Agrupamento e contagem
        df_grouped = df_modificado.groupby(['Status do contrato', 'Até a assinatura']).size().reset_index(name='Quantidade')

        # Renomeia colunas para facilitar o uso no Streamlit
        df_grouped = df_grouped.rename(columns={
            'Status do contrato': 'Status',
            'Até a assinatura': 'Até a assinatura'
        })

        cores_personalizadas = {
            "Sem informação": "gray",
            "Tempo bom": "green",
            "Atenção": "orange",
            "Atrasado": "red"
        }

        # Gráfico de barras horizontais com Altair
        chart = alt.Chart(df_grouped).mark_bar().encode(
            y=alt.Y('Status:N', sort='-x', axis=alt.Axis(grid=False, domain=False), title='Status do Contrato'),
            x=alt.X('Quantidade:Q', axis=alt.Axis(grid=False, domain=False), title='Quantidade'),
            #color=alt.Color('Até a assinatura:N', title='Até a assinatura'),
            color=alt.Color('Até a assinatura:N', title='Até a assinatura', scale=alt.Scale(domain=list(cores_personalizadas.keys()), range=list(cores_personalizadas.values()))),
            tooltip=['Até a assinatura', 'Quantidade']
        ).properties(
            width='container',
            height=500,
            title='Quantidade por Status do Contrato e até a assinatura'
        )

        # Exibe o gráfico no Streamlit
        st.altair_chart(chart, use_container_width=True, key="8")

    #TODO: SLA

    sla1, sla2, sla3, sla4 = st.columns(4)
    with sla1:
        # Dados de contagem
        contagem = df_modificado['Tempo ate a resposta'].value_counts().reindex(status_opcoes[1:], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            graficos.grafico_pizza(contagem, "Delta 1", 
                        ["gray", "green", "orange", "red", "lightblue"]),
            use_container_width=True
        )

    with sla2:
        # Dados de contagem
        contagem = df_modificado['até aprovação'].value_counts().reindex(status_opcoes[1:], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            graficos.grafico_pizza(contagem, "Delta 2", 
                        ["gray", "green", "orange", "red", "lightblue"]),
            use_container_width=True
        )

    with sla3:
        # Dados de contagem
        contagem = df_modificado['Aprovação até a assinatura'].value_counts().reindex(status_opcoes[1:], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            graficos.grafico_pizza(contagem, "Delta 3", 
                        ["gray", "green", "orange", "red", "lightblue"]),
            use_container_width=True
        )
    with sla4:
        # Dados de contagem
        contagem = df_modificado['Até a assinatura'].value_counts().reindex(["Sem informação","Tempo bom", "Atenção", "Atrasado"], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            graficos.grafico_pizza(contagem, "Delta 4", 
                        [ "gray", "green","orange", "red", "lightblue"]),
            use_container_width=True
        )

    #TODO: tabela
    st.subheader("Tabela Geral")
    colunas_disponiveis = [col for col in [
        "Protocolo", "Centro coordenador", "Nome do patrocinador", "Investigador PI",
        "Status do contrato", "Tempo ate a resposta",
        "até aprovação", "Aprovação até a assinatura","Até a assinatura", "Obsevações do contrato"
    ] if col in df_modificado.columns]

    colunas_selecionadas = st.multiselect("Selecione as colunas para visualizar:", colunas_disponiveis, default=colunas_disponiveis)
    st.dataframe(df_modificado[colunas_selecionadas])

#TODO Aba Orcamentos
with ORCAMENTOS:
    #TODO: Delta 1
    with st.expander("Delta 1"):
        st.markdown("O delta 1 consiste no tempo decorido do cadastro do orçamento até resposta:<br>< 5 dias: No prazo<br>5 - 9 dias: Alerta<br> 10 - 14 dias: Urgente<br>15+ dias: Atrasado", unsafe_allow_html=True)
        

    orca1, orca2 = st.columns(2)
    with orca1:
        contagem = df_modificado['resposta do orçamento'].value_counts().reindex(["Sem informação","No prazo","Alerta", "Urgente", "Atrasado"], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação do cadastro do orçamento até resposta", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True, key="9")
    with orca2:        
        df_grouped = df_modificado.groupby(['resposta do orçamento', 'Centro coordenador']).size().reset_index(name='Quantidade')

        # Renomeia colunas para facilitar o uso no Streamlit
        df_grouped = df_grouped.rename(columns={
            'Centro coordenador': 'Centro',
            'resposta do orçamento': 'status'
        })

        cores_personalizadas = {
            "Sem informação": "gray",
            "No prazo": "green",
            "Alerta": "orange",
            "Urgente": "red",
            "Atrasado": "lightblue"
        }
        
        # Gráfico com Altair (barras horizontais)
        chart = alt.Chart(df_grouped).mark_bar().encode(
            y=alt.Y('Centro:N', sort='-x', axis=alt.Axis(grid=False, domain=False)),
            x=alt.X('Quantidade:Q', axis=alt.Axis(grid=False, domain=False)),
            #color='status:N',
            color=alt.Color('status:N', scale=alt.Scale(domain=list(cores_personalizadas.keys()), range=list(cores_personalizadas.values()))),

            tooltip=['Centro', 'status', 'Quantidade']
        ).properties(
            width='container',
            height=500
        )

        st.altair_chart(chart, use_container_width=True, key="61")

    with st.expander("Delta 2"):
        st.markdown("O delta 2 e o tempo decorrido da resposta até a data de aprovação dos orçamentos :<br>< 15 dias: No prazo<br>15 - 29 dias: Alerta<br>30+ dias: Urgente", unsafe_allow_html=True)
    orca3, orca4 = st.columns(2)
    with orca3:
        contagem = df_modificado['resposta até aprovado em orçamento'].value_counts().reindex(["Sem informação","No prazo", "Alerta", "Urgente"], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação da resposta até a data de aprovação", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True, key="11")
    with orca4:
        #st.plotly_chart(graficos.grafico_horizontal_por_coluna(df_modificado,'Nome do patrocinador', 'Sponsor'), use_container_width=True, key="12")
        df_grouped = df_modificado.groupby(['resposta até aprovado em orçamento', 'Nome do patrocinador']).size().reset_index(name='Quantidade')

        # Renomeia colunas para facilitar o uso no Streamlit
        df_grouped = df_grouped.rename(columns={
            'Nome do patrocinador': 'Nome do patrocinador',
            'resposta até aprovado em orçamento': 'status'
        })

        cores_personalizadas = {
            "Sem informação": "gray",
            "No prazo": "green",
            "Alerta": "orange",
            "Urgente": "red"}
        
        # Gráfico com Altair (barras horizontais)
        chart = alt.Chart(df_grouped).mark_bar().encode(
            y=alt.Y('Nome do patrocinador:N', sort='-x', axis=alt.Axis(grid=False, domain=False)),
            x=alt.X('Quantidade:Q', axis=alt.Axis(grid=False, domain=False)),
            #color='status:N',
            color=alt.Color('status:N', scale=alt.Scale(domain=list(cores_personalizadas.keys()), range=list(cores_personalizadas.values()))),

            tooltip=['Nome do patrocinador', 'status', 'Quantidade']
        ).properties(
            width='container',
            height=500
        )

        st.altair_chart(chart, use_container_width=True, key="62")


    with st.expander("Delta 3"):
        st.markdown("O delta 3 e o tempo geral no orçamento:<br>< 19 dias: Bom<br>20 - 44 dias: Atenção<br>45+ dias: Atrasado", unsafe_allow_html=True)
    orca5, orca6 = st.columns(2)
    with orca5:
        contagem = df_modificado['Tempo geral no orçamento'].value_counts().reindex(["Sem informação","Tempo bom", "Atenção", "Atrasado"], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação tempo geral no orçamento", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True, key="13")
    with orca6:        
        # Agrupamento e contagem
        df_grouped = df_modificado.groupby(['Status do orcamento', 'Tempo geral no orçamento']).size().reset_index(name='Quantidade')

        # Renomeia colunas para facilitar o uso no Streamlit
        df_grouped = df_grouped.rename(columns={
            'Status do orcamento': 'Status',
            'Tempo geral no orçamento': 'Tempo geral no orçamento'
        })

        cores_personalizadas = {
            "Sem informação": "gray",
            "Tempo bom": "green",
            "Atenção": "orange",
            "Atrasado": "red"
        }

        # Gráfico de barras horizontais com Altair
        chart = alt.Chart(df_grouped).mark_bar().encode(
            y=alt.Y('Status:N', sort='-x', axis=alt.Axis(grid=False, domain=False), title='Status do orcamento'),
            x=alt.X('Quantidade:Q', axis=alt.Axis(grid=False, domain=False), title='Quantidade'),
            color=alt.Color('Tempo geral no orçamento:N', title='Tempo geral no orçamento', scale=alt.Scale(domain=list(cores_personalizadas.keys()), range=list(cores_personalizadas.values()))),
            tooltip=['Tempo geral no orçamento', 'Quantidade']
        ).properties(
            width='container',
            height=500,
            title='Status'
        )

        # Exibe o gráfico no Streamlit
        st.altair_chart(chart, use_container_width=True, key="8")

    
    sla1, sla2, sla3 = st.columns(3)
    with sla1:
        # Dados de contagem
        contagem = df_modificado['resposta do orçamento'].value_counts().reindex(status_opcoes[1:], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            graficos.grafico_pizza(contagem, "Delta 1", 
                        ["gray", "green", "orange", "red", "lightblue"]),
            use_container_width=True , key="15"
        )
    with sla2:
        # Dados de contagem
        contagem = df_modificado['resposta até aprovado em orçamento'].value_counts().reindex(status_opcoes[1:], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            graficos.grafico_pizza(contagem, "Delta 2", 
                        ["gray", "green", "orange", "red", "lightblue"]),
            use_container_width=True, key="16"
        )
    with sla3:
        # Dados de contagem
        contagem = df_modificado['Tempo geral no orçamento'].value_counts().reindex(["Sem informação","Tempo bom", "Atenção", "Atrasado"], fill_value=0)

        # Exibe o gráfico no Streamlit
        st.plotly_chart(
            graficos.grafico_pizza(contagem, "Delta 3", 
                        ["gray", "green", "orange", "red"]),
            use_container_width=True, key="17"
        )

    
    st.subheader("Tabela Geral")
    colunas_disponiveis = [col for col in [
        "Protocolo", "Centro coordenador", "Nome do patrocinador", "Investigador PI",
        "Status do orcamento", "resposta do orçamento",
        "resposta até aprovado em orçamento", "Tempo geral no orçamento", "Obsevações do orçamento"
    ] if col in df_modificado.columns]

    colunas_selecionadas = st.multiselect("Selecione as colunas para visualizar:", colunas_disponiveis, default=colunas_disponiveis)
    st.dataframe(df_modificado[colunas_selecionadas])

#TODO Aba regulatorio
with REGULATORIO:
    with st.expander("Delta"):
        st.markdown("Tempo decorido no processo do regulatório:<br>< 15 dias: No prazo<br>15 - 29 dias: Alerta<br>30+ dias: Urgente", unsafe_allow_html=True)

    regul1, regul2 = st.columns(2)
    with regul1:
        contagem = df_modificado['Tempo regulatório'].value_counts().reindex(["Sem informação","No prazo", "Alerta", "Urgente"], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação do processo do regulatório:", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True, key="18")
    with regul2:
        df_grouped = df_modificado.groupby(['Tempo regulatório', 'Centro coordenador']).size().reset_index(name='Quantidade')

        # Renomeia colunas para facilitar o uso no Streamlit
        df_grouped = df_grouped.rename(columns={
            'Centro coordenador': 'Centro',
            'Tempo regulatório': 'status'
        })

        cores_personalizadas = {
            "Sem informação": "gray",
            "No prazo": "green",
            "Alerta": "orange",
            "Urgente": "red"
        }
        
        # Gráfico com Altair (barras horizontais)
        chart = alt.Chart(df_grouped).mark_bar().encode(
            y=alt.Y('Centro:N', sort='-x', axis=alt.Axis(grid=False, domain=False)),
            x=alt.X('Quantidade:Q', axis=alt.Axis(grid=False, domain=False), title='Quantidade'),
            #color='status:N',
            color=alt.Color('status:N', scale=alt.Scale(domain=list(cores_personalizadas.keys()), range=list(cores_personalizadas.values()))),

            tooltip=['Centro', 'status', 'Quantidade']
        ).properties(
            width='container',
            height=500
        )

        st.altair_chart(chart, use_container_width=True, key="19")




    # Dados de contagem
    contagem = df_modificado['Tempo regulatório'].value_counts().reindex(status_opcoes[1:], fill_value=0)

    # Exibe o gráfico no Streamlit
    st.plotly_chart(
        graficos.grafico_pizza(contagem, "Distribuição do status no regulatorio", 
                    ["gray", "green", "orange", "red", "lightblue"]),
        use_container_width=True, key="20"
    )    

    st.subheader("Tabela Geral")
    colunas_disponiveis = [col for col in [
        "Protocolo", "Centro coordenador", "Nome do patrocinador", "Investigador PI",
        "Status do regulatório", "Tempo regulatório", "Obsevações do regulatório"
    ] if col in df_modificado.columns]

    colunas_selecionadas = st.multiselect("Selecione as colunas para visualizar:", colunas_disponiveis, default=colunas_disponiveis)
    st.dataframe(df_modificado[colunas_selecionadas])

#TODO Aba geral
with GERAL:
    with st.expander("Geral"):
        st.markdown("Tempo até a ativação do centro:<br>< 15 dias: No prazo<br>15 - 29 dias: Alerta<br>30+ dias: Urgente", unsafe_allow_html=True)
    
    geral1, geral2 = st.columns(2)
    with geral1:
        contagem = df_modificado['ativação do centro após todo o fluxo'].value_counts().reindex(["Sem informação","No prazo", "Alerta", "Urgente"], fill_value=0)
        st.plotly_chart(graficos.grafico_barras(contagem, "Classificação ativação de centro", ["gray", "green", "orange", "red", "lightblue"]), use_container_width=True, key="21")
    with geral2:
        df_grouped = df_modificado.groupby(['ativação do centro após todo o fluxo', 'Centro coordenador']).size().reset_index(name='Quantidade')

        # Renomeia colunas para facilitar o uso no Streamlit
        df_grouped = df_grouped.rename(columns={
            'Centro coordenador': 'Centro',
            'ativação do centro após todo o fluxo': 'status'
        })

        cores_personalizadas = {
            "Sem informação": "gray",
            "No prazo": "green",
            "Alerta": "orange",
            "Urgente": "red",
            "Atrasado": "lightblue"
        }
        
        # Gráfico com Altair (barras horizontais)
        chart = alt.Chart(df_grouped).mark_bar().encode(
            y=alt.Y('Centro:N', sort='-x', axis=alt.Axis(grid=False, domain=False)),
            x=alt.X('Quantidade:Q', axis=alt.Axis(grid=False, domain=False)),
            #color='status:N',
            color=alt.Color('status:N', scale=alt.Scale(domain=list(cores_personalizadas.keys()), range=list(cores_personalizadas.values()))),

            tooltip=['status', 'Quantidade']
        ).properties(
            width='container',
            height=500
        )

        st.altair_chart(chart, use_container_width=True, key="61")




     # Dados de contagem
    # contagem = df_modificado['ativação do centro após todo o fluxo'].value_counts().reindex(status_opcoes[1:], fill_value=0)
    # # Exibe o gráfico no Streamlit
    # st.plotly_chart(
    #     graficos.grafico_pizza(contagem, "status geral", 
    #             ["gray", "green", "orange", "red", "lightblue"]),
    #     use_container_width=True , key="22"
    # )

    geral3, geral4 = st.columns(2)
    with geral3:
        contagem = df_modificado['Status'].value_counts()
        st.plotly_chart(graficos.grafico_barras(contagem, 'Status Geral', ["gray", "green", "orange", "red", "lightblue"] ), use_container_width=True, key="65")

    with geral4:
        df_grouped = df_modificado.groupby(['Status', 'Centro coordenador']).size().reset_index(name='Quantidade')

        # Renomeia colunas para facilitar o uso no Streamlit
        df_grouped = df_grouped.rename(columns={
            'Centro coordenador': 'Centro',
            'Status': 'status'
        })

        cores_personalizadas = {
            "Recrutamento aberto": "gray",
            "Qualificado": "green",
            "Em apreciação Ética": "orange",
            "Aguardando Ativação do Centro": "red",
            "Fase Contratual": "lightblue"
        }
        
        # Gráfico com Altair (barras horizontais)
        chart = alt.Chart(df_grouped).mark_bar().encode(
            y=alt.Y('Centro:N', sort='-x', axis=alt.Axis(grid=False, domain=False)),
            x=alt.X('Quantidade:Q', axis=alt.Axis(grid=False, domain=False)),
            #color='status:N',
            color=alt.Color('status:N', scale=alt.Scale(domain=list(cores_personalizadas.keys()), range=list(cores_personalizadas.values()))),

            tooltip=['status', 'Quantidade']
        ).properties(
            width='container',
            height=500
        )

        st.altair_chart(chart, use_container_width=True, key="66")


    st.subheader("Tabela Geral")
    colunas_disponiveis = [col for col in [
        "Protocolo", "Centro coordenador", "Nome do patrocinador", "Investigador PI", "Dados da CRO responsável", "Status", "Contato na CRO", "Data de cadastro",
        "Data do recebimento do contrato", "Data da resposta do contrato", "Data da aprovação do contrato", "Data da assinatura do contrato", "Tempo ate a resposta", "até aprovação", "Aprovação até a assinatura","Até a assinatura", "Status do contrato", "Obsevações do contrato", 
        "Data do recebimento do orçamento", "Data da resposta do orçamento", "Data da aprovação do orçamento","resposta do orçamento","resposta até aprovado em orçamento", "Tempo geral no orçamento", "Status do orcamento", "Obsevações do orçamento", 
        "Data de submissão regulatória", "Data de aprovação regulatória", "Tempo regulatório", "Status do regulatório", "Obsevações do regulatório",
        "Data de ativação do centro", "Tempo até ativação do centro após todo o fluxo"


    ] if col in df_modificado.columns]

    colunas_selecionadas = st.multiselect("Selecione as colunas para visualizar:", colunas_disponiveis, default=colunas_disponiveis)
    st.dataframe(df_modificado[colunas_selecionadas])