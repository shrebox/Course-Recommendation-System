import matrix_creation

import pandas as pd
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
import operator
import numpy as np

def csv_reader(filename):
	return pd.read_csv(filename,sep='\t',header=None)

def create_pivot_matrix(train_data):
	return train_data.pivot(index='User', columns='Movie', values='Rating').reset_index(drop=True)

def mean_rating(user_movies_matrix,user):
	counta = suma = 0
	aa = user_movies_matrix[user].tolist()
	for i in range(len(aa)):
		suma+=aa[i]
		if aa[i]>0:
			counta+=1
	meanadd = suma/counta
	return meanadd
# def getr(summy,count):
# 	return ((summy/float(count))-0.1)
def mean_rating2(user_movies_matrix,user):
	counta = suma = 0
	aa = user_movies_matrix[user].tolist()
	for i in range(len(aa)):
		suma+=aa[i]
		counta+=1
	meanadd = suma/counta
	return meanadd	

# files = [1,2,3,4,5]
kvals = [10,20,30,40,50]

for k_index in range(len(kvals)):
	print "\n"
	print "K value: " + str(kvals[k_index])
	avg_mae=0

	test_grades, train_matrix, train_matrix_shape0,train_matrix_shape1,train_grades = matrix_creation.get_data()
	user_movies_matrix = train_matrix
	matrix_val = cosine_similarity(train_matrix)
	user_similarity_matrix = pd.DataFrame(matrix_val)

	summy = count = 0
	for ind in range(len(test_grades)):
		try:
	# if count>4000:
			count+=1
			user = test_grades[ind][0]
			movie = test_grades[ind][1]
			rating = test_grades[ind][2]

			similar_users_list = user_similarity_matrix[user].tolist()

			# print "1"
			simdic = {}
			for i in range(len(similar_users_list)):
				simdic[i] = similar_users_list[i]
			sorted_sim = sorted(simdic.items(), key=operator.itemgetter(1),reverse=True)

			topk = []
			sum_weights = 0

			#----------------------co-rated users--------------------------------
			# ks = kvals[k_index]
			# inlop = 1
			# while(ks>0):
			# 	temp_user = sorted_sim[inlop][0]
			# 	inlop+=1
			# 	# print "count, inlop: "+str(count)+" "+str(inlop)
			# 	# print temp_user,movie
			# 	if user_movies_matrix[temp_user][movie]>0 and inlop<len(sorted_sim):
			# 		topk.append(sorted_sim[inlop])
			# 		sum_weights+=sorted_sim[inlop][1]
			# 		ks-=1
			# 		if count%1000==0:
			# 			print count, temp_user, movie, len(topk)

			# -----------------without cor-rated users----------------------------
			for i in range(kvals[k_index]):
				topk.append(sorted_sim[i+1])
				sum_weights+=sorted_sim[i+1][1]
			# print "2"
			adjust_weights = []
			ratings = []
			for i in range(len(topk)):
				uid = topk[i][0]
				vid = topk[i][1]
				adjust_weights.append(vid/sum_weights)

				# ------------------base shift and scale shit normalization---------------
				maxy = -9999999
				miny = 9999999
				ratt = np.array(user_movies_matrix[uid])
				for i in range(len(ratt)):
					if ratt[i]>maxy:
						maxy = ratt[i]
					if ratt[i]<miny:
						miny = ratt[i]
				normalized_rat = (user_movies_matrix[uid][movie]-miny)/(maxy-miny)
				# normalized_rat = user_movies_matrix[uid][movie]

				meanadd = mean_rating2(user_movies_matrix,uid)
				ratings.append(normalized_rat-meanadd)

			# print adjust_weights
			# print ratings
			# break
			# print "3"
			# zip_val = zip(ratings,adjust_weights)
			# zip_val = []
			p_rating = 0
			for i in range(len(ratings)):
				# zip_val.append((ratings[i],adjust_weights[i]))
				p_rating+=ratings[i]*adjust_weights[i]
			# p_rating = sum([x*y for x,y in zip_val])
			
			# counta = suma = 0
			# aa = user_movies_matrix[user].tolist()
			# for i in range(len(aa)):
			# 	suma+=aa[i]
			# 	if aa[i]>0:
			# 		counta+=1
			# meanadd = suma/counta

			meanadd = mean_rating(user_movies_matrix,user)
			# meanadd = mean_item_rating(user_movies_matrix,user)
			summy+=abs(meanadd+p_rating-rating)
			# print "4"
		# else:
			# 	count+=1
		except Exception,e:
			print "Exception: "+ str(e)
			break


	print summy/float(count)
	avg_mae+= summy/float(count)

