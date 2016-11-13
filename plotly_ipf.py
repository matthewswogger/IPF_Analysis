import plotly.plotly as py
from plotly.graph_objs import *
import sqlite3
import pandas as pd
import numpy as np


conn = sqlite3.connect('IPF_data.db')
c = conn.cursor()

df = pd.read_sql('''SELECT *
                    FROM classic''', conn)
conn.close()
#################################################
mens, womens = {},{}
for squat in sorted(df.squat_class.unique()):
    x = df[df.squat_class == squat]
    men = x[x.sex == 'M']
    women = x[x.sex == 'W']
    mens[squat] = [men.best_squat.mean(), men.best_bench.mean(), men.best_deadlift.mean()]
    womens[squat] = [women.best_squat.mean(), women.best_bench.mean(), women.best_deadlift.mean()]

df_men = df[df.sex == 'M']
mens_array = np.array([mens[squat] for squat in df_men.squat_class])

df_women = df[df.sex == 'W']
womens_array = np.array([womens[squat] for squat in df_women.squat_class])

df_men.loc[:,('average_squat')] = mens_array[:,0]
df_men.loc[:,('average_bench')] = mens_array[:,1]
df_men.loc[:,('average_deadlift')] = mens_array[:,2]

df_women.loc[:,('average_squat')] = womens_array[:,0]
df_women.loc[:,('average_bench')] = womens_array[:,1]
df_women.loc[:,('average_deadlift')] = womens_array[:,2]

df = pd.concat([df_men,df_women])
#########################################################

# men and women best squats and benches
men_best_squat_bench = Scatter(x=df.best_squat[df.sex == 'M'],
                               y=df.best_bench[df.sex == 'M'],
                               mode = 'markers',
                               marker = dict(size = 10,color = 'rgba(152, 0, 0, .8)',
                                             line = dict(width = 2,color = 'rgb(0, 0, 0)')),
                               name='Men')

women_best_squat_bench = Scatter(x=df.best_squat[df.sex == 'W'],
                                 y=df.best_bench[df.sex == 'W'],
                                 mode = 'markers',
                                 marker = dict(size = 10,color = 'rgba(255, 182, 193, .9)',
                                               line = dict(width = 2)),
                                 name='Women',
                                 visible=False)

# men and women best deadlifts and benches
men_best_dead_bench = Scatter(x=df.best_deadlift[df.sex == 'M'],
                              y=df.best_bench[df.sex == 'M'],
                              mode = 'markers',
                              marker = dict(size = 10,color = 'rgba(152, 0, 0, .8)',
                                            line = dict(width = 2,color = 'rgb(0, 0, 0)')),
                              name='Men',
                              visible=False)

women_best_dead_bench = Scatter(x=df.best_deadlift[df.sex == 'W'],
                                y=df.best_bench[df.sex == 'W'],
                                mode = 'markers',
                                marker = dict(size = 10,color = 'rgba(255, 182, 193, .9)',
                                              line = dict(width = 2)),
                                name='Women',
                                visible=False)

# men and women squat class and bench squat ratio
men_squat_class_ratio = Scatter(x=df.squat_class[df.sex == 'M'],
                                y=df.bench_squat_ratio[df.sex == 'M'],
                                mode = 'markers',
                                marker = dict(size = 10,color = 'rgba(152, 0, 0, .8)',
                                              line = dict(width = 2,color = 'rgb(0, 0, 0)')),
                                name='Men',
                                visible=False)

women_squat_class_ratio = Scatter(x=df.squat_class[df.sex == 'W'],
                                  y=df.bench_squat_ratio[df.sex == 'W'],
                                  mode = 'markers',
                                  marker = dict(size = 10,color = 'rgba(255, 182, 193, .9)',
                                                line = dict(width = 2)),
                                  name='Women',
                                  visible=False)

# men and women average squat and bench by squat class
men_average_squat_bench = Scatter(x=df.average_squat[df.sex == 'M'],
                                  y=df.average_bench[df.sex == 'M'],
                                  mode = 'markers',
                                  marker = dict(size = 10,color = 'rgba(152, 0, 0, .8)',
                                                line = dict(width = 2,color = 'rgb(0, 0, 0)')),
                                  name='Men',
                                  visible=False)

women_average_squat_bench = Scatter(x=df.average_squat[df.sex == 'W'],
                                    y=df.average_bench[df.sex == 'W'],
                                    mode = 'markers',
                                    marker = dict(size = 10,color = 'rgba(255, 182, 193, .9)',
                                                  line = dict(width = 2)),
                                    name='Women',
                                    visible=False)

