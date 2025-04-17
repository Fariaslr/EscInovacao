import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

# Geração de CSV a partir do dataset Iris (somente uma vez)
data = load_iris(as_frame=True)
df_padrao = data.frame
df_padrao.to_csv("iris.csv", index=False)

st.set_page_config(page_title="Data Analyzer", layout="wide")

st.title("📊 Data Analyzer App")
st.markdown("Faça o upload de um arquivo CSV ou Excel para visualizar, explorar e analisar seus dados.")

# Upload de arquivo
file = st.file_uploader("📁 Faça upload de um arquivo CSV ou Excel", type=['csv', 'xlsx'])

if file:
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Conversão de colunas de data para datetime
        for col in df.select_dtypes(include=['object']).columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='ignore')  # Converte se possível, caso contrário ignora
            except Exception as e:
                pass

        # Visualizar nulos após tratamento
        st.subheader("🧪 Verificação de Dados Nulos")
        st.write(df.isnull().sum())

        # Seleção de colunas
        colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        colunas_categoricas = df.select_dtypes(include=['object']).columns.tolist()

        col_filtro = st.sidebar.selectbox("Coluna numérica para filtrar:", colunas_numericas)
        filtro_min, filtro_max = float(df[col_filtro].min()), float(df[col_filtro].max())
        val_min, val_max = st.sidebar.slider("Intervalo do filtro:", filtro_min, filtro_max, (filtro_min, filtro_max))

        df_filtrado = df[(df[col_filtro] >= val_min) & (df[col_filtro] <= val_max)]

        # Dados
        st.subheader("📋 Visualização da Tabela")
        st.dataframe(df)

        st.subheader("📊 Estatísticas Descritivas (Média, Mediana e Desvio Padrão)")

        # Calcular as estatísticas manualmente
        stats_df = pd.DataFrame({
            "Média": df[colunas_numericas].mean(),
            "Mediana": df[colunas_numericas].median(),
            "Desvio Padrão": df[colunas_numericas].std()
        })

        st.dataframe(stats_df.T)    

        st.subheader(f"🔍 Dados filtrados com base em **{col_filtro}** entre {val_min:.2f} e {val_max:.2f}")
        st.dataframe(df_filtrado)

        # Botão de download
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar dados filtrados", data=csv, file_name="dados_filtrados.csv", mime='text/csv')

        # Gráficos
        st.subheader("📊 Gráficos")

        with st.expander("📉 Histograma"):
            col_hist = st.selectbox("Coluna para histograma", colunas_numericas, key="hist")
            fig, ax = plt.subplots(figsize=(5, 3))
            sns.histplot(df_filtrado[col_hist], kde=True, ax=ax)
            ax.set_title(f'Histograma de {col_hist}')
            ax.set_xlabel(col_hist)
            ax.set_ylabel("Frequência")
            st.pyplot(fig)

        with st.expander("🔘 Gráfico de Dispersão (Scatter Plot)"):
            colunas_eixo_x = df_filtrado.select_dtypes(include=['float64', 'int64', 'datetime64']).columns.tolist()
            colunas_eixo_y = df_filtrado.select_dtypes(include=['float64', 'int64']).columns.tolist()

            x_axis = st.selectbox("Eixo X", colunas_eixo_x, key="x")
            y_axis = st.selectbox("Eixo Y", colunas_eixo_y, key="y")

            fig, ax = plt.subplots()
            sns.scatterplot(data=df_filtrado, x=x_axis, y=y_axis, ax=ax)
            ax.set_title(f'{y_axis} vs {x_axis}')
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            plt.xticks(rotation=45)  # Rotaciona datas se necessário
            st.pyplot(fig)

        with st.expander("📊 Gráfico de Barras"):
            col_bar = st.selectbox("Coluna para gráfico de barras", df.columns)

            aplicar_agrupamento = st.checkbox("Agrupar por prefixo (antes do hífen)", value=False)

            try:
                if aplicar_agrupamento:
                    # Agrupar por prefixo antes do hífen
                    df_filtrado['grupo'] = df_filtrado[col_bar].astype(str).str.split('-').str[0].str.strip()
                    dados_barras = df_filtrado['grupo'].value_counts()
                    label_eixo = "Grupo"
                else:
                    dados_barras = df_filtrado[col_bar].astype(str).value_counts()
                    label_eixo = col_bar

                fig, ax = plt.subplots()
                dados_barras.plot(kind='bar', ax=ax)
                ax.set_title(f'Contagem por {"grupo" if aplicar_agrupamento else "categoria"} em {col_bar}')
                ax.set_xlabel(label_eixo)
                ax.set_ylabel("Contagem")
                st.pyplot(fig)

            except Exception as e:
                st.warning(f"Erro ao gerar gráfico de barras: {e}")


    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
else:
    st.info("Aguardando upload de arquivo...")
