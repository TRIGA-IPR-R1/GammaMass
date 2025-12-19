import openmc.data
import matplotlib.pyplot as plt

# Carregando os dados
c_photon = openmc.data.IncidentPhoton.from_hdf5('/opt/nuclear-data/endfb-viii.0-hdf5/photon/C.h5')

# OPÇÃO A: Acessar a seção de choque TOTAL (soma de todos os processos)
energias = c_photon.energy
sigma_total = c_photon.total_xs

# OPÇÃO B: Se quiser uma reação específica via dicionário de reações
# Vamos listar as chaves para você ver o que existe:
print(f"Reações disponíveis: {c_photon.reactions.keys()}")

# Se quiser plotar, por exemplo, o efeito fotoelétrico:
# reacao = c_photon.reactions[522] 
# energias = reacao.xs.x
# sigma = reacao.xs.y

# --- Plotagem da Seção de Choque Total ---
plt.figure(figsize=(10, 6))
plt.loglog(energias, sigma_total, label='Carbono - Coef. de Atenuação Total')
plt.xlabel('Energia [eV]')
plt.ylabel('Seção de Choque [barns]')
plt.title('Interação de Fótons com o Carbono (ENDF/B-VIII.0)')
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.legend()
plt.show()