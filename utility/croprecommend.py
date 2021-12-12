import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm


# cosine similarity evaluation

def cosine_similarity(list_1, list_2):
    cos_sim = dot(list_1, list_2) / (norm(list_1) * norm(list_2))
    return cos_sim


# organsing the data

def getdata(df, item1, item2):

    df1 = df[df['label'] == item1]
    df2 = df[df['label'] == item2]
    df1_use = df1.drop(['label'], axis=1)
    df2_use = df2.drop(['label'], axis=1)

    return df1_use, df2_use


# calculating the similarity score

def getsimscore(col_list, df, item1, item2):

    df1_use, df2_use = getdata(df, item1, item2)
    cosine_sim_score = []
    for index in range(len(col_list)):
        cosine_sim_score.append(cosine_similarity(df1_use[col_list[index]],
                                                  df2_use[col_list[index]]))

    return np.average(cosine_sim_score)


# running the code

def runcode(df):
    crop_list = list(df['label'].unique())
    col_list = list(df.columns)[:-1]
    finalmappings = {}

    for index in range(len(crop_list)):

        tempsimscore = {}

        for index1 in range(len(crop_list)):

            if crop_list[index] != crop_list[index1]:

                tempsimscore[crop_list[index1]] = round(getsimscore(
                    col_list, df, crop_list[index], crop_list[index1]), 3)

                tempsimscore = dict(
                    sorted(tempsimscore.items(), key=lambda x: x[1], reverse=True)[:6])

        finalmappings[crop_list[index]] = tempsimscore

    return finalmappings


# def getresults(crop):

#     string = 'https://en.wikipedia.org/wiki/'+crop
#     page = requests.get(string)
#     page.encoding = 'utf-8'
#     page = page.text
#     textlist = []
#     soup = BeautifulSoup(page, 'html.parser')
#     for content in soup.find_all("p"):
#         textlist.append(content.get_text())

#     textlist = [i for i in textlist if len(i) > 1]
#     return textlist[:1]

#     croplist = list(df['label'].unique())
#     croplist = [i.capitalize() for i in croplist]

#     completemap = {}
#     for crop in croplist:
#         completemap[crop] = getresults(crop)

#     completemap
