#create levels with 
#no ladder
#no enemies
#just 2 platforms

import numpy as np
np.set_printoptions(edgeitems=10)
np.core.arrayprint._line_width = 180


maxRows = 10
maxCols = 10

for i in range(20):
	mapTmp = np.zeros((maxRows, maxCols), dtype='int8')
	minSize = min(maxRows, maxCols)


	#first platform
	a = np.random.randint(low=3, high=minSize-2) #bottomost platform
	b = np.random.randint(3,8) #x end of platform 1
	c = np.random.randint(0,2) #to decide if platform 1 is left side or right side

	if(c==0):
		mapTmp[a, 1:b] = 1
	else:
		mapTmp[a, b:9] = 1

	#second platform
	mapTmp[a+1, 1:9] = 1 #second platform is fully covered 
	 
	#princess
	if(c==0):
		princessCell = np.random.randint(1, b) #same as b i.e. we want to put princess on platform 1
	else:
		princessCell = np.random.randint(b, 9) #same as b i.e. we want to put princess on platform 1
	mapTmp[a-1, princessCell] = 20

	#player
	if(c==0):
		playerCell = np.random.randint(b, 9) #we want to put player on platform 2
	else:
		playerCell = np.random.randint(1, b) #we want to put player on platform 2
	mapTmp[a, playerCell] = 21


	#walls
	mapTmp[0, 0:10] = 1
	mapTmp[9, 0:10] = 1
	mapTmp[0:10, 0] = 1
	mapTmp[0:10, 9] = 1

	s = "map_1_"+str(i)+".txt"
	np.savetxt(s,mapTmp,fmt='%d',delimiter=',')



