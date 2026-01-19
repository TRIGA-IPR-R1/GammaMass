import matplotlib.pyplot as plt
import numpy as np




def plot_padrao(
    eixo_x,                 #Obrigatório: Lista de numeros que compõem o eixo x
    vetor_eixo_y,           #Obrigatório: Lista de numeros que compõem o eixo y, ou uma lista de várias listas de eixos y
    vetor_eixo_y_std=None,  #Lista de numeros que compõem o desvio padrão do eixo y, ou uma lista de várias listas de desvio padrão do eixo y
    vetor_legenda=None,     #Legenda do gráfico, ou uma lista de legenda do mesmo tamanho que a quantidade de eixo y
    vetor_cores=None,       #Cor do gráfico, ou uma lista de cores do mesmo tamanho que a quantidade de eixo y
    salvar=None,            #Nome do arquivo para ser salvo
    plotar=True,
    titulo="",
    xlabel="",
    ylabel=""
    ):

    plt.figure(figsize=(10, 6))

    # Se for único eixo y, envolvemos em uma lista [] para o loop funcionar igual.
    multiplo = isinstance(vetor_eixo_y[0], (list, tuple, np.ndarray))
    if not multiplo:
        vetor_eixo_y = [vetor_eixo_y]
        if vetor_eixo_y_std is not None:
            vetor_eixo_y_std = [vetor_eixo_y_std]

    # Loop de Plotagem 
    for i, eixo_y in enumerate(vetor_eixo_y):
        
        # Define a cor (se o vetor existir e tiver índice suficiente)
        cor = None
        if vetor_cores and i < len(vetor_cores):
            cor = vetor_cores[i]
            
        # Define a legenda (se o vetor existir e tiver índice suficiente)
        label = None
        if vetor_legenda and i < len(vetor_legenda):
            label = vetor_legenda[i]
            
        # Define o erro padrão para esta curva específica
        yerr = None
        if vetor_eixo_y_std is not None and i < len(vetor_eixo_y_std):
            yerr = vetor_eixo_y_std[i]

        # Plota com ou sem barra de erro
        if yerr is not None:
            plt.errorbar(
                eixo_x, 
                eixo_y, 
                yerr=yerr, 
                fmt='o-', 
                color=cor,     # Usa a cor definida ou automática se None
                ecolor='red', # Cor da barra de erro (opcional, ou usar 'cor')
                elinewidth=2, 
                capsize=5, 
                label=label,
                alpha=0.8
            )
        else:
            plt.plot(
                eixo_x, 
                eixo_y, 
                'o-', 
                color=cor, 
                label=label
            )

    # Estilização
    plt.title(titulo, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Só exibe a legenda se houver labels definidos
    if vetor_legenda:
        plt.legend()

    # Só salva se o nome do arquivo estiver definido
    if salvar is not None:
        plt.savefig(f"{salvar}.png", dpi=300)
        plt.savefig(f"{salvar}.pdf", dpi=300)
        print(f"Gráfico salvo como '{salvar}.png' e '{salvar}.pdf'")
        
    if plotar:
        plt.show()
        

    
    
# Só executa se for executado diretamente, caso seja importado não execute
if __name__ == "__main__":

    # Substitua $$$ pela path até o diretorio que contem o arquivo de resultados
    import $$$.resultados_simuVariaTarugo as r
    import $$$$.resultados_simuVariaTarugo as r

    # Plotar gráfico de fluxo e pulso total com barra de erro
    plot_padrao(r.vetor_varia, r.fluxo_total, r.fluxo_total_std)
    plot_padrao(r.vetor_varia, r.pulso_total, r.pulso_total_std)
    # Comparar os 2 sem barra de erro
    plot_padrao(r.vetor_varia, [r.fluxo_total, r.pulso_total])

    # Repete para energia entre cobalto
    plot_padrao(r.vetor_varia, r.fluxo_entreCobalto, r.fluxo_entreCobalto_std)
    plot_padrao(r.vetor_varia, r.pulso_entreCobalto, r.pulso_entreCobalto_std)
    plot_padrao(r.vetor_varia, [r.fluxo_entreCobalto, r.pulso_entreCobalto])