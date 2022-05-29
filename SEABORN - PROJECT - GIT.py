#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#importando as bibliotecas e abrindo o dados
import pandas as pd

df = pd.read_csv('C:/Users/cleto/Documents/DATA-SCIENCE/dados/gorjetas/tips.csv')
df.head()


# Observando a quantidade de linhas e colunas e os tipos dos dados ,# o data frame não possui valores faltantes
df.info()

#Renomear as colunas para o português
renomear = {'total_bill':'valor_da_conta', 'tip':'gorjeta', 'dessert':'sobremesa', 'day':'dia', 'time':'refeição', 'size':'pessoas'}
Gorjetas = df.rename(columns = renomear)
Gorjetas.head()


#modificando as variáveis categóricas para o português, mas primeiro irei observa-las
Gorjetas.sobremesa.unique()

# Modificando
sob = {'No':'Não', 'Yes':'Sim'}
sob

#Aplicando
Gorjetas.sobremesa.map(sob)

# #salvando no dataframe
Gorjetas.sobremesa = Gorjetas.sobremesa.map(sob)
Gorjetas.head()


# Mais uma variável para observar
Gorjetas.dia.unique()

#modificando
di = {'Sun':'Domingo', 'Sat':'Sábado', 'Thur':'Quinta','Fri':'Sexta'}

#aplicando
Gorjetas.dia.map(di)

#Salvando
Gorjetas.dia = Gorjetas.dia.map(di)
Gorjetas.head()

# A última coluna a ter suas variáveis modificadas
# observaddo a coluna refeição
Gorjetas.refeição.unique()

# Modificando
ref = {'Dinner':'Jantar', 'Lunch':'Almoço'}

#Aplicando
Gorjetas.refeição.map(ref)

# Salvandno no dataframe
Gorjetas.refeição = Gorjetas.refeição.map(ref)
ref.head()



# CRIANDO UMA COLUNA COM A PORCENTAGEM OU  VALOR PROPORCIONAL
Gorjetas['porcentagem'] = Gorjetas['gorjeta'] / Gorjetas['valor_da_conta'] 


# ANÁLISES GRÁFICAS EXPLORATÓRIAS
import seaborn as sns


# Observando se há algum tipo de tendência de aumento, no numero de gorjetas em relação ao valor da conta
ax= sns.scatterplot(x = 'valor_da_conta', y = 'gorjeta', data= Gorjetas)
ax.figure.set_size_inches(12, 6)
#Organização gráfica
ax.set_title('Gorjeta x Valor da Conta', fontsize=18)
ax.set_xlabel('Valor da Conta', fontsize=14)
ax.set_ylabel('Valor da Gorjeta', fontsize=14)
ax



# Observando a tendência de aumento por outro meio gráfico
ax = sns.relplot(x = 'valor_da_conta', y = 'gorjeta', data= Gorjetas, kind = 'line')
#Organização
ax.fig.suptitle( 'Gorjeta x Valor da conta' , fontsize = 14, y = 1.06)
ax.set_axis_labels( 'Valor da conta ', 'Gorjeta', fontsize = 14)  # x primeiro pra depois o y.


# Mais um método gráfico para observar a tendencia de aumento, mas agora com uma reta apontando o acréscimo.
ax = sns.lmplot(x = 'valor_da_conta', y = 'gorjeta', data= Gorjetas)
# Organizando
ax.fig.suptitle( 'Gorjeta x Valor da conta' , fontsize = 14, y = 1.06)
ax.set_axis_labels( 'Valor da conta ', 'Valor da conta', fontsize = 14)  # x primeiro pra depois o y.


# Agora obsrvando se há uma tendência de aumento para a variável porcentagem em relação ao tamanho da gorjeta
ax = sns.lmplot(x = 'porcentagem', y = 'valor_da_conta', data= Gorjetas)

# Organizando
ax.fig.suptitle( 'Valor da conta x Porcentagem' , fontsize = 14, y = 1.06)
ax.set_axis_labels( 'Porcentagem' , 'valor da conta'  , fontsize = 14)  # x primeiro pra depois o y.

# Obs: Apesar de haver uma tendência de aumento na análise de gorjetas x tamanho da conta, aqui foi observado um decréscimo, mas por quê? Porque, quando se realiza a porcentagem
# se observa se há uma tendência proporcional ao aumento dos valores das gorjetas de acordo com o aumento da conta. Podemos concluir com isso tudo que há sim um aumento do
valor da conta com de acordo que se aumentam as gorjetas, mas não necessáriamente esse aumento é proporcional.



# OBSERVANDO AS VARIÁVEIS UMA A UMA PARA FINS DE TESTE DE HIPÓTESE

# Observando a distribuições da 'sim' e 'não' das sobremesas
sns.catplot(x='sobremesa', y = 'gorjeta', data = Gorjetas)
sns.boxplot(x='sobremesa', y = 'gorjeta', data = Gorjetas)


# Observando se há uma tendência de aumento para valor da gorjeta em relação ao tamanho da conta

ax = sns.lmplot(x='valor_da_conta', y= 'gorjeta', data = Gorjetas, hue = 'sobremesa', col = 'sobremesa')
ax.fig.suptitle( 'Gorjeta x Valor da conta utilizando os dados de sobremesa ' , fontsize = 14, y = 1.06)
ax.set_axis_labels( 'Valor da conta ', 'Gorjeta', fontsize = 14)


#TESTANTO HIPÓTESES IREMOS TESTAR DUAS:

# Se há diferença entre o consumo de sobremesa entre os valores proporcionais e se há diferença entre os valores totais

