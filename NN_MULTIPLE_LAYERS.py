import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import pickle
import time
@np.vectorize
def dummyfunc():
	return
def sigmoid(x):
	return 1/(1 + np.e**-x)
def sig_der(x): # sigmoid dirivative
	return x * (1.0 -x)
def relu(x):
	return x * (x>0)
def rel_der(x):
	 return 1 * (x > 0)
def tanh(x):
	return np.tanh(x)
def tanh_der(x):
	return 1 - (tanh(x)**2)
def truncated_normal(mean=0, sd=1, low=0, upp=10):
	return truncnorm((low-mean)/sd, (upp-mean)/sd, loc=mean,
		scale=sd)
class NN():
	def __init__(self, input_nodes, output_nodes, learning, hidden, af):
		if af == "sigmoid":
			self.af = sigmoid
			self.af_der = sig_der
		elif af == "relu":
			self.af = relu
			self.af_der = rel_der
		elif af == "tanh":
			self.af = tanh
			self.af_der = tanh_der
		self.learning = learning
		self.architecture = []
		self.architecture.append(input_nodes)
		for k in hidden:
			self.architecture.append(k)
		self.architecture.append(output_nodes)
		self.weights = []
		self.temp_output = []
		self.epochacc = []
		self.makeWeights()


	def makeWeights(self):
		for i in range(len(self.architecture)-1):
			limit = 1/np.sqrt(self.architecture[i])
			w = truncated_normal(mean=0, sd=1, low=-limit, upp=limit)
			temp_weight_matrix = w.rvs((self.architecture[i+1], self.architecture[i]))
			self.weights.append(temp_weight_matrix)


	def train(self, input_vector, target_vector):
		input_vector = np.array(input_vector, ndmin=2).T
		target_vector = np.array(target_vector, ndmin=2).T
		self.temp_output = []
		self.forward(input_vector, self.weights)
		self.temp_output.insert(0, input_vector)
		error = target_vector - self.temp_output[-1]
		for i in range(len(self.temp_output)-1,0,-1):
			if i == len(self.temp_output)-1 and (self.af == relu or self.af == tanh):
				delta = self.learning * error * sig_der(self.temp_output[i])
			else:
				delta = self.learning * error * self.af_der(self.temp_output[i])
			delta = np.dot(delta, self.temp_output[i-1].T)
			self.weights[i-1] += delta
			error = np.dot(self.weights[i-1].T, error)

	def epoch(self, epochs, data, onehotdata, test, testlabels):
		for i in range(epochs):
			for x in range(len(data)):
				self.train(data[x], onehotdata[x])
			corrects, wrongs = self.evaluate(test, testlabels)
			testacc = corrects/(corrects+wrongs)
			singleacc = testacc
			self.epochacc.append(singleacc)
		return self.epochacc


	def forward(self, input_vector, weights):
		if len(weights) == 0:
			return
		else:
			if len(weights) == 1 and (self.af == relu or self.af == tanh):	
				input_vector = sigmoid(np.dot(weights[0], input_vector))
			else:
				input_vector = self.af(np.dot(weights[0], input_vector))
			self.temp_output.append(input_vector)
			self.forward(input_vector, weights[1:])

		return self.temp_output[-1]

	def run(self, input_vector):
		return self.forward(input_vector, self.weights)

	def evaluate(self, data, labels):
		right =0
		wrong =0
		for i in range(len(data)):
			prediction = np.argmax(self.run(data[i]))
			if prediction == labels[i]:
				right += 1

			else:
				wrong += 1

		return right,wrong

def main(input_nodes, output_nodes, learning, hidden, af, epochs, trainrange):
	totalnodes = sum(hidden)
	with open("numbers.pkl", "br") as fh:
		data = pickle.load(fh)
	trimgs = data[0]
	teimgs = data[1]
	trlabels = data[2]
	telabels = data[3]
	trlabelso = data[4]
	telabelso = data[5]
	trimgs, trlabelso = trimgs[:trainrange], trlabelso[:trainrange] 
	layers = len(hidden)
	ann = NN(input_nodes, output_nodes, learning, hidden, af)
	start = time.clock()
	if epochs == 1:
		for i in range(len(trimgs)): ann.train(trimgs[i], trlabelso[i])
		corrects, wrongs = ann.evaluate(teimgs, telabels)
		acc = corrects/(corrects+wrongs)
	elif epochs > 1:
		acc = ann.epoch(epochs, trimgs, trlabelso, teimgs, telabels)
	end_time = round((time.clock() - start),3)
	final_values = [learning, layers, totalnodes, af, epochs, trainrange, end_time, acc, hidden]
	with open("networks.pkl", "ab") as d:
		pickle.dump(ann, d)
	return final_values

def runimg(img, option):
	from convert import web2arr
	with open("networks.pkl", "rb") as f:
		for i in range(option+1):
			ann = pickle.load(f)

	x = np.argmax(ann.run(web2arr(img)))
	return x