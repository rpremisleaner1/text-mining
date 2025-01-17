# Imports
"""
To begin this project, we must first install the packages required.
Since I am using cinemagoer, I ran "pip install cinemagoer." I do the same for the other packages, such as nltk, pandas, plotnine, etc.
"""

from asyncio.windows_events import NULL
from tkinter import NONE
import imdb
import string
import pandas as pd
import plotnine
from plotnine import * # visualization like ggplot
from imdb import Cinemagoer
import nltk
# nltk.download('vader_lexicon') # This is needed to run the sentiment analyis
from nltk.sentiment.vader import SentimentIntensityAnalyzer

instance = imdb.Cinemagoer()

"""
The purpose of this first part of the project is to gather reviews from movies starred by my favorite actor, Jonah Hill, and do a few analysis regarding its reviews.
To do this, I begin by specifying three of my favorite movies and searching for their respective movie IDs on cinemagoer
"""

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

# print(movie_reviews['data']['reviews'][1]['content']) # transforming into a list

"""
The following chunk of code retrieves information from the top N ratings of the movies specified.
"""

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

"""
Since the list_reviews() function returns a list of words in each of the ratings, I then create a function that returns a dictionary of words and their frequencies
"""
# listed_review_1 = list_reviews(movie_1_id, 5)
# # print(list_reviews(movie_1_id, 5))
# listed_review_2 = list_reviews(movie_2_id, 5)
# listed_review_3 = list_reviews(movie_3_id, 5)

def create_dict(listed_review):
    """
    Returns a dictionary mapping words and their respective frequencies, given a list of reviews.
    """
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

"""
I eventually wanted to create a dictionary that is sort word:frquency pairs from high to low. For that, I create a function called create_sorted_dict()
"""
def create_sorted_dict(a_dict):
    """
    Returns a dictionary of sorted word:frequency pairs given a dictionary.
    """
    sorted_keys = sorted(a_dict, key=a_dict.get, reverse=True)
    sorted_dict = {}
    for key in sorted_keys:
        sorted_dict[key] = a_dict[key]
    return sorted_dict


# print(create_sorted_dict(dict_object))
# sorted_dict_1 = create_sorted_dict(dict_object_1)
# sorted_dict_2 = create_sorted_dict(dict_object_2)
# sorted_dict_3 = create_sorted_dict(dict_object_3)

"""
Now given a dictionary that is already sorted, I only need to select the top N words that I want in order to create a visualization. Nonetheless, many frequently used words would be considered stopwords.
Due to this problem, I import the stopwords.txt file and exclude the stopwords from the dictionary/histogram 
"""

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
    """
    Returns a final list of word:frequency pairs, which may exclude stopwords if specified by the user. The function is also parametrized by a sorted_dictionary, and a number of k words (k_words) to keep
    """
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

"""
I now have the data needed to create the final visualizations. However, There are times for which I want to calculate statistics, such as the mean for a certain sentiment, that requires the use of pandas.
To do that, I transform the final list into a pandas dataframe and merge the data from different movies into a single dataframe
"""

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

"""
After all this work, I am now ready to create my visualizations. I choose to use a Python library called plotnine which closely resembles both the syntax and output of GGplot, an R library that is famous for data visualization.
I first choose to create an (unordered) bar chart of the most common words in the movie reviews, colored by the respective movie names. 
"""

# print((ggplot(full_df, aes(y = 'frequency', x = 'word', fill = 'movie_name', color = 'movie_name')) # https://plotnine.readthedocs.io/en/stable/
# + geom_bar(stat = 'identity') 
# + theme(legend_position = 'bottom', legend_title = element_blank())
# + scale_y_continuous(minor_breaks = NULL)
# + labs(x = '', y = '', title = 'Frequency of Word (Y) vs. Word Name (X) by Movie Name (Colors) and Movie Name (Facets)')
# + facet_wrap('~movie_name', ncol = 3, scales = 'free_x')))


"""
A closer look at the visualizations yields the conclusion that it is not very informative. In fact, most of the words displayed are simply the author's names or words in the movie title.
Therefore, I choose to conduct a sentiment analysis on each of the reviews and see what I can infer from that. 
"""

def analyze_sentiment(listed_review):
    """
    This function takes a list of reviews and uses the SentimentIntensityAnalyzer function from nltk to derive sentiment scores for each of the reviews being analyzed. It requires that the user
    specifies a review in list format, as done in previous lines of code.
    """
    lst = []
    for line in range(len(listed_review)):
        line = listed_review[line]
        score = SentimentIntensityAnalyzer().polarity_scores(line)
        for key, value in score.items():
            lst.append((key, value))
    return lst

