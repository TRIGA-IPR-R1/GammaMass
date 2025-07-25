# gráficos

import matplotlib.pyplot as plt
import numpy as np

# ##### PARADO ######
# # gráfico variando detector
# # caso tarugo 2 (10 x 15.81 x 15.81) com 200000 partículas
# # todos os valores são 10⁴ com incerteza da ordem de 10²
d_carvao=[4.778,4.828,4.890,4.986,5.113,5.213,5.323,5.424,5.538,5.615,5.701]
d_minerio=[3.542,3.547,3.578,3.642,3.722,3.812,3.895,3.971,4.044,4.104,4.170]

d_casos=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


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



# # gráfico variando tarugo
# # todos os valores são 10⁴ com incerteza da ordem de 10² com 200000 partículas
# t_minerio=[3.224, 3.281, 3.405, 3.546, 3.708, 3.810, 3.869, 3.919, 3.944, 3.918, 3.839, 3.743, 3.644]
# t_casos=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ,13]

# plt.errorbar(
#     t_casos, t_minerio, fmt='o-', color='grey',
#     ecolor='slategray', capsize=5, linewidth=2, markersize=4,
#     label='(Flux cm²/s iron ore')

# plt.ylabel('Flux 10⁴ cm²/s')
# plt.xlabel('Casos do tarugo')
# plt.title('Fluxo de Fótons no Detector por Distância do Tarugo')
# plt.legend()
# plt.grid(True, alpha=0.3)
# plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
# plt.show()




# ##### ANDANDO ######
# # caso tarugo 2 (10 x 15.81 x 15.81) com 400000 partículas
# a_carvao=[np.float64(63963.9378347633), np.float64(64069.83739058237), np.float64(64187.1679473196), np.float64(64346.38857972043), np.float64(64569.39754277075), np.float64(64697.604565505404), np.float64(64757.300291091735), np.float64(64782.50415319557), np.float64(65085.90445445213), np.float64(65301.50506854968), np.float64(65325.56246841409), np.float64(64065.24069465291), np.float64(60473.52358103477), np.float64(56000.167879140965), np.float64(52542.69455048575), np.float64(51349.09887642564), np.float64(51446.66297457271), np.float64(51574.81217181554), np.float64(51806.07688117758), np.float64(51880.01834332118), np.float64(52001.96740943693), np.float64(52085.713882750126), np.float64(52134.537359577065), np.float64(52160.98010869395), np.float64(52167.16834144953), np.float64(52134.296871457875), np.float64(52173.408070988546), np.float64(52136.57112481557), np.float64(52151.445001413354), np.float64(52153.0372687785), np.float64(52157.630815463795), np.float64(52055.341817200555), np.float64(51941.99107458285), np.float64(51986.21642931623), np.float64(52120.85107831837), np.float64(52052.929907088765), np.float64(53201.90888394795), np.float64(56438.57299836309), np.float64(60476.85110747846), np.float64(63190.987551692975), np.float64(64612.111657534755), np.float64(64539.036081072605), np.float64(64536.11392881605), np.float64(64592.107696011866), np.float64(64465.859325580495), np.float64(64381.24781401935), np.float64(64313.16692782343), np.float64(64219.03209310525), np.float64(64176.778408366976), np.float64(64117.70646191924)]

