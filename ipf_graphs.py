import pandas as pd
import numpy as np
import sqlite3

from bokeh.layouts import row, widgetbox
from bokeh.models import Select, HoverTool
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure, ColumnDataSource

SIZES = list(range(6, 22, 3))
COLORS = Spectral5

##############################################
conn = sqlite3.connect('IPF_data.db')
c = conn.cursor()

df = pd.read_sql('''SELECT *
                    FROM classic''', conn)
conn.close()
###############################################
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
#######################################

columns = sorted(df.columns)
discrete = [x for x in columns if df[x].dtype == object]
continuous = [x for x in columns if x not in discrete]
quantileable = [x for x in continuous if len(df[x].unique()) > 20]
quantileable.append('sex')


def create_figure():
    xs = df[x.value].values
    ys = df[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    kw = dict()
    if x.value in discrete:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s vs %s" % (x_title, y_title)

    hover = HoverTool(tooltips=[("Lifter", "@lifter"),("Comp year", "@year"),
                                ("Team", "@team"),("Body weight", "@body_weight")])
    p = figure(plot_height=700, plot_width=1000, tools='pan,box_zoom,reset,save', **kw)
    p.add_tools(hover)

    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != 'None':
        if size.value == 'sex':
            sz = [15 if person =='M' else 6 for person in df[size.value].values]
        else:
            groups = pd.qcut(df[size.value].values, len(SIZES))
            sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != 'None':
        if color.value == 'sex':
            c = ['#2b83ba' if person =='M' else '#d7191c' for person in df[color.value].values]
        else:
            groups = pd.qcut(df[color.value].values, len(COLORS))
            c = [COLORS[xx] for xx in groups.codes]

    source = ColumnDataSource(df[['lifter','year','team','body_weight']])
    Legend = '''Color: {} Size : {}'''.format(color.value,size.value)
    p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6,
                                    hover_color='white', hover_alpha=0.5, source=source,
                                    legend=Legend)
    p.legend.location = "top_left"

    return p


def update(attr, old, new):
    layout.children[1] = create_figure()


x = Select(title='X-Axis', value='best_squat', options=columns)
x.on_change('value', update)

y = Select(title='Y-Axis', value='best_bench', options=columns)
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None'] + quantileable)
size.on_change('value', update)

color = Select(title='Color', value='None', options=['None'] + quantileable)
color.on_change('value', update)

controls = widgetbox([x, y, color, size], width=150)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "IPF Analysis"

from bokeh.resources import CDN
from bokeh.embed import file_html

html = file_html(layout, CDN, "my plot")
print '#'*100
print html
###################################################################################
# from jinja2 import Template
# from bokeh.resources import JSResources, CDN
# from bokeh.embed import file_html
# from bokeh.util.browser import view

# # Open our custom template
# with open('index.html', 'r') as f:
#     template = Template(f.read())
#
# # Use inline resources, render the html and open
# js_resources = JSResources(mode='inline')
#
# title = "IPF Analysis"
# html = file_html(layout, resources=CDN, title=title, template=template)
#
# output_file = 'IPF.html'
# with open(output_file, 'w') as f:
#     f.write(html)
# view(output_file)



# from bokeh.io import output_file, save

# html = output_file('IPF', title='IPF Men Women Analysis', autosave=False, mode='inline', root_dir=None)
# save(obj=layout,filename='IPF.html',title='IPF Men Women Analysis')
