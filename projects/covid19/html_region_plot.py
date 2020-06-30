import argparse
import os
import datetime as dt

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import yaml

def get_population(region):
    with open('population.json') as json_file:
        for line in yaml.safe_load(json_file):
            if line['region'].lower() == region:
                return int(line['population'])

def covid19_html_plot(dirpath, region):
	dirpath = dirpath + os.path.sep + region

	# dates
	dates_str = pd.read_csv(dirpath + os.path.sep + "dates.csv", names=["dates"])["dates"].values.tolist()
	dates = [dt.datetime.strptime(d, "%Y-%m-%d").date() for d in dates_str]
	#print(type(dates))
	#c = np.linspace(0, dates.shape[0], dates.shape[0]+1)
	
	# y obs
	y_obs = np.genfromtxt(dirpath + os.path.sep + "y_obs.csv", delimiter=',')
	#df.insert(loc=6, column="y_obs", value=y_obs)

	# y sims
	y_sims = np.genfromtxt(dirpath + os.path.sep + "y_sims.csv", delimiter=',')
	y_mean =  np.mean(y_sims, axis=0)
	y_lower = np.percentile(y_sims, q=2.5, axis=0)
	y_upper = np.percentile(y_sims, q=97.5, axis=0)
	
	trace1 = go.Scatter(x=dates, y=y_upper.astype(int), name = '95% confidence interval', fillcolor='rgba(0,100,80,0.2)', line_color='rgba(255,255,255,0)', showlegend=False)
	trace2 = go.Scatter(x=dates, y=y_lower.astype(int), fill='tonexty', fillcolor='rgba(0,100,80,0.2)', line_color='rgba(255,255,255,0)', name='95% confidence interval')
	trace3 = go.Scatter(x=dates, y=y_mean.astype(int), name = 'mean', line_color='rgb(0,100,80)', line=dict(width = 4))
	trace4 = go.Scatter(x=dates, y=y_obs.astype(int), name = 'reported data (7-day average)', mode = 'markers', line_color='rgb(36, 21, 113)', marker=dict(size=10))

	n_pop = get_population(region)
	scale = 1E6/n_pop

	trace10 = go.Scatter(x=dates, y=(y_upper*scale), name = '95% confidence interval', fillcolor='rgba(0,100,80,0.2)', line_color='rgba(255,255,255,0)', showlegend=False, visible=False)
	trace20 = go.Scatter(x=dates, y=(y_lower*scale), fill='tonexty', fillcolor='rgba(0,100,80,0.2)', line_color='rgba(255,255,255,0)', name='95% confidence interval', visible=False)
	trace30 = go.Scatter(x=dates, y=(y_mean*scale ), name = 'mean', line_color='rgb(0,100,80)', line=dict(width = 4), visible=False)
	trace40 = go.Scatter(x=dates, y=(y_obs*scale  ), name = 'reported data (7-day average)', mode = 'markers', line_color='rgb(36, 21, 113)', marker=dict(size=10), visible=False)

	# TODO: interactive daily/cumm
	#y_obs_cumm = np.cumsum(y_obs)
	#y_mean_cumm = np.cumsum(y_mean)
	#y_lower_cumm = np.cumsum(y_lower)
	#y_upper_cumm = np.cumsum(y_upper)
#
	#trace100 = go.Scatter(x=dates, y=y_upper_cumm.astype(int), name = '95% confidence interval', fillcolor='rgba(0,100,80,0.2)', line_color='rgba(255,255,255,0)', showlegend=False, visible=False)
	#trace200 = go.Scatter(x=dates, y=y_lower_cumm.astype(int), fill='tonexty', fillcolor='rgba(0,100,80,0.2)', line_color='rgba(255,255,255,0)', name='95% confidence interval', visible=False)
	#trace300 = go.Scatter(x=dates, y=y_mean_cumm.astype(int), name = 'mean', line_color='rgb(0,100,80)', line=dict(width = 4), visible=False)
	#trace400 = go.Scatter(x=dates, y=y_obs_cumm.astype(int), name = 'reported data (7-day average)', mode = 'markers', line_color='rgb(36, 21, 113)', marker=dict(size=10), visible=False)
