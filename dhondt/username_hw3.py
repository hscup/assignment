import operator
import sys

from elections_2002 import *

# Constant represent number of district (it will be 81 in this case)
DISTRICT_COUNT = len(electoralDistricts)


def get_user_input():
    """
    Get user input
    Return:
        - The district index if the inputted value in range 0-80
        - None if otherwise
    """
    try:
        district = input(
            'Please enter an index between 0 and 80 (both are inclusive): ')
        # convert to integer
        district = int(district)
        # Check if the inputted value is in range 0-80
        if 0 <= district < DISTRICT_COUNT:
            return district
        else:
            print('You entered an invalid input!!!')
            sys.exit()

    except ValueError:
        print('Please input digit as integer number')
        sys.exit()


def calculate_seat_district(district_deputy_number, parties, votes):
    """
    Calculate seats for each party in list of parties for a district

    Params:
        - district_deputy_number: the number of seats for this district 
        - parties: list of parties
        - votes: list of votes for each party in this district
    Assume that parties and votes parameters have the same size

    Return:
        - A tuple represents number of seats for each party. This tuple has same size with parameter 'parties'
    """
    party_count = len(parties)
    # Each party has been initially allocated 0 seat
    # Initialize a list with initial value is 0
    # For example, if party_count = 5
    # seats will be seats = [0, 0, 0, 0, 0]
    seats = [0] * party_count

    # N value for each party
    # N= V/(s + 1)
    # Init N as a copy of votes list
    N = votes[:]
    while sum(seats) < district_deputy_number:
        # Get the maximum value in list of N value and the index of that maximum value
        # Note: this below line uses the Python's builtin operator
        max_index, max_value = max(enumerate(N), key=operator.itemgetter(1))
        
        # Update the seats list
        # increase the seat of the party that has maximum by 1
        seats[max_index] += 1
        # Update the lagest N with new value
        # using the formal: N= V/(s + 1)
        N[max_index] = votes[max_index] / (seats[max_index] + 1)

    # return as tuple
    # Note: It can be returned as list, however, the tuple is better because it's immutable
    return tuple(seats)


def main():
    """
    Main function
    """
    # Get the district index from user
    district_index = get_user_input()
    district_deputy_number = districtDeputyNumbers[district_index]
    votes = voteNumbersOfParties[district_index]
    seats = calculate_seat_district(district_deputy_number, partyNames, votes)
    # Print the output
    print('Results for {} as follows:'.format(electoralDistricts[district_index]))
    for i in range(0, len(partyNames)):
        print('{}: {}'.format(partyNames[i], seats[i]))

if __name__ == '__main__':
    main()