# Separamos em uma query os dados que iremos utilizar
com_sobremesa = Gorjetas.query("sobremesa == 'Sim'")['porcentagem']
sem_sobremesa = Gorjetas.query("sobremesa == 'Não'")['porcentagem']

com_sobremesa_2 = Gorjetas.query("sobremesa == 'Sim'").valor_da_conta


#PODE ADD GORJETA TB
sem_sobremesa_2 = Gorjetas.query("sobremesa == 'Não'").valor_da_conta


# Importando a biblioteca estatística
from scipy.stats import ranksums

# testando a porcentagem
ranksums(com_sobremesa,sem_sobremesa)
#valor significativo P<0.05

# testando o valor da conta ( se houve difernça entre aqueles que pediu sobremesa ou não)
ranksums(com_sobremesa,sem_sobremesa)

#valor significativo P <0.05


# OBSERVANDO SE HÁ DIFERENÇAS NOS DIAS DA SEMANA

# É possível observar que há diferença nas medianas entre os dias da semana que é nos sábado há valores acima dos máximos e mínimo
ax = sns.boxplot(x = 'dia', y = 'gorjeta', data = Gorjetas)


ax.figure.set_size_inches(10,6) #aumentar a imagem
ax.set_title('Boxplot dos dias da semana pelo valor da gorjeta', fontsize = 20 )
ax.set_ylabel('Valor da gorjeta', fontsize = 18)
ax.set_xlabel('Dias da Semana ', fontsize = 18)


# Avaliando se há tendência de queda ou aumento com a mudança de dia da semana no valor total
ax = sns.lmplot(x = 'valor_da_conta', y = 'gorjeta', data = Gorjetas, hue = 'dia', col = 'dia')
ax.fig.suptitle( 'Gorjeta x Valor da conta: Utilizando dias da semana ' , fontsize = 14, y = 1.06)
ax.set_axis_labels( 'Valor da conta ', 'Gorjeta', fontsize = 14)  # x primeiro pra depois o y.


# Avaliando se há tendência de queda ou aumento com a mudança de dia da semana no valor proporcional (porcentagem)
ax = sns.lmplot(x = 'valor_da_conta', y = 'porcentagem', data = Gorjetas, hue = 'dia', col = 'dia')
ax.fig.suptitle( 'Gorjeta x Valor da conta: Utilizando os dias da Semana' , fontsize = 14, y = 1.06)
ax.set_axis_labels( 'Valor da conta ', 'Porcentagem', fontsize = 14)  # x primeiro pra depois o y.


# Separando em query

Quinta = Gorjetas.query("dia=='Quinta'").valor_da_conta
Sexta = Gorjetas.query("dia=='Sexta'").valor_da_conta
Sábado = Gorjetas.query("dia=='Sábado'").valor_da_conta
Domingo = Gorjetas.query("dia=='Domingo'").valor_da_conta

Quinta2 = Gorjetas.query("dia=='Quinta'").porcentagem
Sexta2 = Gorjetas.query("dia=='Sexta'").porcentagem
Sábado2 = Gorjetas.query("dia=='Sábado'").porcentagem
Domingo2 = Gorjetas.query("dia=='Domingo'").porcentagem

ranksums(Quinta,Sexta)
ranksums(Quinta,Sábado)
ranksums(Quinta,Domingo)
ranksums(Sexta,Sábado)
ranksums(Sexta,Domingo)
# Nesta análise  do valor da conta apenas na  sábado e domingo deram valores significativos


ranksums(Quinta2,Sexta2)
ranksums(Quinta2,Sábado2)
ranksums(Quinta2,Domingo2)
ranksums(Sexta2,Sábado2)
ranksums(Sexta2,Domingo2)

# Nesta análise  do valor da conta dois dias da semana na  deram valores significativos quinta e domingo e sexta e domingo, ilustrando que há diferença entre ambos




# # DIFERENÇA DE REFEIÇÕES


sns.boxplot (x='Refeição', y= 'valor_da_conta', data = gorjetas)

# observa-se  diferença dos valores máximos e mínimos, da distribuição dos dados e da mediana!

# Selecionado a refeição almoço e janta  e seus valores de conta
almoço = gorjetas.query("Refeição == 'Almoço'")['valor_da_conta']
janta = gorjetas.query("Refeição == 'Jantar'")['valor_da_conta']

# Observando a suas distritribuição em um histograma
ax = sns.distplot(almoço, kde = False)
ax.figure.set_size_inches(10,6) 
#organizando
ax.set_title('Disttribuição do valor da conta no almoço', fontsize = 18 )
ax.set_ylabel('Valor da frequência', fontsize = 16)
ax.set_xlabel(' Valor da conta ', fontsize = 16)





# do jantar
ax = sns.distplot(janta, kde = False)
ax.figure.set_size_inches(10,6) 
#organizando
ax.set_title('Disttribuição do valor da conta no Jantar', fontsize = 18 )
ax.set_ylabel('Valor da frequência', fontsize = 16)
ax.set_xlabel(' Valor da conta ', fontsize = 16)

# Realizando o teste de hipóteses

# TESTANDO
# OBSERVANDO SE HÁ DIFERENÇA ENTRE os valores almoço e jantar e o valor da conta
ranksums(almoço,janta)

# P>00,5


almoço2 = Gorjetas.query("refeição == 'Almoço'").porcentagem
janta2 =  Gorjetas.query("refeição == 'Jantar'").porcentagem
ranksums(almoço2,janta2)
# p>005

# Também testei se houve diferença entre os valors da gorjetas nas diferentes refeições
almoço3 = Gorjetas.query("refeição == 'Almoço'").gorjeta
janta3 =  Gorjetas.query("refeição == 'Jantar'").gorjeta
# p>005 não houve diferença significativa.











