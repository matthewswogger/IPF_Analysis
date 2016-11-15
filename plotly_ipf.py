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
# a few variables assigned for readability and ease of changing them
dot_size = 8
line_width = 1
line_color = 'rgb(0, 0, 0)'
men_color = 'rgba(152, 0, 0, .8)'
women_color = 'rgba(25, 219, 128, .9)'

# men and women best squats and benches
men_best_squat_bench = Scatter(x=df.best_squat[df.sex == 'M'],
                               y=df.best_bench[df.sex == 'M'],
                               mode = 'markers',
                               marker = dict(size=dot_size,color=men_color,
                                             line=dict(width=line_width,color=line_color)),
                               name = 'Men')

women_best_squat_bench = Scatter(x=df.best_squat[df.sex == 'W'],
                                 y=df.best_bench[df.sex == 'W'],
                                 mode = 'markers',
                                 marker = dict(size=dot_size,color=women_color,
                                               line=dict(width=line_width)),
                                 name = 'Women')

# men and women best deadlifts and benches
men_best_dead_bench = Scatter(x=df.best_deadlift[df.sex == 'M'],
                              y=df.best_bench[df.sex == 'M'],
                              mode = 'markers',
                              marker = dict(size=dot_size,color=men_color,
                                            line=dict(width=line_width,color=line_color)),
                              name = 'Men',
                              visible = False)

women_best_dead_bench = Scatter(x=df.best_deadlift[df.sex == 'W'],
                                y=df.best_bench[df.sex == 'W'],
                                mode = 'markers',
                                marker = dict(size=dot_size,color=women_color,
                                              line=dict(width=line_width)),
                                name = 'Women',
                                visible = False)

# men and women squat class and bench squat ratio
men_squat_class_ratio = Scatter(x=df.squat_class[df.sex == 'M'],
                                y=df.bench_squat_ratio[df.sex == 'M'],
                                mode = 'markers',
                                marker = dict(size=dot_size,color=men_color,
                                              line=dict(width=line_width,color=line_color)),
                                name = 'Men',
                                visible = False)

women_squat_class_ratio = Scatter(x=df.squat_class[df.sex == 'W'],
                                  y=df.bench_squat_ratio[df.sex == 'W'],
                                  mode = 'markers',
                                  marker = dict(size=dot_size,color=women_color,
                                                line=dict(width=line_width)),
                                  name = 'Women',
                                  visible = False)

# men and women average squat and bench by squat class
men_average_squat_bench = Scatter(x=df.average_squat[df.sex == 'M'],
                                  y=df.average_bench[df.sex == 'M'],
                                  mode = 'markers',
                                  marker = dict(size=dot_size,color=men_color,
                                                line=dict(width=line_width,color=line_color)),
                                  name = 'Men',
                                  visible = False)

women_average_squat_bench = Scatter(x=df.average_squat[df.sex == 'W'],
                                    y=df.average_bench[df.sex == 'W'],
                                    mode = 'markers',
                                    marker = dict(size=dot_size,color=women_color,
                                                  line=dict(width=line_width)),
                                    name = 'Women',
                                    visible = False)

# men and women average deadlift and bench by squat class
men_average_deadlift_bench = Scatter(x=df.average_deadlift[df.sex == 'M'],
                                     y=df.average_bench[df.sex == 'M'],
                                     mode = 'markers',
                                     marker = dict(size=dot_size,color=men_color,
                                                   line=dict(width=line_width,color=line_color)),
                                     name = 'Men',
                                     visible = False)

women_average_deadlift_bench = Scatter(x=df.average_deadlift[df.sex == 'W'],
                                       y=df.average_bench[df.sex == 'W'],
                                       mode = 'markers',
                                       marker = dict(size=dot_size,color=women_color,
                                                     line=dict(width=line_width)),
                                       name = 'Women',
                                       visible = False)

####################################################
layout = Layout(title='IPF Data Analysis',
                xaxis={'title': 'Squat or Deadlift'},
                yaxis={'title': 'Bench or Bench/Squat Ratio'},
                updatemenus=list([dict(yanchor='top',
                                       buttons=list([
                                                     dict(args=['visible', [True,True,False,False,
                                                                            False,False,False,False,
                                                                            False,False]],
                                                          label='X:BestSquat Y:BestBench',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,False,True,True,
                                                                            False,False,False,False,
                                                                            False,False]],
                                                          label='X:BestDead Y:BestBench',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,False,False,False,
                                                                            True,True,False,False,
                                                                            False,False]],
                                                          label='X:SquatClass Y:Bench/Squat',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,False,False,False,
                                                                            False,False,True,True,
                                                                            False,False]],
                                                          label='Average X:Squat Y:Bench',
                                                          method='restyle'),
                                                     dict(args=['visible', [False,False,False,False,
                                                                            False,False,False,False,
                                                                            True,True]],
                                                          label='Average X:Deadlift Y:Bench',
                                                          method='restyle')
                                                    ])
                                                    )]))
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
