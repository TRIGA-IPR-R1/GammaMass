import openmc
import numpy as np
import openmc.model
from matplotlib import pyplot as plt
import os
from datetime import datetime


# Criar pasta e mudar para a pasta criada:
def mkdir(nome="teste_sem_nome",data=True,voltar=False):
    if (voltar==True):
        os.chdir("../")
    if (data==True):
        agora = datetime.now()
        nome = agora.strftime(nome+"_%Y%m%d_%H%M%S")
    if not os.path.exists(nome):
        os.makedirs(nome)
    os.chdir(nome)


#Mudar para a pasta
def chdir(nome=None):
    if (nome != None):
        os.chdir(nome)
    else:
        diretorio_atual = os.getcwd()
        diretorios = [diretorio for diretorio in os.listdir(diretorio_atual) if os.path.isdir(os.path.join(diretorio_atual, diretorio))]

        data_mais_recente = 0
        pasta_mais_recente = None

        for diretorio in diretorios:
            data_criacao = os.path.getctime(os.path.join(diretorio_atual, diretorio))
            if data_criacao > data_mais_recente:
                data_mais_recente = data_criacao
                pasta_mais_recente = diretorio

        if pasta_mais_recente:
            os.chdir(os.path.join(diretorio_atual, pasta_mais_recente))
            print("Diretório mais recente encontrado:", pasta_mais_recente)
        else:
            print("Não foi possível encontrar um diretório mais recente.")





# Controle das iterações
UPPER_TARUGO_INICIAL = 25
UPPER_TARUGO_FINAL= 6
UPPER_TARUGO_INCREMENTO=-1

#Lista de resultados
UPPER_TARUGO_lista = []
lista_fluxos = []
lista_std_dev = []

#Cria uma pasta RODA_DATA com todos os resultados dentro
mkdir(nome="Bancada_variavel",data=True,voltar=False)

