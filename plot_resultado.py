import os
os.system("clear")
import matplotlib.pyplot as plt
import numpy as np


#
# COLOCAR ESSE ARQUIVO DENTRO DA PASTA DE RESULTADOS!!!!!
# (ou colocar o nome da pasta de resultados no import abaixo: nome_pasta.pasta_interna.resultados_experimentos)
#
import resultados_experimentos as r

def somar_por_intervalo(intervalo_alvo, lista_energias, dados_tally):
    """
    Soma os valores do tally dentro de um intervalo de energia específico.
    
    :param intervalo_alvo: Lista ou tupla com [E_min, E_max] em eV.
    :param lista_energias: A lista 'intervalos_energias' usada no filtro (edges).
    :param dados_tally: O vetor de resultados (ex: vetor_fluxo[i]).
    :return: Soma total no intervalo e a incerteza propagada.
    """
    e_min, e_max = intervalo_alvo
    
    # Converter para array numpy para busca rápida
    energias = np.array(lista_energias)
    
    # Encontrar os índices onde o intervalo se encaixa
    # np.searchsorted encontra onde o valor seria inserido para manter a ordem
    idx_inicio = np.searchsorted(energias, e_min) - 1
    idx_fim = np.searchsorted(energias, e_max) - 1
    
    # Garantir que os índices fiquem dentro dos limites dos dados
    idx_inicio = max(0, idx_inicio)
    idx_fim = min(len(dados_tally), idx_fim)
    
    # Selecionar a fatia (slice) dos dados
    fatia_dados = dados_tally[idx_inicio:idx_fim]
    
    return sum(fatia_dados)

def somar_vetor_por_intervalo(intervalo_alvo, lista_energias, lista_de_resultados):
    """
    Processa uma lista de resultados e retorna um novo vetor com as somas no intervalo.
    
    :param intervalo_alvo: [E_min, E_max] em eV.
    :param lista_energias: Os bins (edges) de energia do tally.
    :param lista_de_resultados: O vetor de vetores (ex: vetor_pulso).
    :return: Uma lista com a soma para cada simulação.
    """
    e_min, e_max = intervalo_alvo
    energias = np.array(lista_energias)
    
    # Identifica os índices dos canais apenas uma vez
    idx_inicio = np.searchsorted(energias, e_min) - 1
    idx_fim = np.searchsorted(energias, e_max) - 1
    
    # Garante limites válidos
    idx_inicio = max(0, idx_inicio)
    
    # Lista para armazenar os resultados finais
    vetor_somas = []
    
    for resultado in lista_de_resultados:
        # Pega a fatia do espectro e soma
        fatia = resultado[idx_inicio:idx_fim]
        vetor_somas.append(sum(fatia))
        
    return vetor_somas

def plot_com_error_bar(
    eixo_x,
    eixo_y,
    eixo_y_err,
    titulo,
    xlabel,
    ylabel,
    arquivo
    ):
    
    # 2. Definindo o eixo X (Assumindo que são passos ou índices)
    # Se você tiver as posições em cm, substitua esta linha:
    #eixo_x = np.arange(len(vetor_fluxo)) 

    # 3. Criando o gráfico
    plt.figure(figsize=(10, 6)) # Tamanho da figura (largura, altura)

    # A função mágica aqui é a 'errorbar'
    plt.errorbar(
        eixo_x, 
        eixo_y, 
        yerr=eixo_y_err, 
        fmt='o-',        # 'o' para bolinha, '-' para linha ligando
        color='blue',    # Cor da linha
        ecolor='red',    # Cor da barra de erro
        elinewidth=2,    # Espessura da barra de erro
        capsize=5,       # Tamanho do "tracinho" no topo da barra de erro
        label='Fluxo Medido'
    )

    # 4. Formatação
    plt.title(titulo, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7) # Grade para facilitar leitura
    plt.legend()

    # 5. Salvar e Mostrar
    plt.savefig(f"{arquivo}.png", dpi=300) # Salva com alta qualidade
    print(f"Gráfico salvo como '{arquivo}.png'")
    plt.show()


def plot_mais_de_um(
    eixo_x,
    vetor_eixo_y,
    titulo,
    xlabel,
    ylabel,
    arquivo,
    transpor=True
    ):
    if transpor:
        vetor_eixo_y_np = np.array(vetor_eixo_y).T
    else:
        vetor_eixo_y_np = np.array(vetor_eixo_y)
        

    # 3. Criando o gráfico
    plt.figure(figsize=(10, 6)) # Tamanho da figura (largura, altura)

    # A função mágica aqui é a 'errorbar'
    for vetor in vetor_eixo_y_np.T:
        plt.plot(eixo_x,vetor)

    # 4. Formatação
    plt.title(titulo, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7) # Grade para facilitar leitura
    plt.legend()

    # 5. Salvar e Mostrar
    plt.savefig(f"{arquivo}.png", dpi=300) # Salva com alta qualidade
    print(f"Gráfico salvo como '{arquivo}.png'")
    plt.show()
    
vetor_fluxo = []
for fluxo in r.vetor_fluxo:
    vetor_fluxo.append(sum(fluxo))
    
vetor_fluxo_incerteza = []
for fluxo_incerteza in r.vetor_fluxo_incerteza:
    vetor_fluxo_incerteza.append(sum(fluxo_incerteza))
    
plot_com_error_bar(
    eixo_x = r.vetor_area,
    eixo_y = vetor_fluxo,
    eixo_y_err = vetor_fluxo_incerteza,
    titulo = "fluxo vs. area",
    xlabel = "area",
    ylabel = "fluxo",
    arquivo = "resultados_fluxo")


vetor_pulso = []
for pulso in r.vetor_pulso:
    vetor_pulso.append(sum(pulso))
    
vetor_pulso_incerteza = []
for pulso_incerteza in r.vetor_pulso_incerteza:
    vetor_pulso_incerteza.append(sum(pulso_incerteza))
    
plot_com_error_bar(
    eixo_x      = r.vetor_area,
    eixo_y      = vetor_pulso,
    eixo_y_err  = vetor_pulso_incerteza,
    titulo      = "pulso vs. area",
    xlabel      = "area",
    ylabel      = "pulso",
    arquivo     = "resultados_pulso")

plot_mais_de_um(
    eixo_x          = r.vetor_area,
    vetor_eixo_y    = [vetor_fluxo, vetor_pulso],
    titulo          = "[vetor_fluxo,vetor_pulso]",
    xlabel          = "area",
    ylabel          = "fluxo & pulso",
    arquivo         = "[vetor_fluxo,vetor_pulso]")

intervalos_energias=np.linspace(5e3,2e6,2**10).tolist()
vetor_pulso_intervalo_cobalto = somar_vetor_por_intervalo([1.1e6, 1.4e6], intervalos_energias, r.vetor_pulso)

plot_mais_de_um(
    eixo_x          = r.vetor_area,
    vetor_eixo_y    = [vetor_pulso,vetor_pulso_intervalo_cobalto],
    titulo          = "[vetor_pulso,vetor_pulso_intervalo_cobalto]",
    xlabel          = "area",
    ylabel          = "pulso",
    arquivo         = "[vetor_fluxo,vetor_pulso_intervalo_cobalto]")