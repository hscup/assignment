# this list will store the test scores we will read from the file
scores = []

# Ask the user for a file name 
file_name = input('Please enter the file name: ')

# open the file for reading
with open(file_name, 'r') as score_file:
    for line in score_file:
        # Convert the test score in the current line to a number 
        score = int(line.strip())
        # Add the test score to the list 
        scores.append(score)
#  file closed

# Sort the list using the built in python function sort 
scores.sort()

# Get the len of list scores
len_list_scores = len(scores)
# if the list length is odd 
if len_list_scores % 2 == 1:
    # median gets assigned the middle value of that sequence 
    middle_position = len_list_scores // 2
    median_value =scores[middle_position]

# list length is even
else:
    # val1 gets the value at index list length divided by 2 
    val1 = scores[len_list_scores // 2]
    # val2 gets the value at index list_length divided by 2 – 1 (see hint 3)
    val2 = scores[len_list_scores // 2 - 1]
    # median gets assigned the average of val1 and val2 (i.e., val1 + val2 / 2)
    median_value = (val1 + val2) / 2

# print the median value to console
print(median_value)