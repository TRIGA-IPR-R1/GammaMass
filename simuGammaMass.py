########################################################################
####                                                                ####
####       CENTRO DE DESENVOLVIMENTO DA TECNOLOGIA NUCLEAR          ####
####                  Simulação do Detector Gama                    ####
####                           simu.py                              ####
####                                                                ####
####             Daniel de Almeida Magalhães Campolina              ####
####                      Lilly Salim Thein                         ####
####                 Thalles Oliveira Campagnani                    ####
####               Jefferson Quintão Campos Duarte                  ####
####                                                                ####
########################################################################

import os #para renomear arquivo e limpar tela
os.system("clear") #Limpa tela

import libVariaTarugo




# Configurações de todas simulações
particulas = 10
ciclos = 10







# Cria pasta para armazenar todos os resultados, com data no nome
libVariaTarugo.libGammaMass.mkdir("resultados", data=True)


# Caso Variação de Área com restante dos parametros fixos:
## Neste caso a área da sessão transversal é variada de 0 a 625 em todas simulações,
## sendo possível analizar o espectro de energia do fluxo que chega ao detector e também o espectro de energia dos pulsos gerados.
## Este "for" abaixo repete a simulação com várias magnitudes de intensidade de fonte, com ou sem bindagem.
## Para cada execução do simuVariaSimplesTarugo é possível gerar 1 espectro de fluxo e 1 espectro de pulso para cada área simulada internamente.
## Para cada execução do simuVariaSimplesTarugo é possível gerar 1 curva de "fluxo vs. area" e 1 curva de "pulso vs. area" trabalhando dados de cada espectro referente a cada area

libVariaTarugo.libGammaMass.mkdir("resultados_grupo_variaArea_intensidade_especura", voltar=False)
voltar = False
for fonte_cobalto_intensidade in [0, 7.4e1, 7.4e2, 7.4e3, 7.4e4, 7.4e5, 7.4e6, 7.4e7]:
    libVariaTarugo.simuVariaSimplesTarugo(tipoVaria="area", ini=0, fin=625, passo=25, prop=1, fonte_cobalto_intensidade=fonte_cobalto_intensidade, colimador_espessura = 2.7, particulas=particulas, ciclos=ciclos, voltar=voltar)
    libVariaTarugo.simuVariaSimplesTarugo(tipoVaria="area", ini=0, fin=625, passo=25, prop=1, fonte_cobalto_intensidade=fonte_cobalto_intensidade, colimador_espessura = 0, particulas=particulas, ciclos=ciclos)
    voltar=True




# Caso Variação de Proporção com restante dos parametros fixos:
## Neste caso a área da sessão transversal é mantida, e é variada a proporção de 1/2 a 1 e 1 a 2 por padrão em todas simulações,
## sendo possível analizar o espectro de energia do fluxo que chega ao detector e também dos pulsos gerados.
## Este for abaixo repete a simulação com várias magnitudes de intensidade de fonte, com ou sem bindagem.
## Para cada execução do simuVariaSimplesTarugo é possível gerar 1 espectro de fluxo e 1 espectro de pulso para cada proporção.
## Para cada execução do simuVariaSimplesTarugo é possível gerar 1 curva de "fluxo vs. proporção" e 1 curva de "pulso vs. proporção"

libVariaTarugo.libGammaMass.mkdir("resultados_grupo_variaProp_intensidade_especura")
voltar = True
for fonte_cobalto_intensidade in [0, 7.4e1, 7.4e2, 7.4e3, 7.4e4, 7.4e5, 7.4e6, 7.4e7]:
    libVariaTarugo.simuVariaSimplesTarugo(tipoVaria="prop", ini=1, fin=2, passo=0.2, area=200, fonte_cobalto_intensidade=0, colimador_espessura = 2.7, particulas=particulas, ciclos=ciclos, voltar=voltar)
    libVariaTarugo.simuVariaSimplesTarugo(tipoVaria="prop", ini=1, fin=2, passo=0.2, area=200, fonte_cobalto_intensidade=0, colimador_espessura = 0, particulas=particulas, ciclos=ciclos)
    voltar=False


# Caso Variação de Comprimento com restante dos parametros fixos:
## Neste caso a área da sessão transversal e proporção são mantidas, e é variada o comprimento de 0 a  por padrão em todas simulações,
## sendo possível analizar o espectro de energia do fluxo que chega ao detector e também dos pulsos gerados.
## Este for abaixo repete a simulação com várias magnitudes de intensidade de fonte, com ou sem bindagem.
## Para cada execução do simuVariaSimplesTarugo é possível gerar 1 espectro de fluxo e 1 espectro de pulso para cada proporção.
## Para cada execução do simuVariaSimplesTarugo é possível gerar 1 curva de "fluxo vs. proporção" e 1 curva de "pulso vs. proporção"

libVariaTarugo.libGammaMass.mkdir("resultados_grupo_variaComp_intensidade_especura")
voltar = True
for fonte_cobalto_intensidade in [0, 7.4e1, 7.4e2, 7.4e3, 7.4e4, 7.4e5, 7.4e6, 7.4e7]:
    libVariaTarugo.simuVariaSimplesTarugo(tipoVaria="comp", ini=0, fin=1000, passo=100, area=200, fonte_cobalto_intensidade=0, colimador_espessura = 2.7, particulas=particulas, ciclos=ciclos, voltar=voltar)
    libVariaTarugo.simuVariaSimplesTarugo(tipoVaria="comp", ini=0, fin=10000, passo=1000, area=200, fonte_cobalto_intensidade=0, colimador_espessura = 2.7, particulas=particulas, ciclos=ciclos, voltar=voltar)
    libVariaTarugo.simuVariaSimplesTarugo(tipoVaria="comp", ini=0, fin=1000, passo=100, area=200, fonte_cobalto_intensidade=0, colimador_espessura = 0, particulas=particulas, ciclos=ciclos)
    libVariaTarugo.simuVariaSimplesTarugo(tipoVaria="comp", ini=0, fin=10000, passo=1000, area=200, fonte_cobalto_intensidade=0, colimador_espessura = 0, particulas=particulas, ciclos=ciclos)
    voltar=False







# ToDo List:
# - normalizar os resultados já na função tallies_fluxo_detector (multiplicar pela fonte e dividir pelo volume)
# - gerar um código que geral a calibração automaticamente (faz a regreção gerando uma equação)
# - gerar um código que calcula o erro (ou incerteza. [erro relativo mais fácil?]) da medição de área (para facilitar pode usar a mesma curva usada na calibração) em função da área
# - analizar o gráfico e tirar uma conclusão de como achar uma incerteza (erro) representativa (incerteza pico?)
# - gerar um gráfico da incerteza em função da intensidade da fonte de cobalto