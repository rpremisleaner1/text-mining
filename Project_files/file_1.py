# Imports
"""
To begin this project, we must first install the libraries required.
Since I am using cinemagoer, I ran "pip install cinemagoer"
"""

import imdb
import string
import pandas as pd
import plotnine
from imdb import Cinemagoer

instance = imdb.Cinemagoer()

movie_1 = instance.search_movie("War Dogs")[0]
movie_2 = instance.search_movie("21 Jump Street")[0]
movie_3 = instance.search_movie("Moneyball")[0]

print(movie_1.movieID)  # ID is 2005151
print(movie_2.movieID)  # ID is 1232829
print(movie_3.movieID)  # ID is 1210166

movie_1_id = movie_1.movieID
movie_2_id = movie_2.movieID
movie_3_id = movie_3.movieID

print(movie_1_id)

# print(movie_reviews['data']['reviews'][0]['content']) # check 'rating' as well
# print(movie_reviews['data']['reviews'][1]['content']) # transforming into a list


def list_reviews(movie_id, num_reviews):
    """
    Returns a list of N reviews given a dictionary from cinemagoer reviews. User must specify the movie ID from IMDB reviews, as well as the number of reviews wanted -- 
    this program selects the top N reviews given Cinemagoer's dataset 
    """
    final_list = []
    movie_reviews = instance.get_movie_reviews(movie_id)  # a dictionary
    for i in range(num_reviews):
        final_list.append(movie_reviews['data']['reviews'][i]['content'])
    return final_list

# print(list_reviews(movie_1_id, 5))
# print(list_reviews(movie_2_id, 5))
# print(list_reviews(movie_3_id, 5))


listed_review_1 = list_reviews(movie_1_id, 5)


def make_list():
    k = 0
    new_list = []
    for line in range(len(listed_review_1)):
        line = listed_review_1[k]
        word = line.split()
        new_list.append(word)
        # print(listed_review_1[line])
        k += 1
    return new_list


# print(make_list())
test_list = make_list()


def create_dict():
    res = {}
    for line in range(len(listed_review_1)):
        line = listed_review_1[line]
        word = line.split()
        for words in word:
            res[words] = res.get(words, 0) + 1
    return res


dict_object = create_dict()


def create_sorted_dict(a_dict):
    sorted_keys = sorted(a_dict, key=a_dict.get, reverse=True)
    sorted_dict = {}
    for key in sorted_keys:
        sorted_dict[key] = a_dict[key]
    return sorted_dict


# print(create_sorted_dict(dict_object))
sorted_dict = create_sorted_dict(dict_object)


def process_file(filename):
    """Makes a histogram that contains the words from a file.

    filename: string
    skip_header: boolean, whether to skip the Gutenberg header

    returns: map from each word to the number of times it appears.
    """
    hist = {}
    fp = open(filename, encoding='UTF8')

    strippables = string.punctuation + string.whitespace

    for line in fp:
        if line.startswith('*** END OF THIS PROJECT'):
            break

        line = line.replace('-', ' ')

        for word in line.split():
            # word could be 'Sussex.'
            word = word.strip(strippables)
            word = word.lower()

            # update the dictionary
            hist[word] = hist.get(word, 0) + 1

    return hist


def most_common(sorted_dictionary, k_words, excluding_stopwords=False):
    stopwords = process_file('data/stopwords.txt')
    lst = []
    for word, freq in sorted_dictionary.items():
        if excluding_stopwords:
            if word in stopwords:
                continue
        lst.append((freq, word))
    return lst[0:k_words]


most_common_list = most_common(sorted_dict, 5, True)
df = pd.DataFrame(most_common_list, columns = ['frequency', 'word']) # Source: https://www.geeksforgeeks.org/create-a-pandas-dataframe-from-lists/
print(df)


# if __name__ == "__main__":
#     main()
