#GRAFICO


'''alturas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
fluxos = [1.59e+05, 1.59e+05, 1.59e+05, 1.59e+05, 1.59e+05, 1.59e+05, 1.60e+05, 1.60e+05, 1.60e+05, 1.61e+05, 1.59e+05 , 1.56e+05, 
        1.53e+05, 1.46e+05, 1.40e+05, 1.36e+05, 1.27e+05, 1.19e+05, 1.11e+05, 9.40e+04, 7.70e+04, 6.17e+04, 4.62e+04, 2.99e+04, 1.92e+04, 1.76e+04, 1.72e+04]


std = [4.46e+03, 4.40e+03, 4.42e+03, 4.42e+03, 4.41e+03, 4.41e+03, 4.44e+03, 4.46e+03, 4.52e+03, 4.57e+03, 4.61e+03, 4.54e+03, 
       4.39e+03, 4.30e+03, 4.43e+03, 4.28e+03, 4.29e+03, 3.95e+03, 4.25e+03, 3.69e+03, 3.13e+03, 2.67e+03, 2.27e+03, 1.83e+03, 
       1.66e+03, 1.58e+03, 1.55e+03]


# Cálculo do desvio padrão médio
#desvio_medio = np.mean(std)

# Plotagem do gráfico
plt.figure(figsize=(12, 7))
plt.errorbar(alturas, fluxos, yerr=std, fmt='o-', color='deepskyblue', ecolor='gray', capsize=5, label='Fluxo por Iteração')
plt.axhline(y=desvio_medio, color='r', linestyle='--', label='Desvio Padrão Médio')

plt.xlabel('Iteração')
plt.ylabel('Fluxo')
plt.title('Fluxo por Iteração com Desvio Padrão')
plt.legend()
plt.grid(True)
plt.show()'''

import matplotlib.pyplot as plt
import numpy as np

# Dados
alturas = np.arange(0, 27)
fluxos = np.array([
    1.59e+05, 1.59e+05, 1.59e+05, 1.59e+05, 1.59e+05, 1.59e+05,
    1.60e+05, 1.60e+05, 1.60e+05, 1.61e+05, 1.59e+05, 1.56e+05,
    1.53e+05, 1.46e+05, 1.40e+05, 1.36e+05, 1.27e+05, 1.19e+05,
    1.11e+05, 9.40e+04, 7.70e+04, 6.17e+04, 4.62e+04, 2.99e+04,
    1.92e+04, 1.76e+04, 1.72e+04
])

std = np.array([
    4.46e+03, 4.40e+03, 4.42e+03, 4.42e+03, 4.41e+03, 4.41e+03,
    4.44e+03, 4.46e+03, 4.52e+03, 4.57e+03, 4.61e+03, 4.54e+03,
    4.39e+03, 4.30e+03, 4.43e+03, 4.28e+03, 4.29e+03, 3.95e+03,
    4.25e+03, 3.69e+03, 3.13e+03, 2.67e+03, 2.27e+03, 1.83e+03,
    1.66e+03, 1.58e+03, 1.55e+03
])

# Gráfico
plt.figure(figsize=(12, 7))
plt.errorbar(
    alturas, fluxos, yerr=std, fmt='o-', color='darkorange',
    ecolor='slategray', capsize=5, linewidth=2, markersize=8,
    label='(Fluxo ± Desvio Padrão)cm²/s'
)

# Linha do desvio padrão médio (opcional, pois não é fluxo)
# plt.axhline(y=np.mean(std), color='royalblue', linestyle='--',
#            label=f'Desvio Médio: {np.mean(std):.1e}')

plt.xlabel('Altura cm')
plt.gca().invert_xaxis()   # altura diminuindo
plt.ylabel('Fluxo cm²/s')
plt.title('Fluxo de Fótons no Detector por Altura do Tarugo')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.show()
