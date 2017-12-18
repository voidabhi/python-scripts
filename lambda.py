import random

data = range(10)
random.shuffle(data)

''' map vs without map'''
data1 = [x*x for x in data]
data2 = map(lambda x: x*x, data )

''' filter vs without filter '''
data3 = filter(lambda x: x%2 != 0, data)
data4 = []
for x in data:
	if x%2 != 0:
		data4.append(x)

''' reduce vs without reduce '''
data5 = reduce(lambda x, y: x + y, data)
data6 = 0
for x in data:
	data6 += x
