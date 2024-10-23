#pip install streamlit
#pip install streamlit_option_menu

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu 
from query import conexao


# *** PRIMEIRA CONSULTA / ATUALIZACOES DE DADOS ***
query = "SELECT * FROM tb_carros"


# Carregar os dados 
df = conexao(query)


#Botao para atualizar 
if st.button("Atualizar Dados"):
    df = conexao(query)


# *** ESTRUTURA LATERAL DE FILTROS ***
st.sidebar.header("Selecione o filtro")

marca = st.sidebar.multiselect("Marca Selecionada", #Nome do seletor
                               options=df["marca"].unique(), #Opcoes disponiveis no nosso DF
                               default=df["marca"].unique()) 

modelo = st.sidebar.multiselect("Modelo Selecionado",
                                options=df["modelo"].unique(),
                                default=df["modelo"].unique())

ano = st.sidebar.multiselect("Ano Selecionado",
                             options=df["ano"].unique(),
                             default=df["ano"].unique())

valor = st.sidebar.multiselect("Valor Selecionado",
                               options=df["valor"].unique(),
                               default=df["valor"].unique())

numero_vendas = st.sidebar.multiselect("Numero de vendas Selecionado",
                               options=df["numero_vendas"].unique(),
                               default=df["numero_vendas"].unique())

#Aplicar os filtros selecionados
df_selecionado = df[
    (df["marca"].isin(marca)) &
    # SELECT * FROM tb_carro WHERE marca = marca_p
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["numero_vendas"].isin(numero_vendas))
]

# *** EXIBIR VALORES MEDIOS - ESTATISTICA  ***
def Home():
    with st.expander("Tabela"): # Cria uma caixa expansivel com um titulo
        mostrarDados = st.multiselect("Filter: ", df_selecionado, default=[])

    #Verifica se o usuario selecionou colunas para exibir
        if mostrarDados:
    #Exibe os dados filtrados pelas colunas selecionadas
          st.write(df_selecionado[mostrarDados])

    #Verifica se o DataFrame filtrado (df_selecionado) náo esta vazio
    if not df_selecionado.empty:
        venda_total = df_selecionado["numero_vendas"].sum()
        venda_media = df_selecionado["numero_vendas"].mean()
        venda_mediana = df_selecionado["numero_vendas"].median()

        #Cria tres colunas para exibir os totais calculados
        total1, total2, total3 = st.columns(3, gap="large")

        with total1:
            st.info("Valor total de vendas dos carros", icon="📌")
            st.metric(label="Total", value=f"{venda_total:,.0f}")
        
        with total2:
            st.info("Valor medio das vendas", icon="📌")
            st.metric(label="Total", value=f"{venda_media:,.0f}")

        with total3:
            st.info("Valor medio dos carros", icon="📌")
            st.metric(label="Total", value=f"{venda_mediana:,.0f}")

    else:
        st.warning("Nenhum dado disponivel com os filtros selecionados")

    #Insere uma linha de divisorias para separa as secoes
    st.markdown("""------""")

#*********GRAFICOS************
def graficos(df_selecionado):
  
    #Verifica se o data frame filtrado possui dados para gerar um grafico
    if df_selecionado.empty:
        st.warning("Nenhum dado disponivel para gerar graficos")
        #Interrompe a funcao, pq nao motivo pra continuar executando se n tem medo
        return

    #Criacao dos graficos
    #4 abas -> Grafico de barras, linhas, pizza e dispersao
    graf1, graf2, graf3, graf4, graf5, graf6 = st.tabs(["Grafico de Barras", "Grafico de Linhas", "Grafico de Pizza", "Grafico de Dispersao", "Grafico de Area", "Grafico de Linhas 3D"])

    with graf1:
        st.write("Grafico de Barras")
        investimento = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending = False)
        fig_valores = px.bar(investimento, x=investimento.index, y="valor", orientation="v", title="<b>Valores de Carros</b>", color_discrete_sequence=["#0083b3"])
        st.plotly_chart(fig_valores, use_container_width = True)

    with graf2:
        st.write("Grafico de Linhas")
        dados = df_selecionado.groupby("marca").count()[["valor"]]
        fig_valores2 = px.line(dados, x=dados.index, y="valor", title="<b>Valores por Marca</b>", color_discrete_sequence=["#0083b3"])
        st.plotly_chart(fig_valores2, use_container_width = True)

    with graf3:
        st.write("Grafico de Pizza")
        dados2 = df_selecionado.groupby("marca").sum()[["valor"]]
        fig_valores3 = px.pie(dados2, values="valor", names=dados2.index, title="<b>Distribuicao de Valores por Marca</b>")
        st.plotly_chart(fig_valores3, use_container_width = True)

    with graf4:
        st.write("Grafico de Dispersao")
        dados3 = df_selecionado.melt(id_vars="marca", value_vars=["valor"])
        fig_valores4 = px.scatter(dados3, x="marca", y="value", title="<b>VDispersao de Valores por Marca</b>", color="variable")
        st.plotly_chart(fig_valores4, use_container_width = True)

    with graf5:
        st.write("Grafico de Area")
        dados4 = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending = False)
        fig_valores5 = st.area_chart(dados4)
        st.plotly_chart(fig_valores5, use_container_width = True)

    with graf6:
        st.write("Grafico de Linhas 3D")
        dados5 = df_selecionado.groupby("marca").count()[["valor"]]
        fig_valores6 = px.line_3d(dados5, x=dados5.index, y="valor", title="<b>Valores por Marca</b>", color_discrete_sequence=["#0083b3"])
        st.plotly_chart(fig_valores6, use_container_width = True)

    
def barraprogresso():
    valorAtual = df_selecionado["numero_vendas"].sum()
    objetivo = 10000000
    percentual = round((valorAtual / objetivo * 100))

    if percentual > 100:
        st.subheader("Valores Atingidos!")
    else:
        st.write(f"Voce tem {percentual}% de {objetivo}. Voce consegue nao desista agora!")
        mybar = st.progress(0)
        for percentualCompleto in range(percentual):
            mybar.progress(percentualCompleto + 1, text="Alvo %")

def menuLateral():
    with st.sidebar:
        selecionado = option_menu(menu_title="Menu", options=["Home", "Progresso"], icons=["house", "eye"], menu_icon="cast", default_index=0)

    if selecionado == "Home":
        st.subheader(f"Pagina: {selecionado}")
        Home()
        graficos(df_selecionado)
    
    if selecionado == "Progresso":
       st.subheader(f"Pagina: {selecionado}")
       barraprogresso()
       graficos(df_selecionado)



menuLateral()