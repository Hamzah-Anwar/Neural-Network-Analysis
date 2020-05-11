def writetotxt(filename, data):
	with open(filename, "a")as file:
		for x in data:
			if x == data[-2]:
				if type(x) == list:
					x=x[-1]
				x =x *100
				x=str(x)+","
			elif x == data[-1]:
				x = str(x)
			else: x = str(x) + ","
			file.write(x)
		file.write("\n")