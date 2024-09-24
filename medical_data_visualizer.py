# Importando bibliotecas necessárias
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Importando o dataframe
df = pd.read_csv('medical_examination.csv')

# 2. Criando a coluna 'overweight' com base no IMC
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2))
#se o IMC for maior que 25, o TRUE é convertido para 1 e o FALSE para 0
df['overweight'] = (df['overweight'] > 25).astype(int)

# 3. Normalizando colesterol e glicose
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

# 4. Função para desenhar o gráfico categórico
def draw_cat_plot():
    # 5. Derretendo o DataFrame para incluir as colunas de interesse
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # 6. Renomeando as colunas para 'variable' (característica) e 'value' (valor)
    df_cat = df_cat.rename(columns={'variable': 'variable', 'value': 'value'})

    # 7. Criando o gráfico categórico
    fig = sns.catplot(x="variable", hue="value", col="cardio", data=df_cat, kind="count")

    # 8. Ajustando o rótulo do eixo Y para 'total'
    fig.set_axis_labels("variable", "total")

    # 9. Salvando o gráfico como 'catplot.png'
    fig.savefig('catplot.png')

    # 10. Retornando a figura do gráfico categórico (acessando o objeto de figura do FacetGrid)
    return fig.fig

# 9. Função para desenhar o Heat Map
def draw_heat_map():
    # 10. Filtrando os dados para remover pacientes com altura ou peso fora dos percentis 2.5 e 97.5 (removendo outliers)
    df_heat = df[
        (df['height'] >= df['height'].quantile(0.025)) & 
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) & 
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 11. Calculando a matriz de correlação entre as variáveis numéricas do df filtrado
    corr = df_heat.corr()

    # 12. Criando uma máscara para ocultar o triângulo superior da matriz de correlação
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 13. Ajustando o tamanho da figura
    fig, ax = plt.subplots(figsize=(12, 8))

    # 14. Plotando a matriz de correlação com a máscara e anotando os valores com precisão ajustada (.1f)
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', cmap='coolwarm', square=True, ax=ax)

    # 15. Salvando o gráfico heatmap como 'heatmap.png'
    fig.savefig('heatmap.png')

    # 16. Retornando a figura do heatmap
    return fig

# Executando as funções para gerar os gráficos e salvá-los
draw_cat_plot()
draw_heat_map()