import math


def norm(vec):
    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    numerator = 0
    for word in vec1:
        if word in vec2:
            numerator += vec1[word] * vec2[word]

    denominator = norm(vec1) * norm(vec2)
    return numerator / denominator


def build_semantic_descriptors(sentences):
    """
    Given a list of list of strings representing sentences, return a
    dictionary with semantic descriptors of each word.
    The semantic descriptor represents how many times the subject word and
    the other word appear in the same sentence as
    each other.

    Param:
        -sentences:  a list of list of strings, where the lists group together the words from that sentence.
    Return
        a dictionary with each word that appears in sentences as keys. The value is another dictionary with words as keys and values as the number of times the first and second keys appear in the same sentence
    """

    dictionary_count = {}

    # Make a list that contains all of the words.
    for sentence in sentences:
        # convert all sentences to a set.
        sentence = set(sentence)
        for word in sentence:
            if word not in dictionary_count:
                dictionary_count[word] = {}
            for other_word in sentence:
                if word != other_word:
                    if other_word in dictionary_count[word]:
                        dictionary_count[word][other_word] += 1
                    else:
                        dictionary_count[word][other_word] = 1

    return dictionary_count


def build_semantic_descriptors_from_files(filenames):
    text = ''
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as f:
            text += f.read()
    text = text.replace(",", " ").replace("--", " ").replace("-", " ").replace(
        ":", " ").replace(";", " ").replace('"', " ").replace("'", " ").replace("?", ".").replace(
        "!", ".").split(".")

    sentences = []
    for sentence in text:
        sentences.append(sentence.lower().split())

    return build_semantic_descriptors(sentences)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if word not in semantic_descriptors:
        return choices[0]
    best = choices[0]
    if choices[0] not in semantic_descriptors:
        max_similar = -1
    else:
        max_similar = similarity_fn(
            semantic_descriptors[word], semantic_descriptors[choices[0]])
    for i in choices[1:]:
        if i in semantic_descriptors:
            tmp = similarity_fn(
                semantic_descriptors[word], semantic_descriptors[i])
            if tmp > max_similar:
                max_similar = tmp
                best = i
    return best


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    sentences = open(filename, "r", encoding="utf-8").read().split("\n")
    counter = 0
    for sentence in sentences:
        words = sentence.split()
        word = words[0]
        ans = words[1]
        choices = words[2:]
        if most_similar_word(word, choices, semantic_descriptors, similarity_fn) == ans:
            counter += 1
    percentage = (counter / len(sentences)) * 100
    return round(percentage, 2)


if __name__ == '__main__':
    import time
    start = time.time()
    # 2 files from 2.5
    filenames = ["pg2600.txt", "pg7178.txt"]
    print('Success rate: {}%'.format(run_similarity_test("test.txt",
                              build_semantic_descriptors_from_files(filenames), cosine_similarity)))
    end = time.time()
    print('Running time: {} seconds'.format(round(end - start, 2)))