# men and women average deadlift and bench by squat class
men_average_deadlift_bench = Scatter(x=df.average_deadlift[df.sex == 'M'],
                                     y=df.average_bench[df.sex == 'M'],
                                     mode = 'markers',
                                     marker = dict(size = 10,color = 'rgba(152, 0, 0, .8)',
                                                   line = dict(width = 2,color = 'rgb(0, 0, 0)')),
                                     name='Men',
                                     visible=False)

women_average_deadlift_bench = Scatter(x=df.average_deadlift[df.sex == 'W'],
                                       y=df.average_bench[df.sex == 'W'],
                                       mode = 'markers',
                                       marker = dict(size = 10,color = 'rgba(255, 182, 193, .9)',
                                                     line = dict(width = 2)),
                                       name='Women',
                                       visible=False)

####################################################
layout = Layout(title='IPF Data Analysis',
                xaxis={'title': 'Squat or Deadlift'},
                yaxis={'title': 'Bench or Bench/Squat Ratio'},
                updatemenus=list([dict(yanchor='top',
                                       buttons=list([# best bench on yaxis, best squat on xaxis
                                                     dict(args=['visible', [True,False,False,False,
                                                                            False,False,False,False,
                                                                            False,False]],
                                                          label='Men BestSquat BestBench',
                                                          method='restyle'),
                                                     dict(args=['visible', [True,True,False,False,
                                                                            False,False,False,False,
                                                                            False,False]],
                                                          label='Men Women BestSquat BestBench',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,True,False,False,
                                                                            False,False,False,False,
                                                                            False,False]],
                                                          label='Women BestSquat BestBench',
                                                          method='restyle'),
                                                     # best bench on yaxis, best deadlift on xaxis
                                                     dict(args=['visible', [False,False,True,False,
                                                                            False,False,False,False,
                                                                            False,False]],
                                                          label='Men BestDead BestBench',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,False,True,True,
                                                                            False,False,False,False,
                                                                            False,False]],
                                                          label='Men Women BestDead BestBench',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,False,False,True,
                                                                            False,False,False,False,
                                                                            False,False]],
                                                          label='Women BestDead BestBench',
                                                          method='restyle'),
                                                     # squat class on xaxis, bench/squat ratio on yaxis
                                                     dict(args=['visible', [False,False,False,False,
                                                                            True,False,False,False,
                                                                            False,False]],
                                                          label='Men SquatClass Bench/Squat',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,False,False,False,
                                                                            True,True,False,False,
                                                                            False,False]],
                                                          label='Men Women SquatClass Bench/Squat',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,False,False,False,
                                                                            False,True,False,False,
                                                                            False,False]],
                                                          label='Women SquatClass Bench/Squat',
                                                          method='restyle'),
                                                     # average squat on xaxis, average bench on yaxis
                                                     dict(args=['visible', [False,False,False,False,
                                                                            False,False,True,False,
                                                                            False,False]],
                                                          label='Men Average Bench Squat',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,False,False,False,
                                                                            False,False,True,True,
                                                                            False,False]],
                                                          label='Men Women Average Bench Squat',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,False,False,False,
                                                                            False,False,False,True,
                                                                            False,False]],
                                                          label='Women Average Bench Squat',
                                                          method='restyle'),
                                                     # average deadlift on xaxis, average bench on yaxis
                                                     dict(args=['visible', [False,False,False,False,
                                                                            False,False,False,False,
                                                                            True,False]],
                                                          label='Men Average Bench Deadlift',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,False,False,False,
                                                                            False,False,False,False,
                                                                            True,True]],
                                                          label='Men Women Average Bench Deadlift',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,False,False,False,
                                                                            False,False,False,False,
                                                                            False,True]],
                                                          label='Women Average Bench Deadlift',
                                                          method='restyle')
                                                    ])
                                                    )]),)
##########################################################
data = Data([men_best_squat_bench,
             women_best_squat_bench,
             men_best_dead_bench,
             women_best_dead_bench,
             men_squat_class_ratio,
             women_squat_class_ratio,
             men_average_squat_bench,
             women_average_squat_bench,
             men_average_deadlift_bench,
             women_average_deadlift_bench])

fig = Figure(data=data, layout=layout)
py.plot(fig, filename = 'basic-test')
