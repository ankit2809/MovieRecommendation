import nltk
import numpy as np
import pandas as pd
import mysql.connector 

#nltk.download(["punkt","stopwords","wordnet"])


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="********"
)

movies_sql = "select tb.titleid as movieid, tb.originalTitle as title, tb.titleType, tb.startYear, tb.genres from imdb.titleratings tr, imdb.titlebasics tb where tr.averageRating >=8 and tr.titleid=tb.titleid and tr.numVotes > 10000 and tb.genres != 'None'"
movies = pd.read_sql_query(movies_sql,mydb)


from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
genres = movies["genres"]
li=[]
for i in range(len(genres)):
    temp = genres[i].lower()
    temp = temp.split(",")
    temp = [lemmatizer.lemmatize(word) for word in temp]
    li.append(" ".join(temp))



movies_dataset = pd.DataFrame(li,columns=["genres"],index=movies["title"])

#Finding based on similar movies
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(movies_dataset["genres"]).toarray()


'''
print("Count Vector : \n",X)
print("\nNote: First row of above count vector: ",X[0])
print("\nColumns Coresponding to above count vector is :\n",cv.get_feature_names())
'''

output = movies.loc[:,['movieid','title']]
output = output.join(pd.DataFrame(X))



#Row corresponds to a movie name
from sklearn.metrics.pairwise import cosine_similarity

similarities = cosine_similarity(X) 
#Each row of matrix coressponds to similarity of a movie with all other movies (row len = 10329)

watched_sql = "select titleid from imdb.watchedcontent where watched='y' and recommended IS NULL"
watched_content = pd.read_sql_query(watched_sql,mydb)

for content in watched_content["titleid"]:

    #we need index but we are using id to find which row is crct in similarities matrix
    latest_movieId_watched_by_user = content #watched_content["titleid"][0]
    movie_index = movies.loc[movies['movieid']==latest_movieId_watched_by_user,["title"]].index[0]
    similarity_values = pd.Series(similarities[movie_index])

    #We converted list into series in order to preserve the actual indexes of dataset even after sorting
    similarity_values.sort_values(ascending=False)

    similar_movie_indexes = list(similarity_values.sort_values(ascending=False).index)

    #Remove the already watched movie from index list
    similar_movie_indexes.remove(movie_index)

    '''
    def get_movie_by_index(idx):
        return movies_dataset.index[idx]
    def get_movie_by_id(mv_id):
        return movies.loc[movies['movieid']==mv_id,['title']].values[0][0]
    get_movie_by_id(latest_movieId_watched_by_user)

    print("Since u watched --->",get_movie_by_id(latest_movieId_watched_by_user),"<--- We recommend you")
    for i in range(5):
        print(get_movie_by_index(similar_movie_indexes[i]))
    '''

    value = '"'
    for i in range(4):
        #list.append(output.iloc[similar_movie_indexes[i],0])
        value = value + str(output.iloc[similar_movie_indexes[i],0]) + ','
    value = value + str(output.iloc[similar_movie_indexes[5],0]) + '"'

    recommendation_sql = "update imdb.watchedcontent set recommended =" + value +" where titleid = " + str(latest_movieId_watched_by_user)
    cur = mydb.cursor()
    cur.execute(recommendation_sql)
    mydb.commit()
    cur.close()