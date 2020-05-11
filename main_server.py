from flask import Flask, render_template, url_for, request, redirect, jsonify
from NN_MULTIPLE_LAYERS import main
from NN_MULTIPLE_LAYERS import runimg
from plotgraph import divplot
from write import writetotxt
import numpy as np
server = Flask(__name__)
@server.route("/")
def index():
	return render_template("home.html")

@server.route("/train")
def train():
	return render_template("train.html")

@server.route("/data", methods =["POST", "GET"])
def data():
	formdata = request.form 
	innodes = 784
	onodes = 10
	hlayers = formdata.getlist("hiddenlayers")
	hlayers = [int(i) for i in hlayers]
	lr = float(formdata.getlist("learningrate")[0])
	activation = formdata.getlist("activation")[0]
	epochs = int(formdata.getlist("epochs")[0])
	trainrange = int(formdata.getlist("trainrange")[0])
	final_values = main(innodes, onodes, lr, hlayers, activation, epochs, trainrange)
	writetotxt("nnresults.txt", final_values)
	return render_template("trained.html", layers=len(hlayers), totalnodes=final_values[2], lr=lr, activation=activation, epochs=epochs, epochacc=final_values[7], trainrange=trainrange, time=final_values[6]) 
@server.route("/results")
def results():
	return render_template("results.html")

@server.route("/graph", methods=["POST"])
def graph():
	graphdata = request.form 
	xvar = int(graphdata.getlist("x")[0])
	yvar = int(graphdata.getlist("y")[0])
	x = divplot(xvar, yvar)
	return render_template("graph.html", div=x)

@server.route("/test")
def test():
	with open("nnresults.txt", "r")as file:
		txtdata = file.readlines()
	txtdata = [i.strip("\n").split(",") for i in txtdata]
	return render_template("test.html", numnetworks=len(txtdata),networks=txtdata)

@server.route("/draw", methods=["POST"])
def draw():
	global option
	option = int(request.form.getlist("network")[0]) 
	with open("nnresults.txt", "r")as file:
		txtdata = file.readlines()
	txtdata = [i.strip("\n").split(",") for i in txtdata]
	return render_template("page.html", data=txtdata[option]) 

@server.route('/givenumber', methods=['POST', "GET"])
def givenumber():
	news = request.form.getlist("img[]")
	n = str(runimg(news, option)) 
	return jsonify(number=n)

@server.route('/best')
def best():
	with open("nnresults.txt", "r")as file:
		txtdata = file.readlines()
	txtdata = [i.strip("\n").split(",") for i in txtdata]
	biggest =0
	for i in txtdata:
		if float(i[7]) > biggest:
			biggest = float(i[7])
			best = i
	return render_template("best.html", data=best)
if __name__ == "__main__":
	server.run(debug=True, host="0.0.0.0", port=80)