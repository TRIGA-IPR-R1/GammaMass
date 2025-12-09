########################################################################
####                                                                ####
####       CENTRO DE DESENVOLVIMENTO DA TECNOLOGIA NUCLEAR          ####
####              Simulação Fatorial do Detector Gama               ####
####                        simuFato.py                             ####
####                                                                ####
####             Daniel de Almeida Magalhães Campolina              ####
####                      Lilly Salim Thein                         ####
####                 Thalles Oliveira Campagnani                    ####
####               Jefferson Quintão Campos Duarte                  ####
####                                                                ####
########################################################################

import os #para renomear arquivo e limpar tela
os.system("clear") #Limpa tela








# --- Seção responsável por planejar o experimento ---

import libPlajFatorial
#                           -1    ->      +1
#-----------------------------------------------------------------
#Diâmetro blindagem:         0    ->       5       (cm)
#Impureza blindagem:         0    ->     200       (Bq/kg)
#Raios cósmicos:             1    ->       7       (mês)  [estação do ano]
#Raios cósmicos:           -45    ->      45       (latitude) [hemisfério norte ou sul]
#Número detectores:          1    ->       3
#Obs1: Densidade chumbo não varia, usar 11,34 g/cm3

# Fatores
fatores_nome = [
    "DiamBlin",  #Diâmetro blindagem
    "ImpuBlin",  #Impureza blindagem
    "Mês",       #Raios cósmicos - Estação
    "Latitude",  #Raios cósmicos - Posição
    "NumDetec"   #Número detectores
    ]

# Codificação de Fatores
fatores = []
fatores.append([0,   0,  1, -45, 1]) # -1
fatores.append([3, 100,  3,   0, 2]) #  0
fatores.append([6, 200,  7,  45, 3]) # +1
# OBS: 
#       fatores[0]: -1
#       fatores[1]:  0
#       fatores[2]: +1
# OBS2:
#       fatores[1][0]: Ponto central, DiamBli

#Matriz de planejamento codificada
matriz_planejamento = libPlajFatorial.criaPlanejamento(fatores=5, ponto_centrais=4)
#libPlajFat.imprime_matriz(matriz_planejamento, "Panejamento 2⁵ com 4 pontos centrais (matriz codificada)")

#Matriz de planejamento com valores reais substituidos
matriz_real         = libPlajFatorial.converte_matriz_real(matriz_planejamento, fatores)
#libPlajFat.imprime_matriz(matriz_real, "Panejamento 2⁵ com 4 pontos centrais (matriz real)")















# --- Seção responsável por executar o experimento ---

import libDetector

# Cria pasta com data no nome para armazenar os resultados
libDetector.mkdir("resultados", data=True)

#Configurações da simulação
config = [10000, 110] #Particulas, ciclos totais


#Simular todos os casos usando matriz_real para alterar parâmetros da simulação
#for i in range(0, len(matriz_real)):

pos_ini = 5
pos_fin = 100
for i in range(pos_ini, pos_fin+1, 5):
    print("################")
    print("####### ",i, " ######")
    print("################")
    libDetector.mkdir(f"experimento.{i}", data=False, voltar=(i!=pos_ini))
    
    #Criando reator no OpenMC
    detector = libDetector.Detector(particulas=config[0], ciclos=config[1])
    detector.geometria(
        tarugo_esteira_pos=0,
        colimador_espeçura=5,
        colimador_abertura=i/10
        
    )
    detector.plotagem("plot.lateral.xy.png",  "xy")
    detector.plotagem("plot.frontal.yz.png",  "yz", rotacionar = True)
    detector.plotagem("plot.superior.xz.png", "xz", rotacionar = True, origin=(0,52.35,0))
    
    #Aterar parâmetros de acordo com matriz_real
    detector.geometria(
        colimador_espeçura              =   matriz_real[i][0],   #Diâmetro blindagem
        colimador_impureza              =   matriz_real[i][1],   #Impureza blindagem
        fonte_raiosCosmicos_mes         =   matriz_real[i][2],   #Raios cósmicos - Estação
        fonte_raiosCosmicos_latitude    =   matriz_real[i][3],   #Raios cósmicos - Posição
        detectores_numero               =   matriz_real[i][4]    #Número detectores
        )
    
    #Configurações de tallies
    detector.tallies(init=True)     #Iniciar a lista de tallies
    detector.tallies_fluxo()        #Adicionar o tallies de fluxo a lista
    detector.tallies(export=True)   #Finalizar a lista (exportar tallies.xml)
    
    #Plotar vistas para debugar [opicional]
    detector.plotagem("plot.xy.png", "xy")
    detector.plotagem("plot.yz.png", "yz", rotacionar=True)
    
    #Rodar simulação
    detector.simular()
    

exit(0)






# --- Seção responsável por extrair resultados dos experimentos ---

libDetector.chdir("..")

vetor_fluxo = [] #vetor para salvar todos os resultados
vetor_fluxo_incerteza = [] #vetor de incertezas (na verdade é o desvio padrão (std))

# Navegue arquivo por arquivo coletando os resultados
for i in range(0, len(matriz_real)):
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

    f.write("fatores_nome = ")
    pprint(fatores_nome, stream=f)
    f.write("\n")

    f.write("fatores = ")
    pprint(fatores, stream=f)
    f.write("\n")
       
    f.write("matriz_planejamento = ")
    pprint(matriz_planejamento, stream=f)
    f.write("\n")
    
    f.write("matriz_real = ")
    pprint(matriz_real, stream=f)
    f.write("\n")

    f.write("vetor_fluxo = ")
    pprint(vetor_fluxo, stream=f)
    f.write("\n")
    
    f.write("vetor_fluxo_incerteza = ")
    pprint(vetor_fluxo_incerteza, stream=f)
    f.write("\n")
    