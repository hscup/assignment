import sys
from random import randint


def parse_line(prob_info):
    # the function parses this prob_info string by extracting the problem
    # (i.e., without the < > brackets) and the answer and adds each
    # (i.e., the problem and the answer) to a list
    # (hint: use the string find method; then use append; then return the list)
    result = []
    problem_start_index = str(prob_info).find('<')
    problem_end_index = str(prob_info).find('>')
    if problem_start_index > -1 and problem_end_index > problem_start_index:
        result.append(prob_info[problem_start_index + 1: problem_end_index])

    solution_start_index = str(prob_info).find('<', problem_end_index + 1)
    solution_end_index = str(prob_info).find('>', problem_end_index + 1)
    if solution_start_index > -1 and solution_end_index > solution_start_index:
        result.append(prob_info[solution_start_index + 1: solution_end_index])

    return result


def read_file():
    list_of_probs = []
    # Asks the user for the name of the file storing the problems (e.g., probs.txt)
    file_name = input(
        'What is the name of the file containing your practice problems: ')
    # Read the file line by line
    with open(file_name, 'r') as f:
        for line in f:
            parsed_result = parse_line(line)
            if parsed_result:
                list_of_probs.append(parsed_result)

    # Return list of problem-solution
    return list_of_probs


def incorrect_feedback(list_of_msg):
    """
    Parameter: list_of_msg is a list containing strings (the strings are messages corresponding to feedback telling the user they are not correct)
    """
    # Randomize chose the index of list of message
    pos = randint(0, len(list_of_msg) - 1)
    # return the message at that index
    return list_of_msg[pos]


def test_student(incorrect_msg, max_attempts, description, solution):
    """
    Parameters: There are 4 parameters in this function:
        -incorrect_msg_list is a list of strings that correspond to messages to show to the student if the answer is incorrect (e.g., [“Better luck next time”, “Not quite right”, “Try again!”]. It’s up to you what contents you put in this list but you should have at least 3 strings in it
        - max_attempts: this is an integer representing the max number of attempts a student has to get the answer right
        - description: this is a string that corresponds to a problem description (the problem the student is asked to solve)
        - solution: this is a string that corresponds to the solution to the problem they have to solve 

    """
    # Initialize the variable keeping track of the number of attempts to 0
    attempts = 0
    while True:
        # Increase number of attempts the did
        attempts += 1
        # Display the problem, stored in the parameter description
        print('The problem is {}'.format(description))
        # Grab the answer
        sol = input('Your answer: ')
        # and strip the answer of whitespace to make processing easier
        sol = sol.strip()
        # Compare the user’s solution to the correct one
        if sol == solution.strip():
            # If they got it right, tell them a  happy message and return True
            print('Great job!')
            return True
        elif attempts < max_attempts:
            # number of tries left
            tries_left = max_attempts - attempts
            # tell them to try again and the number of tries they have left
            print('{} You have {} tries left.'.format(
                incorrect_msg, tries_left))
        # If the number of tries exceeds the max_attempts
        elif attempts == max_attempts:
            # then tell them they are out of tries AND what the actual answer was
            print(
                'Out of tries for this one - moving on. The answer was {}'.format(solution))
            # and return False
            return False


# main code: see Main program on page 8
if __name__ == '__main__':
    # ask the user for their name, the number of tries and the problem file
    name = input('What is your name? ')
    # Welcome
    print('Welcome {} to the math cognition tutor. You will practice some standard problems.'.format(name))
    max_attempts = input(
        'How many attemps do you want to give yourself per question? ')
    try:
        # convert string to int
        max_attempts = int(max_attempts)
    except ValueError:
        print('Please enter integer number. Aborting')
        sys.exit(0)

    # initialize a variable that will keep track of how many problems they (eventually) got right to 0
    num_passed = 0
    # Incorrect messages
    incorrect_msgs = ['try again!', 'Ooops - wrong',
                      'Ooops - a typo maybe?', 'Hmm - not quite']
    list_of_probs = read_file()
    # traverse the list_of_probs returned by read_file
    for prob in list_of_probs:
        # Randomly chose incorrect message
        incorrect_msg = incorrect_feedback(incorrect_msgs)
        # call test_student with the correct parameters and store the result returned by it
        result = test_student(incorrect_msg, max_attempts, prob[0], prob[1])
        if result:
            # increase num_passed
            num_passed += 1

    # print the final result
    print('You answered: {}/{} correct'.format(num_passed, len(list_of_probs)))
