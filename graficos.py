# gráficos

import matplotlib.pyplot as plt
import numpy as np




plt.rcParams.update({'font.size': 14}) 


# # # gráfico variando tarugo FIG 1
# # todos os valores são 10⁴ com incerteza da ordem de 10² com 200000 partículas
t_minerio=[3.224, 3.281, 3.405, 3.546, 3.708, 3.810, 3.869, 3.919, 3.944, 3.918, 3.839, 3.743, 3.644]
t_casos=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ,13]

plt.errorbar(
    t_casos, t_minerio, fmt='o-', color='grey',
    ecolor='slategray', capsize=5, linewidth=2, markersize=4,
    label='Iron ore')

plt.ylabel('Gamma Counts x 10⁴')
plt.xlabel('Case # ')
plt.title('Counts x Bulk Material Geometry')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.show()



# # # ##### ANDANDO FIG 2 ######

# carvao = [np.float64(65521.77212300241), np.float64(65644.67205034672), np.float64(65736.10884769316), np.float64(65763.41701488028), np.float64(65798.48856780012), np.float64(65842.36408071405), np.float64(65932.71468866697), np.float64(65998.41508300342), np.float64(66036.94994251286), np.float64(66058.5008652653), np.float64(66028.22936353172), np.float64(66113.63976331272), np.float64(66206.09675909847), np.float64(66161.66957442503), np.float64(66220.3027792265), np.float64(66265.31279282708), np.float64(66246.40468910718), np.float64(65594.12795254259), np.float64(64026.644937374025), np.float64(61703.59392803931), np.float64(59031.95360125874), np.float64(56533.40495459955), np.float64(54183.98998744993), np.float64(52663.975799172345), np.float64(52283.162731102944), np.float64(52316.498977242525), np.float64(52467.29338270618), np.float64(52512.91070492226), np.float64(52662.339797153625), np.float64(52632.167905320384), np.float64(52668.37774457633), np.float64(52701.78104204815), np.float64(52755.64641293291), np.float64(52797.39609001872), np.float64(52846.99765253632), np.float64(52887.51485598436), np.float64(52893.94002170711), np.float64(52922.35980145087), np.float64(52923.67761689416), np.float64(52916.090951609694), np.float64(52936.788747625265), np.float64(52929.233148629304), np.float64(52941.40757006715), np.float64(52942.637428618844), np.float64(52955.69965644906), np.float64(52939.38383586904), np.float64(52922.477210068566), np.float64(52897.53156404323), np.float64(52890.52482585996), np.float64(52848.89740639527), np.float64(52787.825063235), np.float64(52751.377882228226), np.float64(52715.52407844242), np.float64(52682.975474005056), np.float64(52611.1827545046), np.float64(52602.27598948224), np.float64(52587.11075336232), np.float64(53048.82009735941), np.float64(54425.2372055732), np.float64(56656.963495695156), np.float64(59320.66338940356), np.float64(61854.07079532517), np.float64(64090.81138230325), np.float64(65581.97263662063), np.float64(66191.61118912393), np.float64(66230.81697322159), np.float64(66234.7281410398), np.float64(66166.53174272514), np.float64(66073.66150448404), np.float64(66142.69638142483), np.float64(66077.9007396787), np.float64(66031.50472153029), np.float64(65972.87489091455), np.float64(65894.79897152472), np.float64(65854.85767473927), np.float64(65808.33207649154), np.float64(65749.53667071143), np.float64(65709.01132528544), np.float64(65628.72415268206), np.float64(65622.45845763787), np.float64(65559.95659541724)]
# ore = [np.float64(65872.61720660937), np.float64(65900.41785485782), np.float64(65931.76656292097), np.float64(65943.8900439691), np.float64(65983.56868919136), np.float64(66024.92244076253), np.float64(66013.2105188271), np.float64(65990.99778088363), np.float64(65980.33389666572), np.float64(65986.66085010445), np.float64(65953.77992153021), np.float64(65913.18369790494), np.float64(65893.12409268125), np.float64(65836.86203619007), np.float64(65775.01015426494), np.float64(65750.0439284544), np.float64(65502.40384693019), np.float64(63705.73380193617), np.float64(60242.787311435546), np.float64(55925.05421813976), np.float64(51062.81968074675), np.float64(45912.55856288287), np.float64(41095.97441436089), np.float64(38684.10189628873), np.float64(38139.28214198628), np.float64(38192.89513515979), np.float64(38270.814883610474), np.float64(38301.91761461641), np.float64(38418.97230669396), np.float64(38393.20738747851), np.float64(38371.596723273804), np.float64(38398.40154346765), np.float64(38417.87388086555), np.float64(38448.58313633408), np.float64(38467.45830770135), np.float64(38460.00143417986), np.float64(38486.794234340596), np.float64(38522.73740391492), np.float64(38511.27905480999), np.float64(38481.21997835436), np.float64(38505.742754183586), np.float64(38507.95733811228), np.float64(38508.57996398805), np.float64(38502.24537721572), np.float64(38512.049559816674), np.float64(38500.596682446616), np.float64(38493.8547981269), np.float64(38470.46316376373), np.float64(38467.77262099173), np.float64(38420.21286293814), np.float64(38398.1618758553), np.float64(38379.19457324781), np.float64(38348.505456921266), np.float64(38339.75626622924), np.float64(38276.03799958134), np.float64(38280.80493209085), np.float64(38347.08646541268), np.float64(38910.29709887207), np.float64(41440.86713535126), np.float64(45864.960907684435), np.float64(51144.707607870994), np.float64(56002.245674506325), np.float64(60263.87464317683), np.float64(63581.4494811069), np.float64(65395.458294272954), np.float64(65614.93471201627), np.float64(65700.48883439186), np.float64(65796.494376901), np.float64(65819.24997826871), np.float64(65921.63894396693), np.float64(65889.45816097732), np.float64(65881.7620716088), np.float64(65863.44541175416), np.float64(65833.48428398249), np.float64(65843.12440561132), np.float64(65850.51814051095), np.float64(65878.27177135335), np.float64(65927.44124180284), np.float64(65883.1078021706), np.float64(65819.5251887218), np.float64(65781.42721289322)]
# x = np.arange(15, -5.25, -0.25)

