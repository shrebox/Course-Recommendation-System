import json
import numpy as np

from lightfm import LightFM
from lightfm.datasets import fetch_movielens
from lightfm.evaluation import precision_at_k, auc_score
from scipy import sparse

from sklearn.metrics import mean_squared_error
from math import sqrt

import matrix_creation

loss_functions = ['warp','logistic']
for kk in range(len(loss_functions)):
	print "Loss function: " + str(loss_functions[kk])
	avg_auc = 0
	avg_nmae = 0
	avg_rmse = 0
	
	train_data_matrix, test_data_matrix, train_grades, test_grades, train_data, test_data, train_matrix_shape0,train_matrix_shape1 = matrix_creation.get_data()

	model = LightFM(loss=loss_functions[kk])
	model.fit(sparse.csr_matrix(train_data_matrix), epochs=30, num_threads=2)

	test_precision = precision_at_k(model,sparse.csr_matrix(test_data_matrix), k=5).mean()

	print "AUC score:" + str(auc_score(model,sparse.csr_matrix(test_data_matrix)).mean())
	avg_auc+=auc_score(model,sparse.csr_matrix(test_data_matrix)).mean()

	predict_dic = {}
	pred_rat_dic = {}
	for ione in range(len(test_data_matrix)):
		temp = []
		rtemp = []
		for ito in range(len(test_data_matrix[ione])):
			if test_data_matrix[ione][ito]!=0:
				temp.append(ito)
				rtemp.append(test_data_matrix[ione][ito])
		if len(temp)>0:
			predict_dic[ione] = temp
			pred_rat_dic[ione] = rtemp

	final_pred = []
	final_groud = []
	for k,v in predict_dic.iteritems():
		predited_array = model.predict(k,v)
		gold_array = pred_rat_dic[k]
		for ii in range(len(predited_array)):
			final_pred.append(predited_array[ii])
			final_groud.append(gold_array[ii])

	sumval = 0
	countval = 0
	sumrmse = 0
	flag=0
	for ii in range(len(final_pred)):
		grnd_val = final_groud[ii]
		if grnd_val!=0:
			countval+=1
	for ii in range(len(final_pred)):
		pred_val = final_pred[ii]
		grnd_val = final_groud[ii]
		flag+=1
		if grnd_val!=0:
			sumval+=abs(pred_val-grnd_val)
			sumrmse+=((pred_val-grnd_val)*(pred_val-grnd_val))/(countval*1.0)

	flag=0
	print sumval/(countval*1.0*2), sqrt(sumrmse)
	avg_rmse+= sqrt(sumrmse)
	avg_nmae+= sumval/(countval*1.0*2)
	# rms = sqrt(mean_squared_error(final_groud,final_pred))

	# print rms
	print ""
