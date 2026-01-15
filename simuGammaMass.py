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






# --- Seção responsável por executar o experimento ---

import libGammaMass
libGammaMass.simu = True
libGammaMass.plotar = False


def simuVariaArea(fonte_cobalto_intensidade=7.4e6,colimador_espessura = 2.7,voltar=True):
    # Cria pasta com data no nome para armazenar os resultados
    libGammaMass.mkdir("resultados_"+str(int(fonte_cobalto_intensidade))+"_"+str(int(colimador_espessura*10)), data=False, voltar=voltar)

    #Configurações da simulação
    config = [20000, 100] #Particulas, ciclos totais


    #Simular todos os casos usando matriz_real para alterar parâmetros da simulação
    #for i in range(0, len(matriz_real)):

    area_ini = 0
    area_fin = 625 #25x25
    passo    = 25
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
            tarugo_altura  = np.sqrt(area),
            tarugo_largura = np.sqrt(area),
            fonte_cobalto_intensidade    = fonte_cobalto_intensidade,
            colimador_espessura= colimador_espessura,
            fonte_Concreto_intensidade = 0
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

        from pprint import pprint
        with open("resultados_experimentos.py", "w") as f:  #### mudar nome para separar os casos
            f.write("# Resultados da Simulação OpenMC\n")
            f.write("# Arquivo gerado automaticamente\n\n")
            
            f.write("config = ")
            pprint(config, stream=f)
            f.write("\n")

            f.write("colimador_espessura = ")
            pprint(colimador_espessura, stream=f)
            f.write("\n")

            f.write("fonte_cobalto_intensidade = ")
            pprint(fonte_cobalto_intensidade, stream=f)
            f.write("\n")

            f.write("intervalos_energias = ")
            pprint(intervalos_energias, stream=f)
            f.write("\n")

            f.write("vetor_area = ")
            pprint(vetor_area, stream=f)
            f.write("\n")

            f.write("vetor_fluxo = ")
            pprint(vetor_fluxo, stream=f)
            f.write("\n")
            
            f.write("vetor_fluxo_incerteza = ")
            pprint(vetor_fluxo_incerteza, stream=f)
            f.write("\n")

            f.write("vetor_pulso = ")
            pprint(vetor_pulso, stream=f)
            f.write("\n")
            
            f.write("vetor_pulso_incerteza = ")
            pprint(vetor_pulso_incerteza, stream=f)
            f.write("\n")









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