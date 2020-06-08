import argparse
import os
import datetime as dt

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

#fig =px.scatter(x=range(10), y=range(10))
#fig.write_html("us.html")

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
	y_mean =  np.mean(y_sims, axis=0).astype(int)
	y_lower = np.percentile(y_sims, q=2.5, axis=0).astype(int)
	y_upper = np.percentile(y_sims, q=97.5, axis=0).astype(int)
	
	#y_obs_cumm = np.cumsum(y_obs)
	#y_mean_cumm = np.cumsum(y_mean)
	#y_lower_cumm = np.cumsum(y_lower)
	#y_upper_cumm = np.cumsum(y_upper)
	
	trace1 = go.Scatter(x=dates, y=y_upper, name = '95% confidence interval', fillcolor='rgba(0,100,80,0.2)', line_color='rgba(255,255,255,0)', showlegend=False)
	trace2 = go.Scatter(x=dates, y=y_lower, fill='tonexty', fillcolor='rgba(0,100,80,0.2)', line_color='rgba(255,255,255,0)', name='95% confidence interval')
	trace3 = go.Scatter(x=dates, y=y_mean, name = 'mean', line_color='rgb(0,100,80)', line=dict(width = 4))
	trace4 = go.Scatter(x=dates, y=y_obs, name = 'reported data (7-day average)', mode = 'markers', line_color='rgb(36, 21, 113)', marker=dict(size=10))


	data = [trace1, trace2, trace3, trace4]

	updatemenus = list([
	dict(active=1,
	     buttons=list([
	        dict(label='Log',
	             method='update',
	             args=[{'visible': [True, True, True, True, True]}, {'yaxis': {'type': 'log', 'title': 'Daily new cases'}}]),
	        dict(label='Linear',
	             method='update',
	             args=[{'visible': [True, True, True, True, True]}, {'yaxis': {'type': 'linear', 'title': 'Daily new cases'}}])
	        ]),
	     type = "buttons",
	     direction="right",
		 showactive=True,
		 x=0.05,
		 xanchor="left",
		 y=1.12,
		 yanchor="top"
	    )
	])

	# plots
	fig = go.Figure(data=data, layout=dict(updatemenus=updatemenus, yaxis_title='Daily new cases',
	                  xaxis_title='Date',
	                  template='simple_white'))



	#fig.update_layout(
    #annotations=[
    #    dict(text="Log/Linear", x=0, xref="paper", y=1.1, yref="paper",
    #                         align="left", showarrow=False),
    #    dict(text="Total/Per million", x=0.25, xref="paper", y=1.1,
    #                         yref="paper", showarrow=False),
    #    dict(text="Daily/Cummulative", x=.5, xref="paper", y=1.1, yref="paper",
    #                         showarrow=False)
    #])


	# TODO: interactive total/per million

	# TODO: interactive daily/cumm

	# save to html 

	fig.write_html(region + ".html")

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