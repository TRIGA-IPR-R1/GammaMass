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

def escreva_comentario(arquivo, comentario = None):
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


def simuVariaSimplesTarugo(
        # Configurações de variação
        ini,
        fin,
        passo,
        tipoVaria="area", #Outras opções: proporção, posição, largura, altura, comprimento
        vetor_varia = [],
        area = 100, #somente usado no caso de 'proporção'
        prop = 1, #somente usado no caso area


        # Controle de pastas, para se deve voltar uma pasta acima antes de criar
        voltar=True,
        
        # Configurações da simulação
        particulas = 100000,
        ciclos     = 100,

        # Configurações de outras geometrias e fonte
        ## Parâmetros do tarugo (Substituidos se gerados automaticamente)
        tarugo_esteira_pos = 0, #centralizado em cima da fonte
        tarugo_comprimento = 10,
        tarugo_largura     = 10,
        tarugo_altura      = 10,

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

    if vetor_varia:#Se vetor_veria estiver definido, ignore valores passados como parametros que são usados para gerar vetor_varia
        ini=None
        fin=None
        passo=None
    else:#Se vetor varia estiver vazio, gere altomaticamente conforme valores passados
        if tipoVaria == "proporção": #Se o tipo for proporção, gere pontos simetricamente em torno de 'ini'
            #Gera sequencia inversamente simetrica
            ini=1 #Sempre em torno da proporção 1:1
            sequencia_lado_direito = np.arange(ini, fin + (passo / 1000.0), passo)
            sequencia_lado_esquerdo = np.sort(1 / sequencia_lado_direito[1:])
            vetor_varia = np.concatenate((sequencia_lado_esquerdo, sequencia_lado_direito))
        else: #Para os outros casos gere linearmente de ini a fin
            vetor_varia = range(ini, fin+1, passo)



    # Realize as diversas simulações com a variação respectiva
    for varia in vetor_varia:
        # Crie uma pasta para cada variação, sem data.
        libGammaMass.mkdir(f"simulação.{varia}", data=False, voltar=(varia!=vetor_varia[0]))#Voltar é false apenas para a primeira execução

        print("################")
        print("######## Rodando variação: ")
        print(f"####### {tipoVaria} = {varia} ")
        print("################")

        # Varie a variável de acordo com o tipo de variação
        if tipoVaria == "area":
            tarugo_largura      = np.sqrt(varia)*prop
            tarugo_altura       = np.sqrt(varia)/prop

        elif tipoVaria == "proporção":
            tarugo_largura  = np.sqrt(area)*varia
            tarugo_altura   = np.sqrt(area)/varia

        elif tipoVaria == "posição":
            tarugo_esteira_pos           = varia

        elif tipoVaria == "largura":
            tarugo_largura               = varia

        elif tipoVaria == "altura":
            tarugo_altura                = varia

        elif tipoVaria == "comprimento":
            tarugo_comprimento = varia

        else:
            exit(1)




        # Criando reator no OpenMC
        detector = libGammaMass.Detector()
        # Alterando Geometria
        detector.geometria(
            # Valores gerados de acordo com os parâmetros
            tarugo_largura               = tarugo_largura,
            tarugo_altura                = tarugo_altura,
            tarugo_comprimento           = tarugo_comprimento,
            tarugo_esteira_pos           = tarugo_esteira_pos,
            # Repassar o restante dos parâmetros
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
        # Rodando configurações novamente para atualizar a fonte da simulação e alterar as configurações de simulação
        detector.configurações(particulas=particulas, ciclos=ciclos)

        detector.plotagem("plot.lateral.xy.png",  "xy")
        detector.plotagem("plot.frontal.yz.png",  "yz", rotacionar = True)
        #detector.plotagem("plot.superior.xz.png", "xz", rotacionar = True, origin=(0,52.35,0))


        intervalos_energias=np.linspace(5e3,2e6,2**10).tolist() # Intervalo de 5KeV a 2MeV dividido em 2¹⁰ canais
        
        #Configurações de tallies
        detector.tallies(init=True)     #Iniciar a lista de tallies
        detector.tallies_detector(energia=intervalos_energias, score="flux",         nome="espectroFluxo")           #1
        detector.tallies_detector(energia=intervalos_energias, score="pulse-height", nome="espectroPulso")           #2
        detector.tallies(export=True)   #Finalizar a lista (exportar tallies.xml)

        # Gerar os arquivos XML e simular
        detector.simular()




    # --- Seção responsável por extrair resultados dos experimentos ---
    if libGammaMass.simu == True: # Somente extraia caso tenha sido realizada as simulações

        libGammaMass.chdir("..") # Saia da pasta destinada a aultima simução

        # Crie os vetores para salvar todos os resultados (tallies de espectro)
        vetor_espectroFluxo     = [] #vetor para salvar todos os espectros de fluxo
        vetor_espectroFluxo_STD = [] #vetor para salvar todos os desvios padrão (std) dos espectros de fluxo
        vetor_espectroPulso     = [] #vetor para salvar todos os espectros de pulso
        vetor_espectroPulso_STD = [] #vetor para salvar todos os desvios padrão (std)) dos espectros de pulso
        
        # Navegue arquivo por arquivo coletando os resultados
        for i in vetor_varia:
            espectroFluxo, espectroFluxo_STD =     detector.tallies_detector(get=True,    nome="espectroFluxo", score="flux",          file=f"simulação.{i}/statepoint.{ciclos}.h5")
            espectroPulso, espectroPulso_STD =     detector.tallies_detector(get=True,    nome="espectroPulso", score="pulse-height",  file=f"simulação.{i}/statepoint.{ciclos}.h5")
            
            #Salve eles nos vetores
            vetor_espectroFluxo.append(espectroFluxo)
            vetor_espectroFluxo_STD.append(espectroFluxo_STD)
            vetor_espectroPulso.append(espectroPulso)
            vetor_espectroPulso_STD.append(espectroPulso_STD)







        # --- Seção responsável por salvar entradas e saídas de todos experimentos ---


        with open("resultados_simuVariaArea.py", "w") as f:  #### mudar nome para separar os casos
            escreva_comentario(f," Resultados da Simulação OpenMC - Função simuVariaArea\n\n")
            escreva_comentario(f," Arquivo gerado automaticamente\n\n")
            escreva_variaveis(f," Configurações de simulação:", particulas=particulas,  ciclos=ciclos)
            escreva_variaveis(f," Configurações de variação: (caso sejam None, significa que vetor_varia foi fornecido externamente)", tipoVaria=tipoVaria, ini=ini, fin=fin, passo=passo)
            escreva_comentario(f," Configurações de geometria e fonte:")
            escreva_variaveis(f,"# Parâmetros do tarugo (alguns gerados automaticamente):", tarugo_esteira_pos=tarugo_esteira_pos, tarugo_comprimento=tarugo_comprimento)
            escreva_variaveis(f,"# Parâmetros do colimador:",  colimador_espessura=colimador_espessura, colimador_abertura=colimador_abertura, colimador_impureza=colimador_impureza)
            escreva_variaveis(f,"# Parãmetros das fontes", fonte_cobalto_intensidade=fonte_cobalto_intensidade, fonte_raiosCosmicos_mes=fonte_raiosCosmicos_mes, fonte_raiosCosmicos_latitude=fonte_raiosCosmicos_latitude)
            escreva_variaveis(f,"# Parametros do detector", detectores_numero=detectores_numero, detectores_altura_meio=detectores_altura_meio, detectores_altura_esquerda=detectores_altura_esquerda, detectores_altura_direita=detectores_altura_direita)
            escreva_variaveis(f,"# Parametros concreto", fonte_Concreto_intensidade=fonte_Concreto_intensidade)
            escreva_comentario(f," Espectro para resultados:")
            escreva_variaveis(f," Intervalos de energias que são divididos os tallies de fluxo e altura de pulso", intervalos_energias=intervalos_energias)
            escreva_comentario(f," Resultados:\n\n")
            escreva_variaveis(f,"# Vetor contendo cada variação simulada",vetor_varia=vetor_varia)
            escreva_variaveis(f,"# Vetor contendo o espectro de fluxo para cada variação simulada",vetor_espectroFluxo=vetor_espectroFluxo)
            escreva_variaveis(f,"# Vetor contendo o espectro de desvio padrão do fluxo para cada variação simulada",vetor_espectroFluxo_STD=vetor_espectroFluxo_STD)
            escreva_variaveis(f,"# Vetor contendo o espectro de pulso para cada variação simulada",vetor_espectroPulso=vetor_espectroPulso)
            escreva_variaveis(f,"# Vetor contendo o espectro de desvio padrão do pulso para cada variação simulada",vetor_espectroPulso_STD=vetor_espectroPulso_STD)















