# gráficos

import matplotlib.pyplot as plt
import numpy as np

##### PARADO ######
# gráfico variando detector
# caso tarugo 2 (10 x 15.81 x 15.81)
# todos os valores são 10⁴ com incerteza da ordem de 10²
d_carvao=[5.213, 5.113, 4.986, 4.890, 4.828, 4.778, 4.747, 4.827]
d_minerio=[3.812, 3.722, 3.642, 3.578, 3.547, 3.542, 3.541, 3.586]
d_casos=[1, 2, 3, 4, 5, 6, 7, 8]


plt.errorbar(
    d_casos, d_carvao, fmt='o-', color='grey',
    ecolor='slategray', capsize=5, linewidth=2, markersize=4,
    label='(Flux cm²/s coal')
plt.errorbar(
    d_casos, d_minerio, fmt='o-', color='brown',
    ecolor='slategray', capsize=5, linewidth=2, markersize=4,
    label='(Flux cm²/s iron ore')

plt.ylabel('Flux 10⁴ cm²/s')
plt.xlabel('Casos do Detector')
plt.title('Fluxo de Fótons no Detector por Distância do Tarugo')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.show()



# gráfico variando tarugo
# todos os valores são 10⁴ com incerteza da ordem de 10²
t_minerio=[3.224, 3.281, 3.405, 3.546, 3.708, 3.810, 3.869, 3.919, 3.944, 3.918, 3.839, 3.743, 3.644]
t_casos=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ,13]

plt.errorbar(
    t_casos, t_minerio, fmt='o-', color='grey',
    ecolor='slategray', capsize=5, linewidth=2, markersize=4,
    label='(Flux cm²/s iron ore')

plt.ylabel('Flux 10⁴ cm²/s')
plt.xlabel('Casos do tarugo')
plt.title('Fluxo de Fótons no Detector por Distância do Tarugo')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.show()




##### ANDANDO ######
# caso tarugo 2 (10 x 15.81 x 15.81)
a_carvao=[np.float64(63963.9378347633), np.float64(64069.83739058237), np.float64(64187.1679473196), np.float64(64346.38857972043), np.float64(64569.39754277075), np.float64(64697.604565505404), np.float64(64757.300291091735), np.float64(64782.50415319557), np.float64(65085.90445445213), np.float64(65301.50506854968), np.float64(65325.56246841409), np.float64(64065.24069465291), np.float64(60473.52358103477), np.float64(56000.167879140965), np.float64(52542.69455048575), np.float64(51349.09887642564), np.float64(51446.66297457271), np.float64(51574.81217181554), np.float64(51806.07688117758), np.float64(51880.01834332118), np.float64(52001.96740943693), np.float64(52085.713882750126), np.float64(52134.537359577065), np.float64(52160.98010869395), np.float64(52167.16834144953), np.float64(52134.296871457875), np.float64(52173.408070988546), np.float64(52136.57112481557), np.float64(52151.445001413354), np.float64(52153.0372687785), np.float64(52157.630815463795), np.float64(52055.341817200555), np.float64(51941.99107458285), np.float64(51986.21642931623), np.float64(52120.85107831837), np.float64(52052.929907088765), np.float64(53201.90888394795), np.float64(56438.57299836309), np.float64(60476.85110747846), np.float64(63190.987551692975), np.float64(64612.111657534755), np.float64(64539.036081072605), np.float64(64536.11392881605), np.float64(64592.107696011866), np.float64(64465.859325580495), np.float64(64381.24781401935), np.float64(64313.16692782343), np.float64(64219.03209310525), np.float64(64176.778408366976), np.float64(64117.70646191924)]

a_minerio=[np.float64(64392.46929038795), np.float64(64407.51586227142), np.float64(64507.09275586943), np.float64(64714.6349967309), np.float64(64793.93763125465), np.float64(64824.52251986371), np.float64(64729.41193665807), np.float64(64691.98766996938), np.float64(64879.06728261367), np.float64(64895.774493576355), np.float64(64785.19244073457), np.float64(60982.236184219895), np.float64(53965.54729172803), np.float64(46094.84589456683), np.float64(39261.31003597884), np.float64(37587.53603386349), np.float64(37611.95447341098), np.float64(37730.00961373275), np.float64(37876.4449360183), np.float64(37914.88729972506), np.float64(37999.37353981222), np.float64(38077.28571032494), np.float64(38107.83469770295), np.float64(38112.627390363894), np.float64(38114.10805771437), np.float64(38116.67870927944), np.float64(38160.83598387009), np.float64(38186.84467269739), np.float64(38209.08944023454), np.float64(38132.6033311706), np.float64(38110.377738745), np.float64(38039.950129240744), np.float64(38010.76582948086), np.float64(38046.41930646902), np.float64(38030.09040087602), np.float64(38144.462448685685), np.float64(40000.26028277186), np.float64(46549.250967000575), np.float64(54047.67957068375), np.float64(60175.19438859079), np.float64(63938.56267269155), np.float64(64042.00665518285), np.float64(64284.53502631579), np.float64(64567.072659503894), np.float64(64524.56259031304), np.float64(64509.22941878231), np.float64(64481.60312501345), np.float64(64553.58644503599), np.float64(64390.32597344651), np.float64(64337.3301286092)]

distancias = np.arange(15, -5.0 , -0.4)

plt.errorbar(
    distancias, a_carvao, fmt='o-', color='grey',
    ecolor='slategray', capsize=5, linewidth=2, markersize=4,
    label='(Flux cm²/s coal')
plt.errorbar(
    distancias, a_minerio, fmt='o-', color='brown',
    ecolor='slategray', capsize=5, linewidth=2, markersize=4,
    label='(Flux cm²/s iron ore')

plt.ylabel('Flux cm²/s')
plt.xlabel('Distance')
plt.title('Fluxo de Fótons no Detector por Distância do Tarugo')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.show()
