#create levels with 
#2 ladder
#3 platforms
#no enemies
#princess and player can be either on top or bottom platform


import numpy as np
np.set_printoptions(edgeitems=10)
np.core.arrayprint._line_width = 180
import random

maxRows = 10
maxCols = 10

for i in range(30):
	mapTmp = np.zeros((maxRows, maxCols), dtype='int8')
	minSize = min(maxRows, maxCols)

	ladder_length1 = 3 #length of 1st ladder
	top_y = random.randint(3, 6-ladder_length1) #top platform
	top_x = np.random.randint(3,8) #x end of platform 1
	left_right = np.random.randint(0,2) #to decide if platform 1 is left side or right side
	bottom_top = np.random.randint(0,2) #to decide if player is on top or bottom


	#first platform
	if(left_right==0):
		mapTmp[top_y, 1:top_x] = 1
	else:
		mapTmp[top_y, top_x:9] = 1

	#second platform
	middle_y = top_y+ladder_length1
	mapTmp[middle_y, 1:9] = 1 #second platform is fully covered 
	 

	#ladder 1
	if(left_right==0):
		mapTmp[top_y-1:middle_y, top_x:top_x+2] = 2
	else:
		mapTmp[top_y-1:middle_y, top_x-2:top_x] = 2

	#ladder 2
	a = range(1, top_x-1)+range(top_x+1,8)
	middle_x = random.choice(a) #x end of platform 1
	mapTmp[middle_y-1:9, middle_x:middle_x+2] = 2

	#princess and player - one of them is on top platform, the latter on bottom
	if(left_right==0):
		c1 = np.random.randint(1, top_x) #same as b i.e. we want to put princess on platform 1
	else:
		c1 = np.random.randint(top_x, 9) #same as b i.e. we want to put princess on platform 1
	if(bottom_top==0):
		mapTmp[top_y-1, c1] = 20
	else:
		mapTmp[top_y-1, c1] = 21

	a = range(1, middle_x-2)+range(middle_x+2,9)
	c2 = random.choice(a)
	if(bottom_top==0):
		mapTmp[8, c2] = 21
	else:
		mapTmp[8, c2] = 20

	#walls
	mapTmp[0, 0:10] = 1
	mapTmp[9, 0:10] = 1
	mapTmp[0:10, 0] = 1
	mapTmp[0:10, 9] = 1

	s = "map_3_"+str(i)+".txt"
	np.savetxt(s,mapTmp,fmt='%d',delimiter=',')



