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







# --- Seção responsável por executar o experimento ---

import libGammaMass

# Cria pasta com data no nome para armazenar os resultados
libGammaMass.mkdir("resultados", data=True)

#Configurações da simulação
config = [100000, 200] #Particulas, ciclos totais


#Simular todos os casos usando matriz_real para alterar parâmetros da simulação
#for i in range(0, len(matriz_real)):

pos_ini = -8
pos_fin =  8
for i in range(pos_ini, pos_fin+1):
    print("################")
    print("####### ",i, " ######")
    print("################")
    libGammaMass.mkdir(f"simulação.{i}", data=False, voltar=(i!=pos_ini))
    
    #Criando reator no OpenMC
    detector = libGammaMass.Detector(particulas=config[0], ciclos=config[1])
    detector.geometria(
        tarugo_altura=20,
        tarugo_esteira_pos = i,
        colimador_espessura = 1,
        colimador_abertura = 0.70,
    )

    detector.plotagem("plot.lateral.xy.png",  "xy")
    detector.plotagem("plot.frontal.yz.png",  "yz", rotacionar = True)
    detector.plotagem("plot.superior.xz.png", "xz", rotacionar = True, origin=(0,52.35,0))
    
    
    #Configurações de tallies
    detector.tallies(init=True)     #Iniciar a lista de tallies
    detector.tallies_fluxo_detector(nome="qualquer energia")        #Adicionar o tallies de fluxo a lista
    detector.tallies_fluxo_detector(energia=[1.1e6, 1.2e6], nome="energia A cobalto")        #Adicionar o tallies de fluxo a lista
    detector.tallies_fluxo_detector(energia=[1.2e6, 1.3e6], nome="energia A~B cobalto")      #Adicionar o tallies de fluxo a lista
    detector.tallies_fluxo_detector(energia=[1.3e6, 1.4e6], nome="energia B cobalto")        #Adicionar o tallies de fluxo a lista
    detector.tallies(export=True)   #Finalizar a lista (exportar tallies.xml)
    
    
    detector.simular()







# --- Seção responsável por extrair resultados dos experimentos ---

libGammaMass.chdir("..")

vetor_fluxo = [] #vetor para salvar todos os resultados
vetor_fluxo_incerteza = [] #vetor de incertezas (na verdade é o desvio padrão (std))

# Navegue arquivo por arquivo coletando os resultados
for i in range(pos_ini, pos_fin+1):
    #Obtenha o fluxo dos referidos arquivos
    fluxo1, incerteza1 =     detector.tallies_fluxo_detector(get=True,    nome="qualquer energia",       file=f"simulação.{i}/statepoint.{config[1]}.h5")
    fluxo2, incerteza2 =     detector.tallies_fluxo_detector(get=True,    nome="energia A cobalto",      file=f"simulação.{i}/statepoint.{config[1]}.h5")
    fluxo3, incerteza3 =     detector.tallies_fluxo_detector(get=True,    nome="energia A~B cobalto",    file=f"simulação.{i}/statepoint.{config[1]}.h5")
    fluxo4, incerteza4 =     detector.tallies_fluxo_detector(get=True,    nome="energia B cobalto",      file=f"simulação.{i}/statepoint.{config[1]}.h5")
    #Salve eles nos vetores
    vetor_fluxo.append([fluxo1, fluxo2, fluxo3, fluxo4])
    vetor_fluxo_incerteza.append(incerteza1, incerteza2, incerteza3, incerteza4)








# --- Seção responsável por salvar entradas e saídas de todos experimentos ---

from pprint import pprint
with open("resultados_experimentos.py", "w") as f:
    f.write("# Resultados da Simulação OpenMC\n")
    f.write("# Arquivo gerado automaticamente\n\n")
    
    f.write("config = ")
    pprint(config, stream=f)
    f.write("\n")

    f.write("vetor_fluxo = ")
    pprint(vetor_fluxo, stream=f)
    f.write("\n")
    
    f.write("vetor_fluxo_incerteza = ")
    pprint(vetor_fluxo_incerteza, stream=f)
    f.write("\n")
    