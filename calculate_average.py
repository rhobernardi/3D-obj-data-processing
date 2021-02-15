import sys
from vispy.io import read_mesh #import the function from vispy.io (similar to "using namespace" from C++)


#Function to calculate the average of values in a vector
#
# Parameters: vector[] of float numbers that represents all coordenates x, y or z of the "special number"
# Returns: vector[] of float numbers that represents the average of each coordenate
def average(vector):
	if len(vector) > 0: #avoid division by zero when a vector is empty
		sum = 0
		for i in range(0,len(vector)): 			#loop that starts with i = 0 to length of vector - 1
												#(the range() function includes the fist term and excludes the last one)

			sum = sum + vector[i]				#update the value of the sum

		average = sum/len(vector) 				#calculate the average adding the terms and dividing by the number of numbers
		return average							#return the average. If the vector is empty, return None (null)


#Command line input method
#
#usage: ./prog.py <index_path_string> <obj_path_string> <result_path_string>
#reads the inputs with the argv[][]
idx_path = sys.[argv[1]]
obj_path = sys.[argv[2]]
result_path = sys.[argv[3]]

#Static input method
#
#File paths (change names here)
#idx_path = './file.idx'
#obj_path = './file.obj'
#result_path = './results.txt'


#Open and read the .idx file
#
#Throws an Exception if the .idx file doesn't exist
try:
	print('Reading ' + idx_path + '...')
	idx_file = open(idx_path,'r')			#Open .idx file as read only
	index_str = idx_file.readlines()		#Read all the lines of the file in string format in a vector

except FileNotFoundError:					#Handle the Exception if the file doesn't exist with a feedback and closes the program returning 1 (error)
	print('Could not find file ' + '\"' + idx_path + '\"')
	exit(1)


#Declaration of vectors
aux = [] 			#vector auxiliar (data handler)
number = [] 		#vector with the "special numbers" in original order
index_faces = [] 	#vector with the face indexes for the .obj file
index_vertex = [] 	#vector with the vertex indexes for the .obj file


#Loop to create the number and the index int vectors
#
#When these subroutines end, we'll have 3 vectors:
#  auxiliar vector to find out the max "special number" to use as flag
# "special number" vector and index vector, both with the same length and corresponding indexes
for i in range(0,len(index_str)):
	aux.append(int(index_str[i][index_str[i].find(',')+1:]))	#for each iteration, append the numbers AFTER the comma ("special numbers") changed from string to integer
	number.append(aux[i])										#save the original order of the "special numbers" to be equal to position of the faces indexes in the other vector
	index_faces.append(int(index_str[i][:index_str[i].find(',')])) #for each iteration, append the numbers BEFORE the comma, changed from string to integer

idx_file.close() #close the idx file. Everything is already in the memory now


#Find the highest "special number" to use in loop as a stop flag
#We can easily find sorting the vector and taking the last number of the vector
aux.sort()
min_number = 1	#As you don't want the zero numbers, the minimum of interest is 1
max_number = aux[len(aux)-1]


#Read the coordinates in the .obj file
#
#Throws an Exception if the obj file doesn't exist
try:
	print('Reading ' + obj_path + '...')
	coord = read_mesh(obj_path)			#With the funcion imported like in line 2, you just need to use the function of interest
except FileNotFoundError:
	print('Could not find file ' + '\"' + obj_path + '\"')
	exit(1)


#Open a new .txt file to write the values
#
#Open as writing mode. It can create the file if doesn't exist yet
result = open(result_path, 'w')


#Calculate average of the coordinates and write in .txt file
print('Indexing...')
print('Calculating average...')


#Auxiliar matrixes created to handle with integer vectors (coordenates [x,y,z] or vertex indexes from the faces)
aux_faces = [[]]
aux_vertex = [[]]
flag = 0 			#used for control data handling


#Here is the most important part of the entire code. These subroutines will search the values of the indexes and transform 
#them into the coordenates to calculate the average of each coordenate [x,y,z]

#Works like this:
# 1 - Choose a "special number" in the first "for";
# 2 - Go through the number vector searching for this "special number" and see the position of this;
# 3 - With this position, point to the same position in the index_faces vector, taking the corresponding value;
# 4 - Pointing these values in the faces vectors of the meshed obj vector, save it in the next free position of the aux_faces vector;
# 5 - When the aux_faces vector is ready, start go through aux_faces taking the indexes saving in the index_vertex;
# 6 - Now we point all the indexes to the vertexes vectors of the meshed obj vector and save in the aux vertex vector;
# 7 - After this, you have all the coordenates corresponding to the same "special number";
# 8 - Just sand the columns (same coordenate) to the function that calculate the average;
# 9 - Store it in the .txt file.
#The loop will repeat this algorithm until the end of the "special numbers".

for num in range(min_number,max_number+1): 	#the range of this loop is from the minimum to the maximum "special number". This
											#way you can ignore all the zeros in the number vector.
	
	for i in range(0,len(number)):	#this loop is important to define the limit of the iterations (from zero to number of "special numbers")
		
		index_vertex.clear()	#to avoid lots of data at the same time in the memory, we clear this vector after handle with it

		if i == 0:				#same here. Clear it after start go through the vectors again
			aux_faces.clear()

		if number[i] == num:
			if i == 0:
				aux_faces = [coord[1][index_faces[i]]] #store the first pointed face to the aux_faces

			else:	
				aux_faces.append(coord[1][index_faces[i]]) #append a pointed face to the aux_faces
				flag = i

	if number[flag] == num:
		for j in range(0,len(aux_faces)):				#go through the vector that contain the faces
			for k in range(0,len(aux_faces[j])):		
				index_vertex.append(aux_faces[j][k])	#store each value of this in the index_vertex

		for i in range(0,len(index_vertex)):			#go through the vector that contain the index vertexes
			if i == 0:
				aux_vertex.clear()
				aux_vertex = [coord[0][index_vertex[i]]]	#store the first vertex

			else:	
				aux_vertex.append(coord[0][index_vertex[i]])	#store the other vertexes

		# print the solutions of this "special number" in the .txt file
		result.write(str(num) + ': ' + str(average([x[0]for x in aux_vertex])) +' '+ str(average([y[1]for y in aux_vertex])) +' '+ str(average([z[2]for z in aux_vertex])) + '\n')

#Closes the .txt file containing the results
result.close()
print('Results have been saved in ' + result_path)