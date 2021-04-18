# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 21:17:20 2019

@author: DELL
"""

# name: File path of the pgm image file
# Output is a 2D list of integers
import math
def readpgm(name):
	image = []
	with open(name) as f:
		lines = list(f.readlines())
		if len(lines) < 3:
			print("Wrong Image Format\n")
			exit(0)

		count = 0
		width = 0
		height = 0
		for line in lines:
			if line[0] == '#':
				continue

			if count == 0:
				if line.strip() != 'P2':
					print("Wrong Image Type\n")
					exit(0)
				count += 1
				continue

			if count == 1:
				dimensions = line.strip().split(' ')
				print(dimensions)
				width = dimensions[0]
				height = dimensions[1]
				count += 1
				continue

			if count == 2:	
				allowable_max = int(line.strip())
				if allowable_max != 255:
					print("Wrong max allowable value in the image\n")
					exit(0)
				count += 1
				continue

			data = line.strip().split()
			data = [int(d) for d in data]
			image.append(data)
	return image	

# img is the 2D list of integers
# file is the output file path

def writepgm(img, file):
	with open(file, 'w') as fout:
		if len(img) == 0:
			pgmHeader = 'p2\n0 0\n255\n'
		else:
			pgmHeader = 'P2\n' + str(len(img[0])) + ' ' + str(len(img)) + '\n255\n'
			fout.write(pgmHeader)
			line = ''
			for i in img:
				for j in i:
					line += str(j) + ' '
			line += '\n'
			fout.write(line)
########## Function Calls ##########
x = readpgm('test.pgm')			# test.pgm is the image present in the same working directory
writepgm(x, 'test_o.pgm')		# x is the image to output and test_o.pgm is the image output in the same working directory
###################################
def averagingfilter(s):
    image=readpgm(s)
    height=len(image)
    width=len(image[0])
    Image=[[0 for i in range(width)] for j in range(height)]
    for i in range(1,height-1):
        for j in range(1,width-1):
            Image[i][j]=(image[i-1][j-1]+image[i-1][j]+image[i-1][j+1]+image[i][j-1]+image[i][j]+image[i][j+1]+image[i+1][j-1]+ image[i+1][j]+image[i+1][j+1])//9
            
    for j in range(width-1):
        Image[0][j]=image[0][j]
        Image[height-1][j]=image[height-1][j]
        
    for i in range(height-1):
        Image[i][0]=image[i][0]
        Image[i][width-1]=image[i][width-1]
    return Image
writepgm(averagingfilter('test.pgm'),'average1.pgm')

def edgedetection(image):
    Image=readpgm(image)
    height=len(Image)
    width=len(Image[0])
    L=[0 for i in range(width+2)]
    image = [Image[i].copy() for i in range(height)]
    for i in range (height):
        image[i].append(0)
        image[i].insert(0,0)
    image=[L]+image+[L]
    
    
    
    edge=[[0 for j in range(width)] for i in range(height)]
    
    '''
    for i in range(height+1):
        edge[i][0]=0
        edge[i][width]=0
    for j in range(width):
        edge[0][j]=0
        edge[-1][j]=0'''
    maximum=0
    for i in range(1,height+1):
        for j in range(1,width+1):
            hdif = (image[i-1][j-1]-image[i-1][j+1]) + 2*(image[i][j-1]-image[i][j+1]) + (image[i+1][j-1]-image[i+1][j+1])
            vdif = (image[i-1][j-1]-image[i+1][j-1]) + 2*(image[i-1][j]-image[i+1][j]) + (image[i-1][j+1]-image[i+1][j+1]) 
            
            edge[i-1][j-1]= int(math.sqrt(hdif*hdif + vdif*vdif))
            if maximum<edge[i-1][j-1]:
                maximum=edge[i-1][j-1]
    for i in range(height):
        for j in range(width):
            edge[i][j]=(edge[i][j]*255)//(maximum+1)
    return edge
writepgm(edgedetection('test.pgm'),'edge1.pgm')
writepgm(edgedetection('flower_gray.pgm'),'edge2.pgm')
def pathminenergy(edge1,image):
    edge=(edge1)
    image=readpgm(image)
    height=len(edge)
    width=len(edge[0])
    minenergy=[[0 for i in range(width)]for i in range(height)]
    for j in range(width):
        minenergy[0][j]=edge[0][j]
        ''' for j in range(1,height):
        minenergy[j][0]=edge[j][0]+min(minenergy[j-1][0],minenergy[j-1][1])
        minenergy[j][width-1]=edge[j][width-1]+min(minenergy[j-1][width-1],minenergy[j-1][width-2])
    '''
        
    for i in range(1,height):
        
        minenergy[i][width-1]=edge[i][width-1]+min(minenergy[i-1][width-1],minenergy[i-1][width-2])
        minenergy[i][0]=edge[i][0]+min(minenergy[i-1][0],minenergy[i-1][1])
        for j in range(1,width-1):
            minenergy[i][j]=edge[i][j]+min(minenergy[i-1][j],minenergy[i-1][j-1],minenergy[i-1][j+1])
            
    s=minenergy[height-1].index(min(minenergy[height-1]))
    for j in range(width):
        if minenergy[height-1][j]==minenergy[height-1][s]:
            image[height-1][j]=-1
    for i in range(height-1,0,-1):
        for j in range (0,width):
            if image[i][j]==-1:
                t=minenergy[i-1].index(min(minenergy[i-1][j-1],minenergy[i-1][j],minenergy[i-1][j+1]))
                image[i-1][t]=-1
    for i in range(height):
        for j in range(width):
            if image[i][j]==-1:
                image[i][j]=255
    return image
writepgm(pathminenergy(edgedetection('test.pgm'),'test.pgm'),'minpath.pgm')
writepgm(pathminenergy(edgedetection('flower_gray.pgm'),'flower_gray.pgm'),'minpath44.pgm')
           
            
    