import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Carregando os dados do arquivo CSV
try:
    df = pd.read_csv("dados.csv")
except FileNotFoundError:
    st.error("Arquivo não encontrado.")
    st.stop()
except pd.errors.EmptyDataError:
    st.error("O arquivo está vazio.")
    st.stop()
except pd.errors.ParserError:
    st.error("Erro ao analisar o arquivo CSV.")
    st.stop()

# Configurando a página
st.set_page_config(page_title="Dashboard", page_icon="📊")

# Título e logos no topo
st.title("Dashboard")
col1, col2 = st.columns([3, 1])
with col1:
    st.write("## Bem-vindo ao Dashboard")
    st.write("### Setor: NQSP - Gestão de Indicadores")
with col2:
    st.image("logo_hospital.png", width=100)
    st.image("logo_nqsp.jpg", width=100)

# Seleção dos meses
meses_selecionados = st.multiselect("Selecione os meses:", df['Mês'].unique())

# Criando gráficos para cada taxa
def create_graph(title, y_axis_title, traces, color='green'):
    fig = go.Figure()
    for trace in traces:
        fig.add_trace(go.Scatter(x=df['Mês'], y=df[trace], mode='lines', name=trace, line=dict(color=color, dash='dash')))
    fig.update_layout(title=title, xaxis_title="Mês", yaxis_title=y_axis_title)
    if meses_selecionados:
        fig.update_traces(x=[m for m in df['Mês'] if m in meses_selecionados])
    return fig

st.write("### Taxas")
for taxa in ['Taxa de Ocupação (%)', 'Taxa de Infecção (%)', 'Taxa de Mortalidade (%)', 'Taxa de Satisfação (%)']:
    st.plotly_chart(create_graph(f"Gráfico da {taxa}", taxa, [taxa]))

# Criando gráficos para cada quantidade
st.write("### Quantidades")
for quantidade in ['Partos Vaginais SUS', 'Partos Cesáreos SUS', 'Partos Vaginais Particular', 'Partos Cesáreos Particular']:
    cor_linha = 'gray' if 'Vaginais' in quantidade else 'green'
    st.plotly_chart(create_graph(f"Gráfico de {quantidade}", quantidade, [quantidade], color=cor_linha))

# Gráfico para as cirurgias com suas especialidades
st.write("### Cirurgias Realizadas por Especialidade")
especialidades_disponiveis = df.columns.tolist()[5:]  # Pegando as colunas a partir da sexta
especialidades_selecionadas = st.multiselect("Selecione as especialidades:", especialidades_disponiveis, default=[])

if especialidades_selecionadas:
    fig_cirurgias = go.Figure()
    for especialidade in especialidades_selecionadas:
        fig_cirurgias.add_trace(go.Bar(x=df['Mês'], y=df[especialidade], name=especialidade, marker_color='green'))
    fig_cirurgias.update_layout(title="Cirurgias Realizadas por Especialidade", xaxis_title="Mês", yaxis_title="Número de Cirurgias Realizadas")
    if meses_selecionados:
        fig_cirurgias.update_traces(x=[m for m in df['Mês'] if m in meses_selecionados])
    st.plotly_chart(fig_cirurgias, use_container_width=True)
else:
    st.write("Selecione pelo menos uma especialidade para visualizar o gráfico.")
