#create levels with 
#no ladder
#no enemies
#just 2 platforms

import numpy as np
np.set_printoptions(edgeitems=10)
np.core.arrayprint._line_width = 180
import random

maxRows = 10
maxCols = 10

for i in range(30):
	mapTmp = np.zeros((maxRows, maxCols), dtype='int8')
	minSize = min(maxRows, maxCols)


	#first platform
	a = np.random.randint(low=3, high=minSize-2) #bottomost platform
	b = np.random.randint(3,8) #x end of platform 1
	c = np.random.randint(0,2) #to decide if platform 1 is left side or right side
	bottom_top = np.random.randint(0,2) #to decide if player is on top or bottom

	if(c==0):
		mapTmp[a, 1:b] = 1
	else:
		mapTmp[a, b:9] = 1

	#second platform
	mapTmp[a+1, 1:9] = 1 #second platform is fully covered 
	 
	#princess
	if(c==0):
		c1 = np.random.randint(1, b) #same as b i.e. we want to put princess on platform 1
	else:
		c1 = np.random.randint(b, 9) #same as b i.e. we want to put princess on platform 1
	if(bottom_top == 0):
		mapTmp[a-1, c1] = 20
	else:
		mapTmp[a-1, c1] = 21

	#player
	if(c==0):
		c2 = np.random.randint(b, 9) #we want to put player on platform 2
	else:
		c2 = np.random.randint(1, b) #we want to put player on platform 2
	if(bottom_top == 0):
		mapTmp[a, c2] = 21
	else:
		mapTmp[a, c2] = 20


	#walls
	mapTmp[0, 0:10] = 1
	mapTmp[9, 0:10] = 1
	mapTmp[0:10, 0] = 1
	mapTmp[0:10, 9] = 1

	#print(mapTmp)
	s = "map_1_"+str(i)+".txt"
	np.savetxt(s,mapTmp,fmt='%d',delimiter=',')



