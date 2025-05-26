import dados
from datetime import date
import pandas as pd
import itertools


df_geral = dados.df_geral.copy()
df_modificado = df_geral.copy()
hoje = pd.Timestamp.today()

def deltaContratos():
    #-----------------------------------CONTRATOS-------------------------------------
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


#-------------------------------------Orçamentos-----------------------------------
    #TODO Fazendo a clacificacao dos deltas
    df_modificado['Tempo até resposta do orçamento'] = pd.to_timedelta(df_modificado['Tempo até resposta do orçamento'], errors='coerce')
    df_modificado['Tempo decorrido de resposta até aprovado em orçamento'] = pd.to_timedelta(df_modificado['Tempo decorrido de resposta até aprovado em orçamento'], errors='coerce')
    df_modificado['Tempo no orçamento'] = pd.to_timedelta(df_modificado['Tempo no orçamento'], errors='coerce')

    # Criando listas para armazenar os resultados

    tempo_resposta_orcamento = []
    tempo_resp_ate_aprocao_orcamento = []
    tempo_total_orcamento = []


    for resporca, ateapro, temporca in itertools.zip_longest(df_modificado['Tempo até resposta do orçamento'], df_modificado['Tempo decorrido de resposta até aprovado em orçamento'], df_modificado['Tempo no orçamento']):
        if pd.isna(resporca):
            tempo_resposta_orcamento.append('Sem informação')
        elif resporca < pd.Timedelta(days=5):
            tempo_resposta_orcamento.append('No prazo') 
        elif pd.Timedelta(days=5) <= resporca <= pd.Timedelta(days=9):
            tempo_resposta_orcamento.append('Alerta')
        elif pd.Timedelta(days=10) <= resporca <= pd.Timedelta(days=14):
            tempo_resposta_orcamento.append('Urgente')
        elif resporca >= pd.Timedelta(days=15):
            tempo_resposta_orcamento.append('Atrasado')
        
        if pd.isna(ateapro):
            tempo_resp_ate_aprocao_orcamento.append('Sem informação')
        elif ateapro < pd.Timedelta(days=15):
            tempo_resp_ate_aprocao_orcamento.append('No prazo')
        elif pd.Timedelta(days=15) <= ateapro <= pd.Timedelta(days=29):
            tempo_resp_ate_aprocao_orcamento.append('Alerta')
        elif ateapro >= pd.Timedelta(days=30):
            tempo_resp_ate_aprocao_orcamento.append('Urgente')


        if pd.isna(temporca):
            tempo_total_orcamento.append('Sem informação')
        elif temporca <= pd.Timedelta(days=19):
            tempo_total_orcamento.append('Tempo bom')
        elif pd.Timedelta(days=20) <= temporca <= pd.Timedelta(days=44):
            tempo_total_orcamento.append('Atenção')
        elif temporca >= pd.Timedelta(days=45):
            tempo_total_orcamento.append('Atrasado')

    # Atribuindo os resultados às novas colunas
    df_modificado['resposta do orçamento'] = tempo_resposta_orcamento
    df_modificado['resposta até aprovado em orçamento'] = tempo_resp_ate_aprocao_orcamento
    df_modificado['Tempo geral no orçamento'] = tempo_total_orcamento


#-----------------------------------REGULATORIO-------------------------------------

    #TODO Fazendo a clacificacao dos deltas
    df_modificado['Tempo no regulatório'] = pd.to_timedelta(df_modificado['Tempo no regulatório'], errors='coerce')

    # Criando listas para armazenar os resultados
    tempo_regulatorio = []


    for tempregu in df_modificado['Tempo no regulatório']:
        if pd.isna(tempregu):
            tempo_regulatorio.append('Sem informação')
        elif tempregu < pd.Timedelta(days=15):
            tempo_regulatorio.append('No prazo') 
        elif pd.Timedelta(days=15) <= tempregu <= pd.Timedelta(days=29):
            tempo_regulatorio.append('Alerta')
        elif tempregu >= pd.Timedelta(days=29):
            tempo_regulatorio.append('Urgente')

        # Atribuindo os resultados às novas colunas
    df_modificado['Tempo regulatório'] = tempo_regulatorio



#-------------------------------------GERAL-----------------------------------

    #TODO Fazendo a clacificacao dos deltas
    df_modificado['Tempo até ativação do centro após todo o fluxo'] = pd.to_timedelta(df_modificado['Tempo até ativação do centro após todo o fluxo'], errors='coerce')

    # Criando listas para armazenar os resultados
    tempo_ativacao = []


    for tempcentro in df_modificado['Tempo até ativação do centro após todo o fluxo']:
        if pd.isna(tempcentro):
            tempo_ativacao.append('Sem informação')

        elif tempcentro < pd.Timedelta(days=15):
            tempo_ativacao.append('No prazo')

        elif pd.Timedelta(days=15) <= tempcentro <= pd.Timedelta(days=29):
            tempo_ativacao.append('Alerta')

        elif tempcentro >= pd.Timedelta(days=29):
            tempo_ativacao.append('Urgente')

    df_modificado['ativação do centro após todo o fluxo'] = tempo_ativacao

    return df_modificado