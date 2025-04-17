# Projeto focado em Análise e Ciência de Dados

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

df = pd.read_csv(r'dados\dataset.csv')

print(df.head())  # Amostra dos 5 primeiros dados
print(df.tail())  # Amostra dos 5 últimos dados
print(df.columns)  # Colunas do conjunto de dados
print(df.dtypes)  # Verificando o tipo de dado de cada coluna
print(df['Valor_Venda'].describe())  # Resumo estatístico da coluna com o valor de venda
print(df[df.duplicated()])  # Verificando se há registros duplicados
print(df.isnull().sum())  # Verificando de há valores ausentes

# P1 - Qual Cidade com Maior Valor de Venda de Produtos da Categoria 'Office Supplies'?
df_p1 = df[df['Categoria'] == 'Office Supplies'] #filtrando apenas os itens da categoria 'Office Supplies'
df_p1_total = df_p1.groupby('Cidade')['Valor_Venda'].sum() #agrupando o valor das vendas por cada cidade
cidade_maior_venda = df_p1_total.idxmax() #armazena em variavel a cidade com maior valor de venda
print("A cidade com maior valor de venda para 'Office Supplies' é ", cidade_maior_venda)
print(df_p1_total.sort_values(ascending=False)) #mostra o valor de quantas vendas tiveram em cada cidade

# P2 - Qual o Total de Vendas Por Data do Pedido?
df_p2 = df.groupby('Data_Pedido')['Valor_Venda'].sum() #agrupando a soma das vendas pela data do pedido
#Criando o gráfico usando matplotlib
plt.figure(figsize=(20, 6)) #tamanho do gráfico 20 de altura por 6 de largura
df_p2.plot(x = 'Data_Pedido', y = 'Valor_Venda', color = 'green') #atribuição dos eixos x e y
plt.title('Total de valor de Vendas por Data do Pedido') #título do gráfico
print(plt.show())

# P3 - Qual o Total de Vendas por Estado?
df_p3 = df.groupby('Estado')['Valor_Venda'].sum().reset_index() #agrupando a soma das vendas pelo estado
plt.figure(figsize=(14, 6)) #tamanho do gráfico 14 de altura por 6 de largura
sns.barplot(data=df_p3, y='Valor_Venda', x='Estado').set(title='Valor de Vendas por Estado') #criando um gráfico usando o seaborn
plt.xticks(rotation=80) #rotaciona o titulo dos estados para ser melhor de visualizar
print(plt.show()) 

# P4 - Quais São as 10 Cidades com Maior Total de Vendas?
df_p4 = df.groupby('Cidade')['Valor_Venda'].sum().reset_index().sort_values(by='Valor_Venda', ascending=False).head(10) ##agrupando a soma das vendas por cidade, reseta o indice, ordenar e colocar o valor venda em ordem decrescente
print(df_p4)
plt.figure(figsize=(16, 6))
sns.barplot(data=df_p4, x='Cidade', y='Valor_Venda').set(title='As 10 cidade com maior valor de vendas')
print(plt.show())

# P5 - Qual Segmento Teve o Maior Total de Vendas?
df_p5 = df.groupby('Segmento')['Valor_Venda'].sum().reset_index().sort_values(by='Valor_Venda', ascending=False)

def autopct_format(values): #função que converte os dados em valores absolutos
    def my_format(pct):
        total = sum(values)
        val = int(round(pct * total) / 100.0)
        return '$ {v:d}'.format(v = val)
    return my_format


plt.figure(figsize=(14, 6))
plt.pie(df_p5['Valor_Venda'], labels=df_p5['Segmento'], autopct=autopct_format(df_p5['Valor_Venda']), startangle=90)
plt.show()

# P6 - Qual o Total de Vendas Por Segmento e Por Ano?
df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'], dayfirst=True)
df['Ano'] = df['Data_Pedido'].dt.year
df_p6 = df.groupby(['Ano', 'Segmento'])['Valor_Venda'].sum()
print(df_p6.head())

