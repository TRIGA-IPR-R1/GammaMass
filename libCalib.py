from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np


def sum_espectro(vetor_varia, vetor_espectro, intervalos_energias=None, intervalo_sum=None):
    """
    Soma o espectro, opcionalmente dentro de um intervalo de energia específico.
    """
    
    # Índices padrão para fatiamento (slice) do array: [começo : fim]
    idx_inicio = 0
    idx_fim = None # None em fatiamento significa "até o final"

    # Se os argumentos opcionais foram fornecidos, calculamos os novos índices
    if intervalos_energias is not None and intervalo_sum is not None:
        min_ev, max_ev = intervalo_sum
        
        # Função auxiliar para encontrar o índice do valor mais próximo na lista
        def encontrar_indice_mais_proximo(array, valor):
            distancias = [abs(x - valor) for x in array]
            return distancias.index(min(distancias))

        # Encontramos os índices correspondentes aos valores de energia
        idx_inicio = encontrar_indice_mais_proximo(intervalos_energias, min_ev)
        idx_fim = encontrar_indice_mais_proximo(intervalos_energias, max_ev)

        # Validação simples para garantir que inicio < fim
        if idx_inicio > idx_fim:
            idx_inicio, idx_fim = idx_fim, idx_inicio
            
        # Nota: Se idx_inicio == idx_fim, o intervalo é muito pequeno ou
        # cai dentro de uma única borda, resultando em soma 0.

    somatoria = []
    
    for i, varia in enumerate(vetor_varia):
        espectro = vetor_espectro[i]
        
        # Realizamos o slice (fatiamento) da lista baseado nos índices encontrados
        # Se os opcionais não foram passados, será espectro[0 : None], ou seja, tudo.
        parte_espectro = espectro[idx_inicio:idx_fim]
        
        somatoria.append(sum(parte_espectro))
        
    return somatoria

def calcula_curva_calibracao_area(vetor_area, medicao, grau_regressao=2, plotar=False):
    """
    Gera uma função de calibração polinomial e plota gráficos de resíduos.

    Args:
        vetor_area (list/array): Valores reais de área (Target).
        medicao (list/array): Valores de contagem/pulso (Feature).
        grau_regressao (int): Grau do polinômio de ajuste.

    Returns:
        modelo (func): Função matemática f(pulsos) -> área.
        r2 (float): Coeficiente de determinação.
        erro_absoluto (array): Diferença (Calculado - Real) para cada ponto.
        erro_percentual (array): Erro relativo em % para cada ponto.
    """
    
    # 1. Preparação dos dados
    y_area_real = np.array(vetor_area) # O que queremos descobrir (Eixo Y da calibração)
    x_pulsos = np.array(medicao)       # O que medimos (Eixo X da calibração)
    
    # 2. Ajuste Polinomial (Fit)
    coeficientes = np.polyfit(x_pulsos, y_area_real, grau_regressao)
    modelo_matematico = np.poly1d(coeficientes)
    
    # 3. Cálculos de Validação (usando os próprios pontos de treino)
    y_area_calc = modelo_matematico(x_pulsos)
    erro_absoluto = y_area_calc - y_area_real
    
    # --- CORREÇÃO DO ERRO PERCENTUAL ---
    # Inicializa vetor com zeros
    erro_percentual = np.zeros_like(y_area_real)
    
    # Cria uma máscara para identificar onde a área NÃO é zero
    # Usamos uma pequena tolerância (1e-9) caso sejam floats muito pequenos
    mask_valid = (np.abs(y_area_real) > 1e-9)
    
    # Calcula a porcentagem apenas para os valores válidos
    erro_percentual[mask_valid] = (erro_absoluto[mask_valid] / y_area_real[mask_valid]) * 100
    
    # (Opcional) Nos pontos onde area_real == 0, o erro percentual ficará como 0.0,
    # o que evita o gráfico explodir.
    # -----------------------------------

    r2 = r2_score(y_area_real, y_area_calc) if len(y_area_real) > 1 else 0
    erro2medio = np.sqrt(np.mean(erro_percentual**2))
    
    if plotar:
        # 4. Plotagem dos 3 Gráficos
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
        
        # --- Gráfico 1: Curva de Calibração ---
        # Pontos reais
        ax1.scatter(x_pulsos, y_area_real, color='red', label='Dados OpenMC', zorder=5)
        # Linha de tendência suave
        x_linha = np.linspace(x_pulsos.min(), x_pulsos.max(), 100)
        ax1.plot(x_linha, modelo_matematico(x_linha), color='blue', label=f'Modelo (Grau {grau_regressao})')
        
        ax1.set_ylabel('Área Calculada')
        ax1.set_title(f'1. Curva de Calibração (Contagem $\\rightarrow$ Área) | $R^2 = {r2:.4f}$')
        ax1.legend()
        ax1.grid(True, linestyle='--', alpha=0.5)
        
        # --- Gráfico 2: Erro Absoluto ---
        ax2.plot(x_pulsos, erro_absoluto, 'o', color='green')
        ax2.axhline(0, color='black', linewidth=1) # Linha do zero
        ax2.set_ylabel('Erro Absoluto\n($A_{calc} - A_{real}$)')
        ax2.set_title('2. Erro Absoluto (Resíduos)')
        ax2.grid(True, linestyle='--', alpha=0.5)
        
        # --- Gráfico 3: Erro Percentual ---
        ax3.plot(x_pulsos, erro_percentual, 'o', color='purple')
        ax3.axhline(0, color='black', linewidth=1) # Linha do zero
        ax3.set_ylabel('Erro Percentual (%)')
        ax3.set_xlabel('Contagem de Pulsos (Leitura)')
        ax3.set_title('3. Erro Percentual Relativo')
        ax3.grid(True, linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        plt.show()

    return modelo_matematico, r2, erro_absoluto, erro_percentual, erro2medio