# a_minerio=[np.float64(64392.46929038795), np.float64(64407.51586227142), np.float64(64507.09275586943), np.float64(64714.6349967309), np.float64(64793.93763125465), np.float64(64824.52251986371), np.float64(64729.41193665807), np.float64(64691.98766996938), np.float64(64879.06728261367), np.float64(64895.774493576355), np.float64(64785.19244073457), np.float64(60982.236184219895), np.float64(53965.54729172803), np.float64(46094.84589456683), np.float64(39261.31003597884), np.float64(37587.53603386349), np.float64(37611.95447341098), np.float64(37730.00961373275), np.float64(37876.4449360183), np.float64(37914.88729972506), np.float64(37999.37353981222), np.float64(38077.28571032494), np.float64(38107.83469770295), np.float64(38112.627390363894), np.float64(38114.10805771437), np.float64(38116.67870927944), np.float64(38160.83598387009), np.float64(38186.84467269739), np.float64(38209.08944023454), np.float64(38132.6033311706), np.float64(38110.377738745), np.float64(38039.950129240744), np.float64(38010.76582948086), np.float64(38046.41930646902), np.float64(38030.09040087602), np.float64(38144.462448685685), np.float64(40000.26028277186), np.float64(46549.250967000575), np.float64(54047.67957068375), np.float64(60175.19438859079), np.float64(63938.56267269155), np.float64(64042.00665518285), np.float64(64284.53502631579), np.float64(64567.072659503894), np.float64(64524.56259031304), np.float64(64509.22941878231), np.float64(64481.60312501345), np.float64(64553.58644503599), np.float64(64390.32597344651), np.float64(64337.3301286092)]

# distancias = np.arange(15, -5.0 , -0.4)

# plt.errorbar(
#     distancias, a_carvao, fmt='o-', color='grey',
#     ecolor='slategray', capsize=5, linewidth=2, markersize=4,
#     label='(Flux cm²/s coal')
# plt.errorbar(
#     distancias, a_minerio, fmt='o-', color='brown',
#     ecolor='slategray', capsize=5, linewidth=2, markersize=4,
#     label='(Flux cm²/s iron ore')

# plt.ylabel('Flux cm²/s')
# plt.xlabel('Distance')
# plt.title('Fluxo de Fótons no Detector por Distância do Tarugo')
# plt.legend()
# plt.grid(True, alpha=0.3)
# plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
# plt.show()






# carvao = [np.float64(65521.77212300241), np.float64(65644.67205034672), np.float64(65736.10884769316), np.float64(65763.41701488028), np.float64(65798.48856780012), np.float64(65842.36408071405), np.float64(65932.71468866697), np.float64(65998.41508300342), np.float64(66036.94994251286), np.float64(66058.5008652653), np.float64(66028.22936353172), np.float64(66113.63976331272), np.float64(66206.09675909847), np.float64(66161.66957442503), np.float64(66220.3027792265), np.float64(66265.31279282708), np.float64(66246.40468910718), np.float64(65594.12795254259), np.float64(64026.644937374025), np.float64(61703.59392803931), np.float64(59031.95360125874), np.float64(56533.40495459955), np.float64(54183.98998744993), np.float64(52663.975799172345), np.float64(52283.162731102944), np.float64(52316.498977242525), np.float64(52467.29338270618), np.float64(52512.91070492226), np.float64(52662.339797153625), np.float64(52632.167905320384), np.float64(52668.37774457633), np.float64(52701.78104204815), np.float64(52755.64641293291), np.float64(52797.39609001872), np.float64(52846.99765253632), np.float64(52887.51485598436), np.float64(52893.94002170711), np.float64(52922.35980145087), np.float64(52923.67761689416), np.float64(52916.090951609694), np.float64(52936.788747625265), np.float64(52929.233148629304), np.float64(52941.40757006715), np.float64(52942.637428618844), np.float64(52955.69965644906), np.float64(52939.38383586904), np.float64(52922.477210068566), np.float64(52897.53156404323), np.float64(52890.52482585996), np.float64(52848.89740639527), np.float64(52787.825063235), np.float64(52751.377882228226), np.float64(52715.52407844242), np.float64(52682.975474005056), np.float64(52611.1827545046), np.float64(52602.27598948224), np.float64(52587.11075336232), np.float64(53048.82009735941), np.float64(54425.2372055732), np.float64(56656.963495695156), np.float64(59320.66338940356), np.float64(61854.07079532517), np.float64(64090.81138230325), np.float64(65581.97263662063), np.float64(66191.61118912393), np.float64(66230.81697322159), np.float64(66234.7281410398), np.float64(66166.53174272514), np.float64(66073.66150448404), np.float64(66142.69638142483), np.float64(66077.9007396787), np.float64(66031.50472153029), np.float64(65972.87489091455), np.float64(65894.79897152472), np.float64(65854.85767473927), np.float64(65808.33207649154), np.float64(65749.53667071143), np.float64(65709.01132528544), np.float64(65628.72415268206), np.float64(65622.45845763787), np.float64(65559.95659541724)]

