import numpy as np
import math
from PIL import Image
import PIL.ImageOps
import cv2
from scipy import ndimage
def getBestShift(img):
	cy, cx = ndimage.measurements.center_of_mass(img)
	rows,cols = img.shape
	shiftx = np.round(cols/2.0-cx).astype(int)
	shifty = np.round(rows/2.0-cy).astype(int)
	return shiftx, shifty
def shift(img, sx, sy):
	rows,cols = img.shape
	M = np.float32([[1,0,sx], [0,1,sy]])
	shifted = cv2.warpAffine(img,M,(cols,rows))
	return shifted
def web2arr(img):
	img = np.asfarray(img)
	img = img.reshape((300, 300))
	img = Image.fromarray(img)
	img = img.resize((28,28))
	temp = np.asarray(img)
	while np.sum(temp[0]) == 0:
		temp = temp[1:]
	while np.sum(temp[:,0]) ==0:
		temp = np.delete(temp,0,1)
	while np.sum(temp[-1]) == 0:
		temp = temp[:-1]
	while np.sum(temp[:, -1]) == 0:
		temp = np.delete(temp, -1,1)
	rows,cols = temp.shape
	if rows > cols:
		factor = 20.0/rows
		rows = 20
		cols = int(round(cols*factor))
		temp = cv2.resize(temp, (cols,rows))
	else:
		factor = 20.0/cols
		cols = 20
		rows = int(round(rows*factor))
		temp = cv2.resize(temp, (cols,rows))
	colsPadding = (int(math.ceil((28-cols)/2.0)),int(math.floor((28-cols)/2.0)))
	rowsPadding = (int(math.ceil((28-rows)/2.0)),int(math.floor((28-rows)/2.0)))
	temp = np.lib.pad(temp,(rowsPadding,colsPadding),'constant')
	shiftx,shifty = getBestShift(temp)
	shifted = shift(temp,shiftx,shifty)
	temp = shifted
	temp = np.asfarray(temp)/255
	temp = temp.reshape(784)
	return temp


# def web2arr(img):
# 	img = np.asfarray(img)
# 	img = img.reshape((300, 300))
# 	img = Image.fromarray(img)
# 	img = img.resize((28,28))
# 	temp = np.asarray(img)
# 	while np.sum(temp[0]) == 0:
# 		temp = temp[1:]
# 	while np.sum(temp[:,0]) ==0:
# 		temp = np.delete(temp,0,1)
# 	while np.sum(temp[-1]) == 0:
# 		temp = temp[:-1]
# 	while np.sum(temp[:, -1]) == 0:
# 		temp = np.delete(temp, -1,1)
# 	img = Image.fromarray(temp)
# 	img.show()
# 	img = img.resize((20,20))
# 	back = Image.new("L", (28,28))
# 	position = (4,4)
# 	back.paste(img, position)
# 	fac = 255*0.99+1
# 	temp = np.asfarray(back)/fac
# 	temp = temp.reshape(784)
# 	print(temp)
# 	return temp