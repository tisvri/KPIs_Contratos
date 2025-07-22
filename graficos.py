import plotly.graph_objects as go
import plotly.express as px
import altair as alt
import streamlit as st


# Função de gráfico de barras
def grafico_barras(contagem, titulo, cores):
    return go.Figure(
        data=[go.Bar(x=contagem.index, y=contagem.values, marker_color=cores)],
        layout=go.Layout(
            title=titulo,
            xaxis=dict(
                title="Classificação",
                showgrid=False,
                zeroline=False,
                showline=True
            ),
            yaxis=dict(
                title="Quantidade",
                showgrid=False,
                zeroline=False,
                showline=True
            ),
            bargap=0.4
        )
    )

# Função de gráfico horizontal por PI
def grafico_horizontal_por_coluna(df,coluna, titulo):
    contagem = df[coluna].value_counts()
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
    # Filtra valores diferentes de zero
    contagem_filtrada = contagem[contagem > 0]
    total = contagem_filtrada.sum()
    labels = contagem_filtrada.index
    values = contagem_filtrada.values

    # Ajusta cores para corresponder apenas aos valores filtrados
    cores_filtradas = [cores[list(contagem.index).index(label)] for label in labels]

    return go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            marker_colors=cores_filtradas,
            

            hoverinfo='percent+value'
        )],
        layout=go.Layout(
            title=titulo,
            showlegend=False,
            margin=dict(l=0, r=0, t=40, b=0)
        )
    )


def delta3(df_modificado):
    # Agrupamento e contagem
    df_grouped = df_modificado.groupby(['Nome do patrocinador', 'Investigador PI']).size().reset_index(name='Quantidade')

    # Renomeia colunas
    df_grouped = df_grouped.rename(columns={
        'Nome do patrocinador': 'Sponsor',
        'Investigador PI': 'Investigador'
    })

    # Gráfico de barras horizontais com Plotly
    fig = px.bar(
        df_grouped,
        x='Quantidade',
        y='Sponsor',
        color='Investigador',
        orientation='h',
        hover_data=['Investigador', 'Quantidade'],
        height=500
    )

    # Layout e legenda reposicionada
    fig.update_layout(
        xaxis_title='Quantidade',
        yaxis_title='Sponsor',
        yaxis=dict(categoryorder='total ascending'),
        bargap=0.2,
        margin=dict(l=10, r=10, t=30, b=80),  # mais espaço embaixo
        legend=dict(
            title='Investigador',
            orientation='h',
            x=1,
            xanchor='right',
            y=-0.3,  # legenda abaixo do gráfico
            yanchor='top'
        )
    )

    return fig

def statusgeral(df_modificado):
    # Agrupamento e contagem
    df_grouped = df_modificado.groupby(['Status', 'Centro coordenador']).size().reset_index(name='Quantidade')

    # Renomeia colunas
    df_grouped = df_grouped.rename(columns={
        'Centro coordenador': 'Centro',
        'Status': 'status'
    })

    # Cores personalizadas por status
    cores_personalizadas = {
        "Recrutamento aberto": "gray",
        "Qualificado": "green",
        "Em apreciação Ética": "orange",
        "Aguardando Ativação do Centro": "red",
        "Fase Contratual": "lightblue"
    }

    # Gráfico com Plotly
    fig = px.bar(
        df_grouped,
        x='Quantidade',
        y='Centro',
        color='status',
        orientation='h',
        hover_data=['status', 'Quantidade'],
        height=500,
        color_discrete_map=cores_personalizadas
    )

    # Layout e legenda fora do gráfico
    fig.update_layout(
        xaxis_title='Quantidade',
        yaxis_title='Centro',
        yaxis=dict(categoryorder='total ascending'),
        bargap=0.2,
        margin=dict(l=10, r=10, t=30, b=80),
        legend=dict(
            title='Status',
            orientation='h',
            x=1,
            xanchor='right',
            y=-0.3,
            yanchor='top'
        )
    )

    return fig