"""
Similar to what was done before with the other dataframes, I convert the lists to dataframes in order to plot them later. Dataframes are combined into the full_sentiment_df for plotting.
"""
# sentiment_list_1 = analyze_sentiment(listed_review_1)
# sentiment_list_2 = analyze_sentiment(listed_review_2)
# sentiment_list_3 = analyze_sentiment(listed_review_3)

# sentiment_df_1 = pd.DataFrame(sentiment_list_1, columns = ['sentiment', 'value'])
# sentiment_df_1['movie_name'] = movie_1_name

# sentiment_df_2 = pd.DataFrame(sentiment_list_2, columns = ['sentiment', 'value'])
# sentiment_df_2['movie_name'] = movie_2_name

# sentiment_df_3 = pd.DataFrame(sentiment_list_3, columns = ['sentiment', 'value'])
# sentiment_df_3['movie_name'] = movie_3_name

# intermediate_sentiment_df = sentiment_df_1.append(sentiment_df_2, ignore_index = True)
# full_sentiment_df = intermediate_sentiment_df.append(sentiment_df_3, ignore_index = True)

# print(full_sentiment_df)

# https://gist.github.com/conormm/fd8b1980c28dd21cfaf6975c86c74d07 # Source used to understand differences between R's dplyr and the manipulation of Pandas dataframes

"""
The following chunk of code calculates the mean score for each of the sentiment values given in the polarity scores output.
The mean values are then used to create a graph with the mean values on the Y axis, sentiment categories on the X axis, colored by the sentiment categories and faceted by each of the Movie Names  
"""
# full_sentiment_df_aggregated = full_sentiment_df.groupby(['movie_name', 'sentiment']).mean().reset_index()
# print(full_sentiment_df_aggregated)

# https://plotnine.readthedocs.io/en/stable/ # Source used to understand how plotnine library works
# print((ggplot(full_sentiment_df_aggregated, aes(y = 'value', x = 'sentiment', fill = 'sentiment', color = 'sentiment')) 
# + geom_bar(stat = 'identity') 
# + theme(legend_position = 'bottom', legend_title = element_blank())
# + scale_y_continuous(minor_breaks = NULL)
# + labs(x = '', y = '', title = 'Mean Sentiment Value (Y) vs. Sentiment Kind (X) by Sentiment Kind (Colors) and Movie Name (Facets)')
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
    + labs(x = '', y = '', title = 'Graph 1: Frequency of Word (Y) vs. Word Name (X) by Movie Name (Colors) and Movie Name (Facets)')
    + facet_wrap('~movie_name', ncol = 3, scales = 'free_x')))

    sentiment_list_1 = analyze_sentiment(listed_review_1)
    sentiment_list_2 = analyze_sentiment(listed_review_2)
    sentiment_list_3 = analyze_sentiment(listed_review_3)

    sentiment_df_1 = pd.DataFrame(sentiment_list_1, columns = ['sentiment', 'value'])
    sentiment_df_1['movie_name'] = movie_1_name

    sentiment_df_2 = pd.DataFrame(sentiment_list_2, columns = ['sentiment', 'value'])
    sentiment_df_2['movie_name'] = movie_2_name

    sentiment_df_3 = pd.DataFrame(sentiment_list_3, columns = ['sentiment', 'value'])
    sentiment_df_3['movie_name'] = movie_3_name

    intermediate_sentiment_df = sentiment_df_1.append(sentiment_df_2, ignore_index = True)
    full_sentiment_df = intermediate_sentiment_df.append(sentiment_df_3, ignore_index = True)

    full_sentiment_df_aggregated = full_sentiment_df.groupby(['movie_name', 'sentiment']).mean().reset_index()

    print((ggplot(full_sentiment_df_aggregated, aes(y = 'value', x = 'sentiment', fill = 'sentiment', color = 'sentiment')) # https://plotnine.readthedocs.io/en/stable/
    + geom_bar(stat = 'identity') 
    + theme(legend_position = 'bottom', legend_title = element_blank())
    + scale_y_continuous(minor_breaks = NULL)
    + labs(x = '', y = '', title = 'Graph 2: Mean Sentiment Value (Y) vs. Sentiment Kind (X) by Sentiment Kind (Colors) and Movie Name (Facets)')
    + facet_wrap('~movie_name', ncol = 3, scales = 'free_x')))



if __name__ == "__main__":
    main()