# P7 - Os gestores da empresa estão considerando conceder diferentes faixas de descontos e gostariam de fazer uma simulação com base na regra abaixo:
#- Se o Valor_Venda for maior que 1000 recebe 15% de desconto.
#- Se o Valor_Venda for menor que 1000 recebe 10% de desconto.
# Quantas Vendas Receberiam 15% de Desconto?
df['Desconto'] = np.where(df['Valor_Venda'] > 1000, 0.15, 0.10)
print(df.head())
print(df['Desconto'].value_counts())

# P8 - Considere Que a Empresa Decida Conceder o Desconto de 15% do Item Anterior. Qual Seria a Média do Valor de Venda Antes e Depois do Desconto?
df['Valor_Venda_Desconto'] = df['Valor_Venda'] - (df['Valor_Venda'] * df['Desconto'])
df_p8_vendas_antes_desconto = df.loc[df['Desconto'] == 0.15, 'Valor_Venda']
df_p8_vendas_depois_desconto = df.loc[df['Desconto'] == 0.15, 'Valor_Venda_Desconto']
media_vendas_antes_desconto = df_p8_vendas_antes_desconto.mean()
media_vendas_depois_desconto = df_p8_vendas_depois_desconto.mean()
print("Média das vendas antes do desconto de 15%:", round(media_vendas_antes_desconto, 2))
print("Média das vendas depois do desconto de 15%:", round(media_vendas_depois_desconto, 2))

# P9 - Qual o Média de Vendas Por Segmento, Por Ano e Por Mês?
df['Mes'] = df['Data_Pedido'].dt.month
df_p9 = df.groupby(['Ano', 'Mes', 'Segmento'])['Valor_Venda'].agg([np.sum, np.mean, np.median])
anos = df_p9.index.get_level_values(0)
meses = df_p9.index.get_level_values(1)
segmentos = df_p9.index.get_level_values(2)
plt.figure(figsize=(12, 6))
sns.set()
fig1 = sns.relplot(kind='line',
                   data=df_p9,
                   y='mean',
                   x=meses,
                   hue=segmentos,
                   col=anos,
                   col_wrap=4)
plt.show()

# P10 - Qual o Total de Vendas Por Categoria e SubCategoria, Considerando Somente as Top 12 SubCategorias?
df_p10 = df.groupby(['Categoria', 'SubCategoria']).sum(numeric_only=True).sort_values('Valor_Venda', ascending=False).head(12)
df_p10 = df_p10[['Valor_Venda']].astype(int).sort_values(by='Categoria').reset_index()
df_p10_cat = df_p10.groupby('Categoria').sum(numeric_only=True).reset_index()
cores_categorias = ['#5d00de', '#0ee84f', '#e80e27']
cores_subcategorias = ['#aa8cd4', '#aa8cd5', '#aa8cd6', '#aa8cd7', '#26c957', '#26c958', '#26c959', '#26c960', '#e65e65', '#e65e66', '#e65e67', '#e65e68']
fig, ax = plt.subplots(figsize=(18, 12))
p1 = ax.pie(df_p10_cat['Valor_Venda'],
            radius=1,
            labels = df_p10_cat['Categoria'],
            wedgeprops=dict(edgecolor='white'),
            colors=cores_categorias)
p2 = ax.pie(df_p10['Valor_Venda'],
            radius=0.9,
            labels=df_p10['SubCategoria'],
            autopct=autopct_format(df_p10['Valor_Venda']),
            colors=cores_subcategorias,
            labeldistance=0.7,
            wedgeprops=dict(edgecolor='white'),
            pctdistance=0.53,
            rotatelabels=True)
centre_circle = plt.Circle((0, 0), 0.6, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.annotate(text='Total de Vendas: ' + '$ ' + str(int(sum(df_p10['Valor_Venda']))), xy=(-0.2, 0))
plt.title('Total de Vendas Por Categoria e Top 12 SubCategorias')
plt.show()