UPPER_TARUGO = UPPER_TARUGO_INICIAL
while UPPER_TARUGO >= UPPER_TARUGO_FINAL:
    #Cria uma pasta para o resultado, volta para pasta anterior antes de criar nova pasta caso não seja a primeira iteração
    mkdir(nome=f"UPPER_TARUGO={UPPER_TARUGO}",data=False,voltar=(UPPER_TARUGO<UPPER_TARUGO_INICIAL) )



    # ======================
    # Materiais
    # ======================

    # Material 1 - Fonte de Cobalto (Co-60)
    cobalto = openmc.Material(name='Fonte de Cobalto')
    cobalto.add_nuclide('Co59', 1.0)
    cobalto.set_density('g/cm3', 8.9)

    # Material 2 - Aço
    aco = openmc.Material(name='Aço')
    aco.add_element('Fe', 0.98)
    aco.add_element('C', 0.02)
    aco.set_density('g/cm3', 7.85)

    # Material 3 - Detector de Cristal de Iodeto de Cesio
    csi = openmc.Material(name='Detector de CsI')
    csi.add_nuclide('Cs133', 0.5)
    csi.add_nuclide('I127', 0.5)
    csi.set_density('g/cm3', 4.51)

    # Material 4 - Água
    agua = openmc.Material(name='Água')
    agua.add_nuclide('H1', 2.0)
    agua.add_nuclide('O16', 1.0)
    agua.set_density('g/cm3', 1.0)

    # Material 5 - Ar
    ar = openmc.Material(name='Ar')
    ar.add_nuclide('N14', 0.755)
    ar.add_nuclide('O16', 0.231)
    ar.add_nuclide('Ar40', 0.013)
    ar.set_density('g/cm3', 0.001225)

    # Criação do conjunto de materiais
    materials = openmc.Materials([cobalto, aco, csi, agua, ar])
    materials.cross_sections = "/home/jefferson/GammaMass/nuclear-data/endfb-viii.0-hdf5/cross_sections.xml"
    materials.export_to_xml()
    #print(materials)

    colors = {
        cobalto: 'blue',
        aco: 'yellow',
        ar: 'pink',
        csi: 'black',
        agua: 'gray',
    }




    # ======================
    # Geometria (& intersection, > union,  ~ complement.)
    # ======================
    # Fonte (Co-60)
    Co60_cyl=openmc.ZCylinder(x0=0, y0=-13.34, r=0.35) #
    plane_z_min = openmc.ZPlane(z0=0)
    plane_z_max = openmc.ZPlane(z0=23.4)

    fonte_cell = openmc.Cell(name='Fonte Co60')
    fonte_cell.region = -Co60_cyl & +plane_z_min & -plane_z_max
    fonte_cell.fill = cobalto

    # Água
    H2O_cyl=openmc.ZCylinder(x0=0, y0=-13.34, r=6) 

    agua_cell = openmc.Cell(name='Água')
    agua_cell.region = -H2O_cyl & +Co60_cyl & +plane_z_min & -plane_z_max
    agua_cell.fill = agua


    # Tarugo de Aço Altura 7.4-24.4 !! FALTA ARRUMAR ELE SENDO ALTURA NEGATIVA
    tarugo_superficie = openmc.model.RectangularPrism(width=6.75, height=6.75, axis = 'z', origin=(0,0,0))


    #UPPER_TARUGO = 7.4 #UPPER_TARUGO está sendo definido no FOR!!!!

    BOTTOM_TARUGO  = UPPER_TARUGO - 16.6
    plane_z_min_tarugo = openmc.ZPlane(z0=BOTTOM_TARUGO)
    plane_z_max_tarugo = openmc.ZPlane(z0=UPPER_TARUGO) 



    tarugo_cell = openmc.Cell(name='Tarugo de Aço')
    tarugo_cell.region = -tarugo_superficie & +plane_z_min_tarugo & -plane_z_max_tarugo 
    tarugo_cell.fill = aco

    # Detector de Cristal de CsI

    radius_CsI=2
    NaI_cyl = openmc.YCylinder(x0=0.0, z0=21.4, r=radius_CsI)
    plane_y_min = openmc.YPlane(y0=12.32)
    plane_y_max = openmc.YPlane(y0=17.32)

    detector_cell = openmc.Cell(name='Detector de CsI')
    detector_cell.region = -NaI_cyl & +plane_y_min & -plane_y_max
    detector_cell.fill = csi

    # Ar
    plane_y_max_vazio = openmc.YPlane(y0=25, boundary_type='vacuum')
    plane_y_min_vazio = openmc.YPlane(y0=-25, boundary_type='vacuum')
    plane_x_max_vazio = openmc.XPlane(x0=15, boundary_type='vacuum')
    plane_x_min_vazio = openmc.XPlane(x0=-15, boundary_type='vacuum')
    plane_z_max_vazio = openmc.ZPlane(z0=30, boundary_type='vacuum')
    plane_z_min_vazio = openmc.ZPlane(z0=-15, boundary_type='vacuum')

    ### O EIXO 'Y' É NA HORIZONTAL DO DESENHO E O 'Z' NA VERTICAL DO DESENHO ###

    ar_cell = openmc.Cell(name='Ar')
    plane_esquerda_tarugo = openmc.YPlane(y0=-6.75/2)
    # Todas as parte de ar em uma só célula
    ar_cell.region =  (-plane_y_max_vazio & +plane_y_max & -plane_z_max_vazio & +plane_z_min_vazio |
                    -plane_y_max & +plane_y_min & +NaI_cyl & -plane_z_max_vazio & +plane_z_min_vazio |
                    -plane_y_min & +tarugo_superficie & +plane_esquerda_tarugo & -plane_z_max_vazio & +plane_z_min_vazio |
                    -tarugo_superficie & +plane_z_min_vazio & -plane_z_min_tarugo |
                    -tarugo_superficie & +plane_z_max_tarugo & -plane_z_max_vazio |
                    +H2O_cyl & -plane_z_max_vazio & +plane_z_min_vazio & +plane_y_min_vazio & -plane_esquerda_tarugo |
                    -H2O_cyl & -plane_z_max_vazio & +plane_z_max |
                    -H2O_cyl & +plane_z_min_vazio & -plane_z_min)
    ar_cell.fill = ar

    # Criação do universo
    universe_1 = openmc.Universe(cells=[fonte_cell, agua_cell, tarugo_cell, detector_cell, ar_cell])
    #universe_1.plot(width=(50,50), origin=(0,0,0), basis='xy')
    geometry = openmc.Geometry()
    geometry.root_universe = universe_1
    geometry.export_to_xml()



    # ======================
    # Parâmetros de Plotagem
    # ======================
    plot = openmc.Plot()
    plot.filename = 'geometry_plot.png'  
    plot.basis = ('yz')
    plot.width = (60 , 60)
    plot.pixels = (3000, 3000)
    plot.origin = (0, 0, 7)
    plot.color_by = 'material'
    plot.colors = colors
    plots = openmc.Plots([plot])
    plot.show_edges = True  # Mostrar bordas das células
    plot.show_labels = True  # Mostrar rótulos das células

    plots.export_to_xml()
    openmc.plot_geometry()

    #from IPython.display import Image
    #Image('geometry_plot.png')
    #xdg-open geometry_plot.png


    #secao_transversal = openmc.Plot.from_geometry(geometry)


    # ======================
    # Fonte
    # ======================

    # Espectro de energia do Cobalto-60
    energy_dist = openmc.stats.Discrete([1.1732e6, 1.3325e6], [0.5, 0.5])

    # Distribuição espacial (raio entre 0 e 0.35 cm, cilindro ao longo do eixo z)
    radius_dist = openmc.stats.Uniform(a=0, b=0.35)  # Raio entre 0 e 0.35 cm
    length_points = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 
                    17, 18, 19, 20, 21, 22, 23.46]  # Pontos de extensão em z
    prob_length = [0, 1324, 1088, 1137, 1226, 1304, 1357, 1397, 1483, 1551, 1653, 
                1728, 1810, 1897, 2002, 2116, 2219, 2306, 2414, 2463, 2476, 
                2813, 2898, 3310]  # Distribuição ao longo de z (normalizar)

    # Normalizando a distribuição probabilística em z
    total_prob = sum(prob_length)
    prob_length = [p / total_prob for p in prob_length]

    # Distribuição da extensão ao longo de z com probabilidades normalizadas
    length_dist = openmc.stats.Discrete(length_points, prob_length)

    # Definindo uma distribuição espacial cilíndrica
    space_dist = openmc.stats.CylindricalIndependent(
        r=radius_dist,
        phi=openmc.stats.Uniform(0, 2 * 3.141592653589793),  # Ângulo uniforme ao longo de 360°
        z=length_dist,
        origin=(0, -13.34, 0)  # Origem centralizada no ponto definido
    )

    # Criando a fonte com parâmetros definidos
    source = openmc.IndependentSource(
        space=space_dist,
        angle=openmc.stats.Isotropic(),  # Ângulo isotrópico
        energy=energy_dist,              # Espectro de energia para Co-60
        strength=3.7e7,                   # Intensidade da fonte (1 mCi ou 0,7mCi?)
        particle='photon'
    )


    # MESH PRA ATIVIDADE DA FONTE

    # OUTRO PRA ATIVIDADE NO DETECTOR ?

    filtro_energia_exemplo = openmc.EnergyFilter([1,2])
    particle_foton = openmc.ParticleFilter(bins='photon')

    tally_flux = openmc.Tally(name='Fluxo de fótons chegando ao cristal')
    detector_filter = openmc.CellFilter(detector_cell)
    tally_flux.filters.append(particle_foton)
    tally_flux.filters.append(detector_filter)
    tally_flux.scores.append('flux')

    tallies = openmc.Tallies([tally_flux])
    tallies.export_to_xml()







    # ======================
    # Configurações
    # ======================

    settings = openmc.Settings()
    settings.output = {'tallies': False}
    settings.source = source
    settings.batches = 100  # Número de batches para simulação
    settings.particles = 10000
    settings.photon_transport=True
    settings.run_mode='fixed source'
    settings.export_to_xml()





    # ======================
    # Rodando openmc
    # ======================
    openmc.run()





    # ======================
    # statepoints
    # ======================


    sp = openmc.StatePoint(f"statepoint.{settings.batches}.h5")
    
    flux = sp.get_tally(scores=['flux'], name='Fluxo de fótons chegando ao cristal')
    flux_mean = flux.mean[0][0][0]
    flux_std_dev = flux.std_dev[0][0][0]
    
    UPPER_TARUGO_lista.append(UPPER_TARUGO)
    lista_fluxos.append(flux_mean)
    lista_std_dev.append(flux_std_dev)
    print(f'Fluxo: {flux_mean:.2e} ± {flux_std_dev:.2e}')


    #Fim do while tem que incrementar:
    UPPER_TARUGO += UPPER_TARUGO_INCREMENTO




