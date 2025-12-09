########################################################################
####                                                                ####
####       CENTRO DE DESENVOLVIMENTO DA TECNOLOGIA NUCLEAR          ####
####                      libPlajFatorial.py                        ####
####             Biblioteca de planejamento fatorial                ####
####                 Thalles Oliveira Campagnani                    ####
####                                                                ####
########################################################################




import itertools
from functools import reduce
import operator

def criaPlanejamento(fatores, fracionado=0, ponto_centrais=0):
    """
    Gera matriz de planejamento 2^k ou fracionado com regras de multiplicação customizadas.
    
    Regras de fração implementadas:
    - fracionado=1: Última coluna é o produto de TODAS as anteriores (Ex: E = A*B*C*D).
    - fracionado>=2:
        - Se nº colunas base é PAR: Pares disjuntos (Ex: E=A*B, F=C*D).
        - Se nº colunas base é ÍMPAR: Pares sequenciais (Ex: D=A*B, E=B*C).
    """
    
    # 1. Definir quantas colunas são independentes (a base)
    n_base = fatores - fracionado
    
    if n_base < 2 and fracionado > 0:
        raise ValueError("Número de fatores base insuficiente para gerar frações.")

    matriz_final = []

    # 2. Gerar a parte Fatorial (+1/-1)
    # Usamos reversed para garantir a ordem de Yates (+1, -1 na primeira coluna)
    combinacoes_base = itertools.product([1, -1], repeat=n_base)
    
    for comb in combinacoes_base:
        linha_base = list(reversed(comb)) # Ex: [A, B, C]
        colunas_extras = []
        
        # --- Lógica de Geração das Colunas Fracionadas ---
        if fracionado == 1:
            # Regra: Multiplicação de TODAS as outras
            # Ex: E = A * B * C * D
            valor = reduce(operator.mul, linha_base)
            colunas_extras.append(valor)
            
        elif fracionado >= 2:
            # Regra: Multiplicação de pares
            for i in range(fracionado):
                if n_base % 2 == 0:
                    # BASE PAR (Ex: 4 bases -> A,B,C,D)
                    # Usa pares separados: AB, CD, EF...
                    # i=0 -> idx 0 e 1 (A*B)
                    # i=1 -> idx 2 e 3 (C*D)
                    idx1 = (i * 2) % n_base
                    idx2 = (i * 2 + 1) % n_base
                else:
                    # BASE ÍMPAR (Ex: 3 bases -> A,B,C)
                    # Usa "janela deslizante": AB, BC, CD...
                    # i=0 -> idx 0 e 1 (A*B)
                    # i=1 -> idx 1 e 2 (B*C)
                    idx1 = i % n_base
                    idx2 = (i + 1) % n_base
                
                valor = linha_base[idx1] * linha_base[idx2]
                colunas_extras.append(valor)

        # Junta a base com as novas colunas calculadas
        matriz_final.append(linha_base + colunas_extras)

    # 3. Adicionar Pontos Centrais (Linhas de Zeros)
    # Pontos centrais são sempre 0 em todas as colunas (base e geradas)
    linha_centro = [0] * fatores
    for _ in range(ponto_centrais):
        matriz_final.insert(0, linha_centro) # Insere no topo ou append no final, conforme preferir

    return matriz_final

def imprime_matriz(matriz, titulo):
    print(f"\n--- {titulo} ---\n")
    for linha in matriz: 
        print(linha)
    print()











def conv_matriz_real(matriz_orig, fatores_0, fatores_coef):
    # Validação das dimensões (colunas)
    num_colunas = len(matriz_orig[0])
    if len(fatores_0) != num_colunas or len(fatores_coef) != num_colunas:
        raise ValueError(f"Erro: A matriz tem {num_colunas} colunas, mas as listas de fatores têm tamanhos diferentes.")

	# Calcular coeficiente
    matriz_real = []
    for i in range(len(matriz_orig)):
        nova_linha = []
        # 4. Loop pelas colunas (j)
        for j in range(num_colunas):
            # Aplica a fórmula: Valor * Coeficiente + Ponto Central
            valor_transformado = (matriz_orig[i][j] * fatores_coef[j]) + fatores_0[j]
            nova_linha.append(valor_transformado)
        matriz_real.append(nova_linha)

    return matriz_real


def converte_matriz_real(matriz, fatores_reais):
    """
    Substitui os códigos (-1, 0, +1) pelos valores reais correspondentes.
    
    Args:
        matriz (list): Matriz de planejamento com -1, 0, +1.
        fatores_reais (list): Lista de 3 listas contendo os valores reais.
                              fatores_reais[0] -> valores para nível -1
                              fatores_reais[1] -> valores para nível  0
                              fatores_reais[2] -> valores para nível +1
    
    Returns:
        list: Nova matriz com os valores reais.
    """
    matriz_convertida = []

    for linha in matriz:
        linha_real = []
        for coluna_idx, codigo_nivel in enumerate(linha):
            # A mágica acontece aqui:
            # Se codigo é -1 -> index vira 0 (pega da lista de "low")
            # Se codigo é  0 -> index vira 1 (pega da lista de "center")
            # Se codigo é +1 -> index vira 2 (pega da lista de "high")
            index_fator = int(codigo_nivel + 1)
            
            valor = fatores_reais[index_fator][coluna_idx]
            linha_real.append(valor)
            
        matriz_convertida.append(linha_real)

    return matriz_convertida