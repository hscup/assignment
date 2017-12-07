'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 18, 2015.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    numerator = 0 
    for word in vec1:
        if word in vec2:
            numerator += vec1[word] * vec2[word]
    denominator = norm(vec1) * norm(vec2)
    return numerator/denominator


def build_semantic_descriptors(sentences):
    pass

def build_semantic_descriptors_from_files(filenames):
    pass



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    pass


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    pass
