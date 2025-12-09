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

import libDetector

# Cria pasta com data no nome para armazenar os resultados
libDetector.mkdir("resultados", data=True)

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
    libDetector.mkdir(f"experimento.{i}", data=False, voltar=(i!=pos_ini))
    
    #Criando reator no OpenMC
    detector = libDetector.Detector(particulas=config[0], ciclos=config[1])
    detector.geometria(
        tarugo_esteira_pos = i,
        colimador_espessura = 5,
        colimador_abertura = 0.70
    )
    detector.plotagem("plot.lateral.xy.png",  "xy")
    detector.plotagem("plot.frontal.yz.png",  "yz", rotacionar = True)
    detector.plotagem("plot.superior.xz.png", "xz", rotacionar = True, origin=(0,52.35,0))
    
    
    #Configurações de tallies
    detector.tallies(init=True)     #Iniciar a lista de tallies
    detector.tallies_fluxo()        #Adicionar o tallies de fluxo a lista
    detector.tallies(export=True)   #Finalizar a lista (exportar tallies.xml)
    
    
    detector.simular()







# --- Seção responsável por extrair resultados dos experimentos ---

libDetector.chdir("..")

vetor_fluxo = [] #vetor para salvar todos os resultados
vetor_fluxo_incerteza = [] #vetor de incertezas (na verdade é o desvio padrão (std))

# Navegue arquivo por arquivo coletando os resultados
for i in range(pos_ini, pos_fin+1):
    #Obtenha o fluxo dos referidos arquivos
    fluxo, incerteza = detector.tallies_fluxo(get=True, file=f"experimento.{i}/statepoint.{config[1]}.h5")
    #Salve eles nos vetores
    vetor_fluxo.append(fluxo)
    vetor_fluxo_incerteza.append(incerteza)










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
    