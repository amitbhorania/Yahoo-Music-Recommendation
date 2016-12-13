##################################################################
### File - Ensemble_Algo.py
###
### Description - 
###	This file was provided by Meng Cao. We Changed the code
###	according to our requirement.
###
###	Changed the Code to Automatically set the Correction Rate 
###	as per the number of input file
###
###	Split Logic to write 1s and 0s not always write three 1s
###	and three 0s from 6 test tracks. Therefore the logic is 
###	changed to Sort the Result and then provide the 1s and 0s
### 
##################################################################


##################################################################
## Comment from Meng Cao
## Ensemble result using Correlation Matrix
## By Meng Cao
# This program is not fully loaded, need some work to make it runs
# 1. Modify the loading part to fit you results.
# 2. Input you correct rate manually
# 2. Make sure you can understand how the coefficients are derived 
##################################################################

## Import
from __future__ import print_function
from operator import itemgetter
import numpy as np
import os.path

predictionFile = open("esembled2.txt", "w")

def sort_list(input_list):
	sorted_list = sorted(input_list, key = itemgetter(1))
	i=0
	pred_dic = {}
	for item in sorted_list:
		if i < 3:
			pred_dic[item[0]]=0
		else:
			pred_dic[item[0]]=1
		i += 1
	return 	[pred_dic[item[0]] for item in input_list]

# Load Data
# modify the name so fit your files.
resultsList=[]
i=1
result_c = 0

#########################################################################
while os.path.isfile("prediction%d.txt"%i): # Check if file exist
	result_c += 1
	resultsList.append(np.genfromtxt('prediction%d.txt'%(i),delimiter = ','))
	print("Loading file: %d"%i)
	i += 1
#########################################################################

result_length = len(resultsList[0])
print("%d TestResult file found" % result_c)

# Load correct rate for each prediction
#########################################################################
#correct_rate = [1,1,1,1] 
correct_rate = [1] * result_c
#print ("Correction Rate new try")
#print (correct_rate)

#########################################################################
correct_rate = np.array(correct_rate)

print("Correct Rate:", correct_rate)

# Correlation Matrix
co_matrix = np.zeros([len(resultsList),len(resultsList)])
for i in range(len(resultsList)):
	for j in range(len(resultsList)):
		co_matrix[i,j]= (resultsList[i]==resultsList[j]).sum()/float(result_length)

np.savetxt("CorrelationMatrix.csv",co_matrix,delimiter=",",fmt="%.4f")

# Coefficient 
coef = np.dot(np.linalg.inv(co_matrix),correct_rate)
print("Alpha:",coef)

# Ensemble 	
r_matrix = np.zeros([result_length,result_c])

for i in range(result_c):
	r_matrix[:,i]= resultsList[i]*coef[i]

print (r_matrix)

result = r_matrix.sum(1)

print (result)
count = result_length+1

input_list = []
for i in range(1, count):
	input_list.append([i%6,result[i-1]])
	if (i%6 == 0):
		prediction_result = sort_list(input_list)
		for item in prediction_result:
			# Write the File
			predictionFile.write(str(item)+"\n")
		input_list = []


#split_point = coef.sum()/2
#result[result>=split_point]=1
#result[result<split_point]=0

#print("Split Point:",split_point)
		
#np.savetxt("esembled2.txt",result,delimiter=",",fmt="%d")
