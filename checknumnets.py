import pickle 
count = 0
with open("networks.pkl", "rb") as f:
	while 1==1:
		try:
			o = pickle.load(f)
		except EOFError:
			break

		count+=1

print(count)