# plt.errorbar(
#     x, carvao, fmt='o-', color='grey',
#     ecolor='slategray', capsize=5, linewidth=2, markersize=4,
#     label='Coal')
# plt.errorbar(
#     x, ore, fmt='o-', color='brown',
#     ecolor='slategray', capsize=5, linewidth=2, markersize=4,
#     label='Ion ore')

# plt.ylabel('Displacement')
# plt.xlabel('Displacement')
# plt.title('Counts x Bulk Material Position')
# plt.legend()
# plt.grid(True, alpha=0.3)
# plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
# plt.show()

# #### PARADO FIG 3######
# # gráfico variando detector
# # caso tarugo 2 (10 x 15.81 x 15.81) com 200000 partículas
# # todos os valores são 10⁴ com incerteza da ordem de 10²
# d_carvao=[4.778,4.828,4.890,4.986,5.113,5.213,5.323,5.424,5.538,5.615,5.701]
# d_minerio=[3.542,3.547,3.578,3.642,3.722,3.812,3.895,3.971,4.044,4.104,4.170]

# d_casos=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# plt.errorbar(
#     d_casos, d_carvao, fmt='o-', color='grey',
#     ecolor='slategray', capsize=5, linewidth=2, markersize=4,
#     label='Coal')
# plt.errorbar(
#     d_casos, d_minerio, fmt='o-', color='brown',
#     ecolor='slategray', capsize=5, linewidth=2, markersize=4,
#     label='Iron ore')

# plt.ylabel('Counts x 10⁴')
# plt.xlabel('Case # ')
# plt.title('Counts x Crystal Dimensions Variation')
# plt.legend()
# plt.grid(True, alpha=0.3)
# plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
# plt.show()
