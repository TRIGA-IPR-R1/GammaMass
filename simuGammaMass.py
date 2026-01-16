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
import numpy as np

# Funções para escrita em arquivo
from pprint import pprint

def escreva_comentario(arquivo, valor, nome, comentario = None):
    # Escreva comantário e salte linha
    arquivo.write(f"#{comentario}\n")

def escreva_variaveis(arquivo, comentario = None, **kwargs):
    # Se for passado comentário, escreva antes da variável
    if comentario != None:
        arquivo.write(f"#{comentario}\n")

    for nome, valor in kwargs.items():
        arquivo.write(f"{nome} = ")
        pprint(valor, stream=arquivo)
        arquivo.write("\n")




# --- Seção responsável por executar o experimento ---

import libGammaMass
libGammaMass.simu = True
libGammaMass.plotar = False


def simuVariaArea(
        # Controle de pastas, para se deve voltar uma pasta acima antes de criar
        voltar=True,
        
        # Configurações da simulação
        particulas = 100000,
        ciclos     = 100,

        # Configurações de variação de área
        area_ini = 0,
        area_fin = 625, #25x25
        passo    = 25,

        # Configurações de geometria e fonte
        ## Parâmetros do tarugo
        tarugo_esteira_pos = 0, #centralizado em cima da fonte
        tarugo_comprimento = 10,
        #Gerados automaticamente:
        #tarugo_largura     = 10,
        #tarugo_altura      = 10,
        
        ## Parâmetros do colimador
        colimador_espessura = 2.7, #Espessura nominal do colimador LB-4700
        colimador_abertura  = 7.8, #Diametro do detector
        colimador_impureza  = 0,
        
        ## Parãmetros das fontes
        fonte_cobalto_intensidade    = 7.4e6, ########### Atividade de 3.7e7 x2 pois são 2 fótons
        fonte_raiosCosmicos_mes      = 1,
        fonte_raiosCosmicos_latitude = 0,
        
        ## Parametros do detector
        detectores_numero           = 1,
        detectores_altura_meio      = 52.35,
        detectores_altura_esquerda  = 52.35,
        detectores_altura_direita   = 52.35,

        ##Parametros concreto
        fonte_Concreto_intensidade = 1.59e4           ### multiplicado por 1,57 área da semi-esfera
        ):
    # Cria pasta com data no nome para armazenar os resultados
    libGammaMass.mkdir("resultados_"+str(int(fonte_cobalto_intensidade))+"_"+str(int(colimador_espessura*10)), data=False, voltar=voltar)

    #Configurações da simulação
    config = [particulas, ciclos] #Particulas, ciclos totais


    vetor_area = []
    for area in range(area_ini, area_fin+1, passo):
        libGammaMass.mkdir(f"simulação.{area}", data=False, voltar=(area!=area_ini))

        print("################")
        print("####### ",area, " ######")
        print("################")

        
        #Criando reator no OpenMC
        vetor_area.append(area)
        detector = libGammaMass.Detector(particulas=config[0], ciclos=config[1])
        detector.geometria(
            # Valores gerados de acordo com os parâmetros passados como parâmetros
            tarugo_largura               = np.sqrt(area),
            tarugo_altura                = np.sqrt(area),
            # Repassar valores dos parâmetros
            tarugo_esteira_pos           = tarugo_esteira_pos,
            tarugo_comprimento           = tarugo_comprimento,
            colimador_espessura          = colimador_espessura,
            colimador_abertura           = colimador_abertura,
            colimador_impureza           = colimador_impureza,
            fonte_cobalto_intensidade    = fonte_cobalto_intensidade,
            fonte_raiosCosmicos_mes      = fonte_raiosCosmicos_mes,
            fonte_raiosCosmicos_latitude = fonte_raiosCosmicos_latitude,
            fonte_Concreto_intensidade   = fonte_Concreto_intensidade,
            detectores_numero            = detectores_numero,
            detectores_altura_meio       = detectores_altura_meio,
            detectores_altura_esquerda   = detectores_altura_esquerda,
            detectores_altura_direita    = detectores_altura_direita
        )
        detector.configurações(particulas=config[0], ciclos=config[1])

        detector.plotagem("plot.lateral.xy.png",  "xy")
        detector.plotagem("plot.frontal.yz.png",  "yz", rotacionar = True)
        #detector.plotagem("plot.superior.xz.png", "xz", rotacionar = True, origin=(0,52.35,0))


        intervalos_energias=np.linspace(5e3,2e6,2**10).tolist() # Intervalo de 5KeV a 2MeV dividido em 2¹⁰ canais
        
        #Configurações de tallies
        detector.tallies(init=True)     #Iniciar a lista de tallies
        detector.tallies_detector(energia=intervalos_energias, score="flux",         nome="espectroFluxo")           #1
        detector.tallies_detector(energia=intervalos_energias, score="pulse-height", nome="espectroPulso")           #2
        detector.tallies(export=True)   #Finalizar a lista (exportar tallies.xml)


        detector.simular()





    if libGammaMass.simu == True:

        # --- Seção responsável por extrair resultados dos experimentos ---

        libGammaMass.chdir("..")

        vetor_fluxo = [] #vetor para salvar todos os resultados
        vetor_fluxo_incerteza = [] #vetor de incertezas (na verdade é o desvio padrão (std))
        vetor_pulso = [] #vetor para salvar todos os resultados
        vetor_pulso_incerteza = [] #vetor de incertezas (na verdade é o desvio padrão (std))
        # Navegue arquivo por arquivo coletando os resultados
        for i in range(area_ini, area_fin+1, passo):
            fluxo, incerteza_f =     detector.tallies_detector(get=True,    nome="espectroFluxo", score="flux",          file=f"simulação.{i}/statepoint.{config[1]}.h5")
            pulso, incerteza_p =     detector.tallies_detector(get=True,    nome="espectroPulso", score="pulse-height",  file=f"simulação.{i}/statepoint.{config[1]}.h5")
            
            #Salve eles nos vetores
            vetor_fluxo.append(fluxo)
            vetor_fluxo_incerteza.append(incerteza_f)
            vetor_pulso.append(pulso)
            vetor_pulso_incerteza.append(incerteza_p)







        # --- Seção responsável por salvar entradas e saídas de todos experimentos ---


        with open("resultados_simuVariaArea.py", "w") as f:  #### mudar nome para separar os casos
            escreva_comentario(f," Resultados da Simulação OpenMC - Função simuVariaArea\n\n")
            escreva_comentario(f," Arquivo gerado automaticamente\n\n")
            escreva_variaveis(f," Configurações de simulação:", particulas=particulas,  ciclos=ciclos)
            escreva_variaveis(f," Configurações de variação de área:", area_ini=area_ini, area_fin=area_fin, passo=passo)
            escreva_comentario(f," Configurações de geometria e fonte:")
            escreva_variaveis(f,"# Parâmetros do tarugo (tarugo_largura e tarugo_altura são gerados automaticamente):", tarugo_esteira_pos=tarugo_esteira_pos, tarugo_comprimento=tarugo_comprimento)
            escreva_variaveis(f,"# Parâmetros do colimador:",  colimador_espessura=colimador_espessura, colimador_abertura=colimador_abertura, colimador_impureza=colimador_impureza)
            escreva_variaveis(f,"# Parãmetros das fontes", fonte_cobalto_intensidade=fonte_cobalto_intensidade, fonte_raiosCosmicos_mes=fonte_raiosCosmicos_mes, fonte_raiosCosmicos_latitude=fonte_raiosCosmicos_latitude)
            escreva_variaveis(f,"# Parametros do detector", detectores_numero=detectores_numero, detectores_altura_meio=detectores_altura_meio, detectores_altura_esquerda=detectores_altura_esquerda, detectores_altura_direita=detectores_altura_direita)
            escreva_variaveis(f,"# Parametros concreto", fonte_Concreto_intensidade=fonte_Concreto_intensidade)
            escreva_comentario(f," Espectro para resultados:")
            escreva_variaveis(f," Intervalos de energias que são divididos os tallies de fluxo e altura de pulso", intervalos_energias=intervalos_energias)
            escreva_comentario(f," Resultados:\n\n")
            escreva_variaveis(f,"# Vetor contendo cada área simulada",vetor_area=vetor_area)
            escreva_variaveis(f,"# Vetor contendo o espectro de fluxo para cada área simulada",vetor_fluxo=vetor_fluxo)
            escreva_variaveis(f,"# Vetor contendo o espectro de incerteza do fluxo para cada área simulada",vetor_fluxo_incerteza=vetor_fluxo_incerteza)
            escreva_variaveis(f,"# Vetor contendo o espectro de pulso para cada área simulada",vetor_pulso=vetor_pulso)
            escreva_variaveis(f,"# Vetor contendo o espectro de incerteza do pulso para cada área simulada",vetor_pulso_incerteza=vetor_pulso_incerteza)




