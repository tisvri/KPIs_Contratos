import plotly.graph_objects as go


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
            
            textinfo='label+text',
            hoverinfo='label+percent+value'
        )],
        layout=go.Layout(
            title=titulo,
            margin=dict(l=0, r=0, t=40, b=0)
        )
    )