# ore = [np.float64(65872.61720660937), np.float64(65900.41785485782), np.float64(65931.76656292097), np.float64(65943.8900439691), np.float64(65983.56868919136), np.float64(66024.92244076253), np.float64(66013.2105188271), np.float64(65990.99778088363), np.float64(65980.33389666572), np.float64(65986.66085010445), np.float64(65953.77992153021), np.float64(65913.18369790494), np.float64(65893.12409268125), np.float64(65836.86203619007), np.float64(65775.01015426494), np.float64(65750.0439284544), np.float64(65502.40384693019), np.float64(63705.73380193617), np.float64(60242.787311435546), np.float64(55925.05421813976), np.float64(51062.81968074675), np.float64(45912.55856288287), np.float64(41095.97441436089), np.float64(38684.10189628873), np.float64(38139.28214198628), np.float64(38192.89513515979), np.float64(38270.814883610474), np.float64(38301.91761461641), np.float64(38418.97230669396), np.float64(38393.20738747851), np.float64(38371.596723273804), np.float64(38398.40154346765), np.float64(38417.87388086555), np.float64(38448.58313633408), np.float64(38467.45830770135), np.float64(38460.00143417986), np.float64(38486.794234340596), np.float64(38522.73740391492), np.float64(38511.27905480999), np.float64(38481.21997835436), np.float64(38505.742754183586), np.float64(38507.95733811228), np.float64(38508.57996398805), np.float64(38502.24537721572), np.float64(38512.049559816674), np.float64(38500.596682446616), np.float64(38493.8547981269), np.float64(38470.46316376373), np.float64(38467.77262099173), np.float64(38420.21286293814), np.float64(38398.1618758553), np.float64(38379.19457324781), np.float64(38348.505456921266), np.float64(38339.75626622924), np.float64(38276.03799958134), np.float64(38280.80493209085), np.float64(38347.08646541268), np.float64(38910.29709887207), np.float64(41440.86713535126), np.float64(45864.960907684435), np.float64(51144.707607870994), np.float64(56002.245674506325), np.float64(60263.87464317683), np.float64(63581.4494811069), np.float64(65395.458294272954), np.float64(65614.93471201627), np.float64(65700.48883439186), np.float64(65796.494376901), np.float64(65819.24997826871), np.float64(65921.63894396693), np.float64(65889.45816097732), np.float64(65881.7620716088), np.float64(65863.44541175416), np.float64(65833.48428398249), np.float64(65843.12440561132), np.float64(65850.51814051095), np.float64(65878.27177135335), np.float64(65927.44124180284), np.float64(65883.1078021706), np.float64(65819.5251887218), np.float64(65781.42721289322)]

# x = np.arange(15, -5.25, -0.25)

# plt.errorbar(
#     x, carvao, fmt='o-', color='grey',
#     ecolor='slategray', capsize=5, linewidth=2, markersize=4,
#     label='(Flux cm²/s coal')
# plt.errorbar(
#     x, ore, fmt='o-', color='brown',
#     ecolor='slategray', capsize=5, linewidth=2, markersize=4,
#     label='(Flux cm²/s iron ore')

# plt.ylabel('Flux cm²/s')
# plt.xlabel('Distance')
# plt.title('Fluxo de Fótons no Detector por Distância do Tarugo')
# plt.legend()
# plt.grid(True, alpha=0.3)
# plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
# plt.show()