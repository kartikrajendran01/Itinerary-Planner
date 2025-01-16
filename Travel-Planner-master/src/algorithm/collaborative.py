import numpy as np
import pandas as pd
import scipy.sparse
import json
from math import sqrt
from math import isnan
from scipy.stats import pearsonr

data = pd.read_csv(r"D:\BE\Project\Final\Travel-Planner-master\src\data\n_data.csv")
placeInfo = pd.read_csv(r"D:\BE\Project\Final\Travel-Planner-master\src\data\t_data.csv")

with open(r"D:\BE\Project\Final\Travel-Planner-master\src\data\district_wise_places.json") as r:
    district_places = json.loads(r.read())

userIds = data.userId
userIds2 = data[['userId']]

data.loc[0:10, ['userId']]
data = pd.DataFrame.sort_values(data, ['userId', 'itemId'], ascending=[0, 1])


def favoritePlace(activeUser, N):
    topPlace = pd.DataFrame.sort_values(
        data[data.userId == activeUser], ['rating'], ascending=[0])[:N]
    return list(topPlace.title)


userItemRatingMatrix = pd.pivot_table(data, values='rating',
                                      index=['userId'], columns=['itemId'])


def similarity(user1, user2):             #used to find th smiliarty betwen users asbed common item sand rating
    try:
        user1 = np.array(user1)
        user2 = np.array(user2)
        commonItemIds = [i for i in range(
            len(user1)) if user1[i] > 0 and user2[i] > 0]
        if len(commonItemIds) < 2:
            if(len(commonItemIds) == 1):
                return ((user1[commonItemIds[0]]-np.nanmean(user1))*(user2[commonItemIds[0]]-np.nanmean(user2)))/(sqrt(((user1[commonItemIds[0]]-np.nanmean(user1))**2)+((user2[commonItemIds[0]]-np.nanmean(user2))**2)))
            return 0

        else:
            user1 = np.array([user1[i] for i in commonItemIds])
            user2 = np.array([user2[i] for i in commonItemIds])
            if(~(((user1 != user1[0]).any()) & ((user2 != user2[0]).any()))):
                return 0
            sim, p_val = pearsonr(user1, user2)
            return sim
    except ZeroDivisionError:
        print("You can't divide by zero!")


def nearestNeighbourRatings(activeUser, K, places):
    try:
        similarityMatrix = pd.DataFrame(
            index=userItemRatingMatrix.index, columns=['Similarity'])
        for i in userItemRatingMatrix.index:
            similarityMatrix.loc[i] = similarity(
                userItemRatingMatrix.loc[activeUser], userItemRatingMatrix.loc[i])
        similarityMatrix = pd.DataFrame.sort_values(
            similarityMatrix, ['Similarity'], ascending=[0])
        nearestNeighbours = similarityMatrix
        neighbourItemRatings = userItemRatingMatrix[places].loc[nearestNeighbours.index]
        predictItemRating = pd.DataFrame(index=places, columns=['Rating'])
        for i in places:
            predictedRating = 0
            num = 0
            summ = 0
            for j in neighbourItemRatings.index:
                if userItemRatingMatrix.loc[j, i] > 0:
                    predictedRating += (
                        userItemRatingMatrix.loc[j, i])*nearestNeighbours.loc[j, 'Similarity']
                    summ += nearestNeighbours.loc[j, 'Similarity']
                    num += 1
                    if(num == K):
                        break
            if(summ == 0):
                summ = 1
            predictItemRating.loc[i, 'Rating'] = predictedRating/summ
    except ZeroDivisionError:
        print("You can't divide by zero!")
    return predictItemRating


def topNRecommendations(activeUser, N, places, watched):
    try:
        predictItemRating = nearestNeighbourRatings(activeUser, 10, places)
        placeAlreadyWatched = list(userItemRatingMatrix[places].loc[activeUser]
                                   .loc[userItemRatingMatrix[places].loc[activeUser] > 0].index)
        if(watched == True):
            predictItemRating = predictItemRating.drop(placeAlreadyWatched)
        topRecommendations = pd.DataFrame.sort_values(predictItemRating,
                                                      ['Rating'], ascending=[0])[:N]
        topRecommendationTitles = placeInfo.loc[[
            i-1 for i in topRecommendations.index]]
    except ZeroDivisionError:
        print("You can't divide by zero!")
    return topRecommendationTitles


def RecommentedPlaces(districts, userid, no, watched):
    places = set()
    for district in districts:
        places = places.union(set(district_places[district]))
    places = list(places)
    # print("The recommended places for you are: ")
    result = topNRecommendations(userid, no, places, watched)
    return result

# activeUser=int(input("Enter userid: "))
# districts=list(input().split(','))
# no=int(input())
# RecommentedPlaces(districts,activeUser,no,False)
