# Imports
"""
To begin this project, we must first install the libraries required.
Since I am using cinemagoer, I ran "pip install cinemagoer"
"""

from asyncio.windows_events import NULL
from tkinter import NONE
import imdb
import string
import pandas as pd
import plotnine
from plotnine import * # visualization like ggplot
from imdb import Cinemagoer

instance = imdb.Cinemagoer()

# movie_1_name = "War Dogs"
# movie_2_name = "21 Jump Street"
# movie_3_name = "Moneyball"

# movie_1 = instance.search_movie(movie_1_name)[0]
# movie_2 = instance.search_movie(movie_2_name)[0]
# movie_3 = instance.search_movie(movie_3_name)[0]

# print(movie_1.movieID)  # ID is 2005151
# print(movie_2.movieID)  # ID is 1232829
# print(movie_3.movieID)  # ID is 1210166

# movie_1_id = movie_1.movieID
# movie_2_id = movie_2.movieID
# movie_3_id = movie_3.movieID

# print(movie_1_id)

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


# listed_review_1 = list_reviews(movie_1_id, 5)
# listed_review_2 = list_reviews(movie_2_id, 5)
# listed_review_3 = list_reviews(movie_3_id, 5)

def create_dict(listed_review):
    res = {}
    for line in range(len(listed_review)):
        line = listed_review[line]
        word = line.split()
        for words in word:
            res[words] = res.get(words, 0) + 1
    return res


# dict_object_1 = create_dict(listed_review_1)
# dict_object_2 = create_dict(listed_review_2)
# dict_object_3 = create_dict(listed_review_3)


def create_sorted_dict(a_dict):
    sorted_keys = sorted(a_dict, key=a_dict.get, reverse=True)
    sorted_dict = {}
    for key in sorted_keys:
        sorted_dict[key] = a_dict[key]
    return sorted_dict


# print(create_sorted_dict(dict_object))
# sorted_dict_1 = create_sorted_dict(dict_object_1)
# sorted_dict_2 = create_sorted_dict(dict_object_2)
# sorted_dict_3 = create_sorted_dict(dict_object_3)


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


# most_common_list_1 = most_common(sorted_dict_1, 5, True)
# most_common_list_2 = most_common(sorted_dict_2, 5, True)
# most_common_list_3 = most_common(sorted_dict_3, 5, True)

# df_1 = pd.DataFrame(most_common_list_1, columns = ['frequency', 'word']) # Source: https://www.geeksforgeeks.org/create-a-pandas-dataframe-from-lists/
# df_1['movie_name'] = movie_1_name

# df_2 = pd.DataFrame(most_common_list_2, columns = ['frequency', 'word'])
# df_2['movie_name'] = movie_2_name

# df_3 = pd.DataFrame(most_common_list_3, columns = ['frequency', 'word'])
# df_3['movie_name'] = movie_3_name

# intermediate_df = df_1.append(df_2, ignore_index = True)
# full_df = intermediate_df.append(df_3, ignore_index = True)


# print(df_1)
# print(df_2)
# print(df_3)
# print(full_df)


# print((ggplot(full_df, aes(y = 'frequency', x = 'word', fill = 'movie_name', color = 'movie_name')) # https://plotnine.readthedocs.io/en/stable/
# + geom_bar(stat = 'identity') 
# + theme(legend_position = 'bottom', legend_title = element_blank())
# + scale_y_continuous(minor_breaks = NULL)
# + labs(x = '', y = '', title = 'Frequency of Word (Y) vs. Word Name (X) by Movie Name (Colors) and Movie Name (Facets)')
# + facet_wrap('~movie_name', ncol = 3, scales = 'free_x')))


def main():
    movie_1_name = "War Dogs"
    movie_2_name = "21 Jump Street"
    movie_3_name = "Moneyball"

    movie_1 = instance.search_movie(movie_1_name)[0]
    movie_2 = instance.search_movie(movie_2_name)[0]
    movie_3 = instance.search_movie(movie_3_name)[0]

    movie_1_id = movie_1.movieID
    movie_2_id = movie_2.movieID
    movie_3_id = movie_3.movieID

    listed_review_1 = list_reviews(movie_1_id, 5)
    listed_review_2 = list_reviews(movie_2_id, 5)
    listed_review_3 = list_reviews(movie_3_id, 5)

    dict_object_1 = create_dict(listed_review_1)
    dict_object_2 = create_dict(listed_review_2)
    dict_object_3 = create_dict(listed_review_3)

    sorted_dict_1 = create_sorted_dict(dict_object_1)
    sorted_dict_2 = create_sorted_dict(dict_object_2)
    sorted_dict_3 = create_sorted_dict(dict_object_3)

    most_common_list_1 = most_common(sorted_dict_1, 5, True)
    most_common_list_2 = most_common(sorted_dict_2, 5, True)
    most_common_list_3 = most_common(sorted_dict_3, 5, True)

    df_1 = pd.DataFrame(most_common_list_1, columns = ['frequency', 'word']) # Source: https://www.geeksforgeeks.org/create-a-pandas-dataframe-from-lists/
    df_1['movie_name'] = movie_1_name

    df_2 = pd.DataFrame(most_common_list_2, columns = ['frequency', 'word'])
    df_2['movie_name'] = movie_2_name

    df_3 = pd.DataFrame(most_common_list_3, columns = ['frequency', 'word'])
    df_3['movie_name'] = movie_3_name

    intermediate_df = df_1.append(df_2, ignore_index = True)
    full_df = intermediate_df.append(df_3, ignore_index = True)

    print((ggplot(full_df, aes(y = 'frequency', x = 'word', fill = 'movie_name', color = 'movie_name')) # https://plotnine.readthedocs.io/en/stable/
    + geom_bar(stat = 'identity') 
    + theme(legend_position = 'bottom', legend_title = element_blank())
    + scale_y_continuous(minor_breaks = NULL)
    + labs(x = '', y = '', title = 'Frequency of Word (Y) vs. Word Name (X) by Movie Name (Colors) and Movie Name (Facets)')
    + facet_wrap('~movie_name', ncol = 3, scales = 'free_x')))

# if __name__ == "__main__":
#     main()
