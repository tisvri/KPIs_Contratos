# TODO: Bibliotecas

import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import requests
from urllib.parse import urljoin
from datetime import datetime, timedelta 
from io import BytesIO
import time


#----------------------------------------------------------------------------------------------- 
# TODO: Carregar as variáveis de ambiente
load_dotenv()

api_username = os.getenv('API_USERNAME')
api_password = os.getenv('API_PASSWORD')
api_url = os.getenv("API_URL")

# TODO: funções globais
# Obter o mês e o ano do mês atual menos 1 ano
dia_atual = datetime.now().day
mes_atual = datetime.now().month - 0
ano_anterior = datetime.now().year - 1
proximas_duas_semanas = (datetime.now()+timedelta(days=15)).strftime('%Y-%m-%d')

# TODO: API 
# Corpo do login a ser utilizado no acesso
body = {
    "nome": api_username,
    "password":api_password
}

# Obtençao do token de acesso à polotrial
auth_url = urljoin(api_url, "/sessions")

response = requests.post(auth_url, json = body)

# Extraindo o token
token = response.json()["token"]

# Incorporando a string Bearer para inserir
if token:
    auth_token = "Bearer " + token
    # print(f"Auth Token: {auth_token}")
else:
    print("Falha ao obter o token.")
    
    
url_request = "https://api.polotrial.com"

headers = {"Authorization": auth_token}

# TODO: Extrair ultima informacao

def extrair_ultima_informacao(x):
    if x is None:
        return None
    else:
        values_list = list(x.values())
        if len(values_list) == 0:
            return None
        else:
            return values_list[-1]
        

# TODO: Generica

rota_generica = url_request+"/generica?nested=true"
df_generica = requests.get(rota_generica, headers = headers).json()
df_generica = pd.DataFrame(df_generica)
df_generica_limpo=df_generica[['id', 'ds_descricao']]


# TODO:PROTOCOLO

rota_protocolo = url_request+"/protocolo?nested=true"
df_protocolo = requests.get(rota_protocolo, headers = headers).json()
df_protocolo = pd.DataFrame(df_protocolo)

# Lista de colunas de datas relevantes
colunas_datas = [
    'data_recebimento_contrato',
    'data_resposta_contrato',
    'data_aprovacao_contrato',
    'data_assinatura_contrato',
    'data_recebimento_orcamento',
    'data_resposta_orcamento',
    'data_aprovacao_orcamento',
    'data_submissao_regulatorio',
    'data_aprovacao_regulatorio'
]

#TODO: Lambidas

# Converter para datetime (caso ainda não estejam nesse formato)
for col in colunas_datas:
    df_protocolo[col] = pd.to_datetime(df_protocolo[col], errors='coerce')

df_protocolo['Tempo_ate_resposta'] = df_protocolo['data_resposta_contrato'] - df_protocolo['data_recebimento_contrato'] 

df_protocolo['Tempo_ate_aprovacao'] = df_protocolo['data_aprovacao_contrato'] - df_protocolo['data_recebimento_contrato'] 

df_protocolo['Tempo_aprova_ate_assina'] = df_protocolo['data_assinatura_contrato'] - df_protocolo['data_aprovacao_contrato'] 

df_protocolo['Tempo_total_precesso_assinatura'] = df_protocolo['data_assinatura_contrato'] - df_protocolo['data_recebimento_contrato'] 


df_protocolo['Tempo_ate_resposta_orcamento'] = df_protocolo['data_resposta_orcamento'] - df_protocolo['data_recebimento_orcamento']

df_protocolo['Tempo_respo_apro_orcamento'] = df_protocolo['data_resposta_orcamento'] - df_protocolo['data_aprovacao_orcamento']

df_protocolo['Tempo_total_recbi_apro_orcamento'] = df_protocolo['data_aprovacao_orcamento'] - df_protocolo['data_recebimento_orcamento']

df_protocolo['Tempo_ate_regulatorio'] = df_protocolo['data_aprovacao_regulatorio'] - df_protocolo['data_submissao_regulatorio']