#Começo da execução
libGammaMass.mkdir("resultados_grupo_varia_intensidade_especura", data=True)

#resultados gerados
simuVariaArea(fonte_cobalto_intensidade=0,     colimador_espessura = 2.7, voltar=False)
simuVariaArea(fonte_cobalto_intensidade=7.4e1, colimador_espessura = 2.7)
simuVariaArea(fonte_cobalto_intensidade=7.4e2, colimador_espessura = 2.7)
simuVariaArea(fonte_cobalto_intensidade=7.4e3, colimador_espessura = 2.7)
simuVariaArea(fonte_cobalto_intensidade=7.4e4, colimador_espessura = 2.7)
simuVariaArea(fonte_cobalto_intensidade=7.4e5, colimador_espessura = 2.7)
simuVariaArea(fonte_cobalto_intensidade=7.4e6, colimador_espessura = 2.7)
simuVariaArea(fonte_cobalto_intensidade=7.4e7, colimador_espessura = 2.7)

simuVariaArea(fonte_cobalto_intensidade=7.4e7, colimador_espessura = 0)
simuVariaArea(fonte_cobalto_intensidade=7.4e6, colimador_espessura = 0)
simuVariaArea(fonte_cobalto_intensidade=7.4e5, colimador_espessura = 0)
simuVariaArea(fonte_cobalto_intensidade=7.4e4, colimador_espessura = 0)
simuVariaArea(fonte_cobalto_intensidade=7.4e3, colimador_espessura = 0)
simuVariaArea(fonte_cobalto_intensidade=7.4e2, colimador_espessura = 0)
simuVariaArea(fonte_cobalto_intensidade=7.4e1, colimador_espessura = 0)
simuVariaArea(fonte_cobalto_intensidade=0,     colimador_espessura = 0)


# ToDo List:
# - gerar TODOS resultados novamente (agora tem pulse-heigth)
# - normalizar os resultados já na função tallies_fluxo_detector (multiplicar pela fonte e dividir pelo volume)
# - gerar um código que geral a calibração automaticamente (faz a regreção gerando uma equação)
# - gerar um código que calcula o erro (ou incerteza. [erro relativo mais fácil?]) da medição de área (para facilitar pode usar a mesma curva usada na calibração) em função da área
# - analizar o gráfico e tirar uma conclusão de como achar uma incerteza (erro) representativa (incerteza pico?)
# - gerar um gráfico da incerteza em função da intensidade da fonte de cobalto