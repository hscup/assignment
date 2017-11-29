import operator
import sys

import matplotlib.pyplot as plt

from elections_2002 import *

# Constant represent number of district (it will be 81 in this case)
DISTRICT_COUNT = len(electoralDistricts)


def get_user_input():
    """
    Get user input
    Return:
        - The lower bound and upper bound threshold
        - exit if otherwise
    """
    try:
        lower_bound = int(input(
            'Please enter a lower bound for the threshold (barrage): '))
        upper_bound = int(input('Please enter an upper bound for the threshold (barrage): '))
        if 0 < lower_bound < upper_bound:
            return (lower_bound, upper_bound)
        else:
            print('You entered an invalid input!!!')
            sys.exit()

    except ValueError:
        print('Please input digit as integer number')
        sys.exit()

# This function is copied from hw3
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

def calculate_seat(threshold):
    """
    Calculate the seat distribution of each political party across the country with specific threshold

    Params:
        - threshold: the threshold

    Return:
        - A list represents number of seats for each party
    """
    
    # A political party which does not achieve that threshold across the country, 
    # does not get any seats allocated to it in any electoral district, 
    # even if it received enough votes to have some seats in some districts.
    # It means that we can assume the votes for the party which has total votes less than threshold
    # in any district to 0
    # Otherwise, we keep the original value
    assumedVoteNumbersOfParties = []
    for votes_districts in voteNumbersOfParties:
        votes = []
        for i in range(len(votes_districts)):
            # Check if the party has total votes less than threshold
            if countrywidePercentages[i] < threshold:
                votes.append(0)
            else:
                # Keep un-change
                votes.append(votes_districts[i])
        assumedVoteNumbersOfParties.append(votes)

    # Initialize the seat for every party is 0
    seats = [0] * len(partyNames)
    for i, district_deputy_number in enumerate(districtDeputyNumbers):
        seats_district = calculate_seat_district(district_deputy_number, partyNames, assumedVoteNumbersOfParties[i])
        # using Python's builtin method add from operator package
        # to sum up the total seat for each party
        seats = list(map(operator.add, seats, seats_district))

    return seats

def plot(thresholds, seats_thresholds):
    """
    plot the seats for party versus threshold
    Params:
        - threshold: list of threshold
        - seats_thresholds: a list of list contains seats for each party coresponding list of threshold (i.e. thresholds)
    """
    fig, ax = plt.subplots()
    for seats in seats_thresholds:
        ax.plot(thresholds, seats)

    ax.set(xlabel='barrage (threshold)', ylabel='Seat Number')
    ax.grid()

    # marker
    plt.legend(partyNames)

    fig.savefig("test.png")
    plt.show()

def main():
    """
    Main function
    """
    # Get the district index from user
    lower_bound, upper_bound = get_user_input()
    thresholds = range(lower_bound, upper_bound + 1)
    seats_thresholds = []
    for threshold in thresholds:
        seats = calculate_seat(threshold)
        seats_thresholds.append(seats)
        print('The result for threshold {} is {}'.format(threshold, seats))

    # matrix transpose
    # https://stackoverflow.com/questions/4937491/matrix-transpose-in-python
    seats_thresholds = [list(i) for i in zip(*seats_thresholds)]
    plot(thresholds, seats_thresholds)

    # plot
if __name__ == '__main__':
    main()