# Criar a nova coluna com a data mais recente
df_protocolo['data_mais_recente'] = df_protocolo[colunas_datas].max(axis=1)

df_protocolo['data_mais_recente'] = pd.to_datetime(df_protocolo['data_mais_recente'], errors='coerce')
df_protocolo['data_ativacao_centro'] = pd.to_datetime(df_protocolo['data_ativacao_centro'], errors='coerce')


df_protocolo['Tempo_pos_procesos_ate_ativacao'] = df_protocolo['data_ativacao_centro'] - df_protocolo['data_mais_recente']

#TODO: criando o dim_protocolo:
dim_protocolo = df_protocolo[[
    'id',
    'apelido_protocolo',
    'dados_co_centro',
    'dados_pi',
    'status',
    'dados_tipo_de_iniciativa',
    'nome_patrocinador',
    'dados_cro_responsavel',
    'cro_contatos',
    'data_cadastro',
    'data_recebimento_contrato',
    'data_resposta_contrato',
    'data_aprovacao_contrato',
    'data_assinatura_contrato',
    'Tempo_ate_resposta',
    'Tempo_ate_aprovacao',
    'Tempo_aprova_ate_assina',
    'Tempo_total_precesso_assinatura',
    'status_contrato',
    'observacoes_contrato',
    'data_recebimento_orcamento',
    'data_resposta_orcamento',
    'data_aprovacao_orcamento',
    'Tempo_ate_resposta_orcamento',
    'Tempo_respo_apro_orcamento',
    'Tempo_total_recbi_apro_orcamento',
    'status_orcamento',
    'observacoes_orcamento',
    'data_submissao_regulatorio',
    'data_aprovacao_regulatorio',
    'Tempo_ate_regulatorio',
    'status_regulatorio',
    'observacoes_regulatorio',
    'data_ativacao_centro',
    'data_mais_recente',
    'Tempo_pos_procesos_ate_ativacao'
    
]]

extrair_ultima_info = [
    'dados_pi',
    'status',
    'nome_patrocinador',
    'dados_cro_responsavel',
    'dados_tipo_de_iniciativa',
    'dados_co_centro'
    
]


for coluna in extrair_ultima_info:
    if coluna in dim_protocolo.columns:
        dim_protocolo.loc[:, coluna] = dim_protocolo[coluna].apply(extrair_ultima_informacao)
    else:
        print(f"A coluna '{coluna}' não existe no DataFrame.")


df_generica_limpo_contrato = df_generica_limpo.copy()
df_generica_limpo_contrato.rename(columns={'id': 'status_contrato', 'ds_descricao': 'contrato_status'}, inplace=True)
dim_protocolo = dim_protocolo.merge(df_generica_limpo_contrato, on='status_contrato', how='left')
dim_protocolo['status_contrato'] = dim_protocolo['contrato_status']
dim_protocolo = dim_protocolo.drop(columns=['contrato_status'])


df_generica_limpo_contrato = df_generica_limpo.copy()
df_generica_limpo_contrato.rename(columns={'id': 'status_orcamento', 'ds_descricao': 'orcamento_status'}, inplace=True)
dim_protocolo = dim_protocolo.merge(df_generica_limpo_contrato, on='status_orcamento', how='left')
dim_protocolo['status_orcamento'] = dim_protocolo['orcamento_status']
dim_protocolo = dim_protocolo.drop(columns=['orcamento_status'])


df_generica_limpo_contrato = df_generica_limpo.copy()
df_generica_limpo_contrato.rename(columns={'id': 'status_regulatorio', 'ds_descricao': 'regulatorio_status'}, inplace=True)
dim_protocolo = dim_protocolo.merge(df_generica_limpo_contrato, on='status_regulatorio', how='left')
dim_protocolo['status_regulatorio'] = dim_protocolo['regulatorio_status']
dim_protocolo = dim_protocolo.drop(columns=['regulatorio_status'])


