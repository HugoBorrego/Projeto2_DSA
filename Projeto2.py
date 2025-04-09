# Projeto focado em Análise e Ciência de Dados

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

df = pd.read_csv(r'C:\Users\Computadores Gamer\PycharmProjects\pythonProject\Projeto2\dados\dataset.csv')

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