print("\nResultados finais:")
for i, (flux, std) in enumerate(zip(lista_fluxos, lista_std_dev)):
    print(f"Iteração {i+1}: {flux:.2e} ± {std:.2e}")



    # ======================
    # MatPlotLib
    # ======================


# PLT styles

# ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 
# 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 
# 'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 
# 'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']

# Colors

# xkcd color survey, prefixed with 'xkcd:' (e.g., 'xkcd:sky blue'; case insensitive) https://xkcd.com/color/rgb/
# Tableau Colors from the 'T10' categorical palette:
# {'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'}

plt.style.use("seaborn-v0_8-paper")

# gráfico fluxo por altura do tarugo
plt.plot(UPPER_TARUGO_lista, lista_fluxos, marker='o', color='xkcd:dark pink', linestyle='-', linewidth=1)
plt.xlabel('Altura do Tarugo (cm)',fontsize=20)
plt.ylabel('Fluxo de Fótons no Cristal (cm²/s)', fontsize=20)
plt.title('Fluxo de Fótons no Cristal vs Altura do Tarugo', fontsize=24)

#Gridlines
plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.2, color='gray')
plt.grid(True, which='both', axis='x', linestyle='--', linewidth=0.2, color='gray')
plt.tick_params(axis='both', which='major', labelsize=16)

#plt.axhline(y=lista_std_dev, color='r', linestyle='--', label='Desvio Padrão Médio')
plt.legend(fontsize=22)

plt.tight_layout()
plt.show()
    

