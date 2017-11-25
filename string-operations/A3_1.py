
# ask the user for a sentence
sentence = input('Please enter the sentence: ')
# store the starting location of a given word in the input sentence – initialize it to 0
last_index = 0
while True:
    # find to start looking for the blank at index last_index AND assign the index returned by find to a variable called blank_index
    blank_index = str(sentence).find(' ', last_index)
    if blank_index > -1:
        # extract a word from last_index up to blank_index
        word = str(sentence)[last_index : blank_index]
        # and print the word
        print(word)
        # update last_index to be the location directly after blank_index 
        last_index = blank_index + 1
    else:
        # there are no more blanks to be processed
        # extract the last word from the user’s string 
        word = str(sentence)[last_index : len(sentence)]
        # print the word
        print(word)
        # Exit the loop
        break
