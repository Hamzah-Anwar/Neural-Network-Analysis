
#text file data format: [learning rate, #oflayers, #ofnodes, function, epochs, samples, time, accuracy]
import plotly as py
import plotly.graph_objs as go
def divplot(xvar, yvar):
	form = ["learning rate", "number of layers", "number of hidden nodes", "epochs", "samples", "time", "accuracy", "structure"]
	with open("nnresults.txt")as file:
		txtdata = file.readlines()
	txtdata = [i.strip("\n").split(",") for i in txtdata]
	relu =[]
	tanh = []
	sigmoid =[]
	for i in range(len(txtdata)):
		if "relu" in txtdata[i]:
			del txtdata[i][3]
			relu.append(txtdata[i])
		if "tanh" in txtdata[i]:
			del txtdata[i][3]
			tanh.append(txtdata[i])
		if "sigmoid" in txtdata[i]:
			del txtdata[i][3]
			sigmoid.append(txtdata[i])
	relux, reluy = [float(i[xvar]) for i in relu], [float(i[yvar]) for i in relu]
	relu_sorted = sorted(zip(relux, reluy))
	relux, reluy = map(list,zip(*relu_sorted))
	tanhx, tanhy =[float(i[xvar]) for i in tanh], [float(i[yvar]) for i in tanh]
	tanh_sorted = sorted(zip(tanhx, tanhy))
	tanhx, tanhy = map(list,zip(*tanh_sorted))
	sigmoidx, sigmoidy = [float(i[xvar]) for i in sigmoid], [float(i[yvar]) for i in sigmoid]
	sigmoid_sorted = sorted(zip(sigmoidx, sigmoidy))
	sigmoidx, sigmoidy = map(list,zip(*sigmoid_sorted))
	relutrace = go.Scatter(
		x=relux,
		y=reluy,
		name="RELU"
	)
	tanhtrace = go.Scatter(
		x=tanhx,
		y=tanhy,
		name="TANH"
	)
	sigmoidtrace = go.Scatter(
		x=sigmoidx,
		y=sigmoidy,
		name="SIGMOID"
	)
	data = [relutrace, tanhtrace, sigmoidtrace]
	layout = go.Layout(
		title = go.layout.Title(text=f"{form[yvar]} against {form[xvar]}"),
		
		xaxis=go.layout.XAxis(
			title=go.layout.xaxis.Title(text=f"{form[xvar]}")
		),
		yaxis=go.layout.YAxis(
			title=go.layout.yaxis.Title(text=f"{form[yvar]}")
		)
	)
	fig = go.Figure(data=data, layout=layout)
	x = py.offline.plot(fig, include_plotlyjs=False, output_type="div")
	return x












