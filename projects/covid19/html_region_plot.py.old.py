import plotly
import plotly.graph_objs as go


x = [1, 2, 3]
y = [1000, 10000, 100000]
y2 = [5000, 10000, 90000]

trace1 = go.Bar(x=x, y=y, name='trace1')
trace2 = go.Bar(x=x, y=y2, name='trace2', visible=False)


data = [trace1, trace2]

updatemenus = list([
    dict(active=1,
         buttons=list([
            dict(label='Log Scale',
                 method='update',
                 args=[{'yaxis': {'type': 'log'}}]),
            dict(label='Linear Scale',
                 method='update',
                 args=[{'yaxis': {'type': 'linear'}}])
            ]),
        )
    ])

layout = dict(updatemenus=updatemenus, title='Linear scale')
fig = go.Figure(data=data, layout=layout)

plotly.offline.iplot(fig)