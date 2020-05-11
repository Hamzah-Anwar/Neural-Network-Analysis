import pickle
import numpy as np
#load the testdata
tedata = np.loadtxt("mnist_test.csv", delimiter=",")
#load the traindata
trdata = np.loadtxt("mnist_train.csv", delimiter=",")
# print(f"number of test samples {len(tedata)}") #number of lines (imgs) in the testdata array
# print(f"number of train samples {len(trdata)}") #number of lines (imgs) in the traindata array
# print(tedata[0]) #show the first element in the test data array
# print(f"the number of pixels in each img is {len(tedata[0])}") # the number of pixels in each img


# images stored as 3d numpy float array "trdata[:, 1:]" takes all values of trdata apart from 1st element in each array 
teimgs = np.asfarray(tedata[:, 1:])/255 #divide by 255 so that all values are between 1 and 0
trimgs = np.asfarray(trdata[:, 1:])/255

#create the lables for the data and store in a numpy float array "trdata[:, :1]" means to take only the 1st element in each array 
trlabels = np.asfarray(trdata[:, :1])
telabels = np.asfarray(tedata[:, :1])

print(len(teimgs[0]))
print(telabels[0])

lr = np.arange(10) # create temporary numpy array containing elements from 0 to 9
#for each value in trlabels if equal to a value in lr returns array with 0 when false and 1 when true
trlabelso = (lr==trlabels).astype(np.float)
telabelso = (lr==telabels).astype(np.float)

#to prevent any training issues cannot have any values that are 0 or 1 so use 0.1 and 0.99 instead
trlabelso[trlabelso==0] = 0.01
trlabelso[trlabelso==1] = 0.99
telabelso[telabelso==0] = 0.01
telabelso[telabelso==1] = 0.99


# import matplotlib.pyplot as plt
# # for i in range(10):
# # 	img = trimgs[i].reshape((28,28))
# # 	plt.imshow(img, cmap="Greys")
# # 	plt.show()
# import pickle
with open("numbers.pkl", "bw") as file:
	data = (trimgs, teimgs, trlabels, telabels, trlabelso, telabelso)
	pickle.dump(data, file)
