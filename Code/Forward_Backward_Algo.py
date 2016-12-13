##################################################################
### File - Forward_Backward_Algo.py
###
### Description - 
###	Algorithm to Predict the Ratings using Forward and Backword 
###	Hierarchy of Track, Album, Artist and Genre with equal Weights
###
###	Whole New Algorithm is developed for this Algorithm
### 
##################################################################

##################################################################
### Libraries & Predefined Functions
## Load Libraries
from __future__ import print_function
from operator import itemgetter
import time
import os

## Environment Variables
TEST_DATA_FILE = "RawData/testTrack_hierarchy.txt"
TRAIN_DATA_FILE = "RawData/trainIdx2.txt"
RESULT_FILE = "Results/prediction_new_7_25_05.txt"		# Result file
RATE_OUTPUT_FILE = "Results/rate_output_heirarchy_7_25_05.txt"		# Result file
TRACK_FILE = "RawData/trackData2.txt"
ALBUM_FILE = "RawData/albumData2.txt"

none_value = 0		# Number to replace the none values

level1_weight = 1
level2_weight = 1
level3_weight = 1

# Create Folder is not there
if not os.path.isdir("Results"):
	os.makedirs("Results")

## Functions
# Replace the highest three scores with 1, and lowest three scores with 0.
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

# Function that read multiple lines, "num" is the number of lines you want to read
def read_lines(file, num):
	lines = []
	line = file.readline()
	lines.append(line)
	if line:
		for i in range(1,num):
			lines.append(file.readline())
		return lines
	else:
		return line

##################################################################
### Main Program
## Variables
start_time = time.time()

##################################################################
# Code to Gather Album-> Track Info
MAX_ID = 296200

hierarchy_data = [[] for i in range (MAX_ID)]

with open(TRACK_FILE, 'r') as trackData:
	for line in trackData:
		[track_id,album_id,track_detail] = line.strip("\n").split("|",2)
		if album_id != "None":
			hierarchy_data[int(album_id)].append(int(track_id))

with open(ALBUM_FILE, 'r') as albumData:
	for line in albumData:
		data = line.strip("\n").split("|")
		# Check if the Artist is not None then add that info in list
		if data[1] != "None":
			hierarchy_data[int(data[1])].append(int(data[0]))
		if len(data) > 2:
			# It means that Genre info is present
			for i in range(2, len(data)):
				if data[1] != "None":
					hierarchy_data[int(data[i])].append(int(data[1]))

##################################################################
# Code for algorithm which will predict the result

# Dictionary for Training
train_dict = {}
train_user = -1
start_time = time.time()
ratOutFile = open(RATE_OUTPUT_FILE, "w")

# Source file that contains the item ID in the hierarchy structure
with open(TEST_DATA_FILE) as testData:
	# Source file that contains the item ratings by each user.
	with open(TRAIN_DATA_FILE) as trainData:
		# File to Write the Prediction Result
		with open(RESULT_FILE, "w") as predictionFile:
			# 6 test song for each user
			lines_test = read_lines(testData,6)
			while lines_test:
				cur_test = lines_test[0].strip("\n").split("|")
				cur_user = cur_test[0]

				# Navigate to the current user in training data.
				while int(train_user) < int(cur_user):
					lines_train = trainData.readline()
					[train_user,train_user_count] = lines_train.strip("\n").split("|")
					lines_train = read_lines(trainData,int(train_user_count))
					
				# Clear Dictionary for the current user.
				train_dict.clear()

				# Fill up the Dictionary
				for line_train in lines_train:
					train_dict_item = line_train.strip("\n").split("\t")
					train_dict[train_dict_item[0]] = int(train_dict_item[1])

				output_list = []
				# Get ratings for each line in hierarchy structure.
				for line_test in lines_test:
					test_song = line_test.strip("\n").split("|")

					# 0 - User ID
					# 1 - Track ID
					# 2 - Album ID
					# 3 - Artist ID
					# 4 - Genre ID
					track = test_song[1]
					album = test_song[2]
					artist = test_song[3]

					track_ratings = []
					level1_ratings = []
					level2_ratings = []
					level3_ratings = []
					# Check for the Album ID Rating
					if album != "None":				
						if album in train_dict:
							track_ratings.append(train_dict[album])
							level1_ratings.append(train_dict[album])

						# Now check for the Tracks of the given Album
						album_info = hierarchy_data[int(album)]
						if  len(album_info) > 0:
							# Tracks are present
							for i in range(len(album_info)):
								if album_info[i] in train_dict:
									track_ratings.append(train_dict[album_info[i]])
									level1_ratings.append(train_dict[album_info[i]])
					else:
						track_ratings.append(0)
						level1_ratings.append(0)

					if artist != "None":				
						# Check for the Artist ID Rating				
						if artist in train_dict:
							track_ratings.append(train_dict[artist])
							level2_ratings.append(train_dict[artist])


						# Now check for the Album of the given Artist
						artist_info = hierarchy_data[int(artist)]
						if  len(artist_info) > 0:
							# Albums are present
							for i in range(len(artist_info)):
								if artist_info[i] in train_dict:
									track_ratings.append(train_dict[artist_info[i]])
									level2_ratings.append(train_dict[artist_info[i]])
					else:
						track_ratings.append(0)
						level2_ratings.append(0)


					# Check whether the Given Track has Genres or not
					if len(test_song) > 4:
						# Genres are present
						for i in range(4,len(test_song)):
							# Do the Below Process for Each Genre
							genre = test_song[i]
							if genre != "None":
								if genre in train_dict:
									track_ratings.append(train_dict[genre])
									level3_ratings.append(train_dict[genre])
			
								# Now check for the Artist of the given Genre
								genre_info = hierarchy_data[int(genre)]
								if  len(genre_info) > 0:
									# Artists are present
									for j in range(len(genre_info)):
										if genre_info[j] in train_dict:
											track_ratings.append(train_dict[genre_info[j]])
											level3_ratings.append(train_dict[genre_info[j]])
							else:
								track_ratings.append(0)
								level3_ratings.append(0)

					# Till now all the ratings are added in the list
					# Find the Average and store it with Track ID
					rat_value = 0
					level1_value = 0
					level2_value = 0
					level3_value = 0
					if len(level1_ratings) > 0:
						# Sum up the ratings
						level1_value = sum(level1_ratings)/len(level1_ratings)
						level1_value = level1_value * level1_weight

					if len(level2_ratings) > 0:
						# Sum up the ratings
						level2_value = sum(level2_ratings)/len(level2_ratings)
						level2_value = level2_value * level2_weight

					if len(level3_ratings) > 0:
						# Sum up the ratings
						level3_value = sum(level3_ratings)/len(level3_ratings)
						level3_value = level3_value * level3_weight
					rat_value = level1_value + level2_value + level3_value
					output_list.append([track,rat_value])
					# Algo Complete
							
				# Sort the Sorted List and Write the prediction in the File
				prediction_result = sort_list(output_list)
			
				# Output prediction to result file
				for item in prediction_result:
					predictionFile.write(str(item)+"\n")		

				# Read hierarchy structure for next user
				lines_test = read_lines(testData,6)

				print(cur_user,"%.2f s"%(time.time()-start_time))

print("Finished, Spend %.2f s"%(time.time()-start_time))