#
	#trace1000 = go.Scatter(x=dates, y=y_upper_cumm*scale, name = '95% confidence interval', fillcolor='rgba(0,100,80,0.2)', line_color='rgba(255,255,255,0)', showlegend=False, visible=False)
	#trace2000 = go.Scatter(x=dates, y=y_lower_cumm*scale, fill='tonexty', fillcolor='rgba(0,100,80,0.2)', line_color='rgba(255,255,255,0)', name='95% confidence interval', visible=False)
	#trace3000 = go.Scatter(x=dates, y=y_mean_cumm*scale, name = 'mean', line_color='rgb(0,100,80)', line=dict(width = 4), visible=False)
	#trace4000 = go.Scatter(x=dates, y=y_obs_cumm*scale, name = 'reported data (7-day average)', mode = 'markers', line_color='rgb(36, 21, 113)', marker=dict(size=10), visible=False)


	data = [trace1, trace2, trace3, trace4, trace10, trace20, trace30, trace40] #, trace100, trace200, trace300, trace400, trace1000, trace2000, trace3000, trace4000]

	updatemenus = []
	updatemenus.append(dict(active=0,
	     buttons=list([
	     	dict(label='Linear',
	             method='relayout',
	             args=[{'yaxis.type': 'linear'}]),
	        dict(label='Log',
	             method='relayout',
	             args=[{'yaxis.type': 'log'}])
	        ]),
	     type = "buttons",
	     direction="right",
		 showactive=True,
		 x=0.05,
		 xanchor="left",
		 y=1.12,
		 yanchor="top"
	    ))

	updatemenus.append(
	dict(active=0,
	     buttons=list([
	        dict(label='Total',
	             method='restyle',
	             args=[{'visible': [True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False]}]),
	        dict(label='Per million habitants',
	             method='restyle',
	             args=[{'visible': [False, False, False, False, True, True, True, True, False, False, False, False, False, False, False, False]}])
	        ]),
	     type = "buttons",
	     direction="right",
		 showactive=True,
		 x=0.2,
		 xanchor="left",
		 y=1.12,
		 yanchor="top"
	    ))

	#print(updatemenus[0]['buttons'][updatemenus[0]['active']]['args'][0]['visible'])
	#print(updatemenus[0]['buttons'][updatemenus[0]['active']]['args'][1]['yaxis']['title'])
	#  args=[{'visible': updatemenus[0]['buttons'][updatemenus[0]['active']]['args'][0]['visible']}, {'yaxis': {'type': 'linear',  'title': updatemenus[0]['buttons'][updatemenus[0]['active']]['args'][1]['yaxis']['title'] }}]),

	# plots
	fig = go.Figure(data=data, layout=dict(updatemenus=updatemenus, yaxis_title = 'Daily new cases', xaxis_title='Date', template='simple_white'))

	# save to html 
	fig.write_html(region + ".html", config={'displaylogo':False})

def main():
	parser = argparse.ArgumentParser(description="Generates the html plot of the specified region.")
	parser.add_argument('--folder', '-f', default='./data/', help='path of data folder')
	parser.add_argument('--region', '-r', default='canada', help='region of interest')
	parser.add_argument('--all', '-a', action='store_true', default=False, help='generate the plots for all available regions')

	args = parser.parse_args()

	folder = args.folder
	region = args.region.lower()
	is_all = args.all

	all_regions = ['australia', 'canada', 'france', 'germany', 'italy', 'netherlands',
	               'spain', 'switzerland', 'uk', 'us']

	if is_all: 
		for region in all_regions:
			covid19_html_plot(folder, region)
	else:             
		covid19_html_plot(folder, region)

if __name__ == '__main__':
	main()