dim_protocolo['data_cadastro'] = pd.to_datetime(dim_protocolo['data_cadastro'], errors='coerce').dt.date


# Certifique-se de que as colunas de data estão no formato datetime
for coluna in ['data_recebimento_contrato', 'data_resposta_contrato','data_aprovacao_contrato','data_assinatura_contrato','data_cadastro']:
    dim_protocolo[coluna] = pd.to_datetime(dim_protocolo[coluna], errors='coerce')


# Define a data dos ultimos 2 anos
ano_limite = datetime(datetime.now().year - 2, 1, 1)

# TODO: tirando filtrando o Dim_protocolo

dim_protocolo = dim_protocolo[dim_protocolo['data_cadastro'] > ano_limite]
dim_protocolo = dim_protocolo[dim_protocolo['dados_tipo_de_iniciativa'] == 'Patrocinador']
dim_protocolo = dim_protocolo[(dim_protocolo['status'].isin(['Aprovado pelo CEP'])) | (dim_protocolo['status'].isin(['Em apreciação Ética'])) | (dim_protocolo['status'].isin(['Fase Contratual'])) | (dim_protocolo['status'].isin(['Recrutamento aberto'])) | (dim_protocolo['status'].isin(['Qualificado'])) | (dim_protocolo['status'].isin(['Aguardando Ativação do Centro']))]


#TODO: Re-nomeia as colunas

def renomear_colunas(df):
    mapeamento = {
        'id': 'ID',
        'apelido_protocolo': 'Protocolo',
        'nome_patrocinador': 'Nome do patrocinador',
        'dados_cro_responsavel': 'Dados da CRO responsável',
        'cro_contatos': 'Contato na CRO',
        'dados_tipo_de_iniciativa': 'Tipo de iniciativa',
        'dados_co_centro': 'Centro coordenador',
        'data_cadastro': 'Data de cadastro',
        'data_recebimento_contrato': 'Data do recebimento do contrato',
        'data_resposta_contrato': 'Data da resposta do contrato',
        'data_aprovacao_contrato': 'Data da aprovação do contrato',
        'data_assinatura_contrato': 'Data da assinatura do contrato',
        'status_contrato': 'Status do contrato',
        'Tempo_total_precesso_assinatura': 'Tempo até a assinatura',
        'data_recebimento_orcamento': 'Data do recebimento do orçamento',
        'data_aprovacao_orcamento': 'Data da aprovação do orçamento',
        'Tempo_total_recbi_apro_orcamento': 'Tempo no orçamento',
        'data_submissao_regulatorio': 'Data de submissão regulatória',
        'data_aprovacao_regulatorio': 'Data de aprovação regulatória',
        'Tempo_ate_regulatorio': 'Tempo no regulatório',
        'data_ativacao_centro': 'Data de ativação do centro',
        'Tempo_pos_procesos_ate_ativacao': 'Tempo até ativação do centro após todo o fluxo',
        'data_mais_recente': 'Data do último processo do fluxo',
        'dados_pi': 'Investigador PI',
        'status': 'Status',
        'Tempo_ate_resposta': 'Tempo até resposta',
        'Tempo_ate_aprovacao': 'Tempo até aprovação',
        'Tempo_aprova_ate_assina': 'Tempo da aprovação até a assinatura',
        'Tempo até a assinatura': 'Tempo total',
        'data_resposta_orcamento': 'Data da resposta do orçamento',
        'Tempo_ate_resposta_orcamento': 'Tempo até resposta do orçamento',
        'Tempo_respo_apro_orcamento': 'Tempo decorrido de resposta até aprovado em orçamento',
        'status_regulatorio': 'Status do regulatório',
        'status_orcamento': 'Status do orcamento',
        'observacoes_contrato': 'Obsevações do contrato',
        'observacoes_orcamento': 'Obsevações do orçamento',
        'observacoes_regulatorio': 'Obsevações do regulatório'
        
    }
    return df.rename(columns=mapeamento)

df_geral = renomear_colunas(dim_protocolo)


df_geral.reset_index(drop=True, inplace = True)