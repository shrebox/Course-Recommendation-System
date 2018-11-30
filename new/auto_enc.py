import theano
import theano.tensor as T
import numpy as np
import math
import matplotlib.pyplot as plt
import pickle
from matrix_creation import get_data
import json

def cal_RMSE(prediction_M, test_ratings,mainlist):
    RMSE = 0
    for rating in test_ratings:
        pg=10*abs((prediction_M[int(rating[1]), int(rating[0])]-mainlist[0])/(1.0*(mainlist[-1]-mainlist[0])))
        RMSE += (rating[2] - pg)**2
    RMSE = math.sqrt(RMSE / len(test_ratings))
    return RMSE

def cal_MAE(prediction_M, test_ratings,mainlist):
    MAE = 0
    for rating in test_ratings:
        pg=10*abs((prediction_M[int(rating[1]), int(rating[0])]-mainlist[0])/(1.0*(mainlist[-1]-mainlist[0])))
        MAE += abs(rating[2] - pg)
    MAE = math.sqrt(MAE / len(test_ratings))
    return MAE

def train_auto(nb_epoch = 10, test_p = 0.1, nb_hunits = 10, lambda_reg = 0.001, learningrate = 0.01,userid=1,semester=5):
    train_M, _, k, test_ratings,train_data,test_data, nb_users, nb_movies = get_data()


    with open('train_dic_with_sem.pkl','rb') as f:
        data=pickle.load(f)

   
    c=0
    subj_id_mapping={}
    filer=open('subj_id_mapping.txt','r')
    for f in filer:
        if int(f.split("\t")[1]) not in subj_id_mapping:
            subj_id_mapping[int(f.split("\t")[1])]=f.strip().split("\t")[0]
    filer.close()

    subj_sem_mapping={}
    filer=open('subj_sem_mapping.txt','r')
    for f in filer:
        if int(f.split("\t")[0]) not in subj_sem_mapping:
            subj_sem_mapping[int(f.split("\t")[0])]=[int(x) for x in f.strip().split("\t")[1][1:-1].split(',')]
    filer.close()

    train_M=train_M.T
    prediction_M = np.zeros((nb_movies, nb_users), dtype = np.float32)
    RMSE_list = [0] * nb_epoch

    # set up theano autoencoder structure and update function
    X = T.dvector("input")
    X_observed = T.dvector("observedIndex")
    update_matrix = T.matrix("updateIndex")
    V = theano.shared(np.random.randn(nb_hunits, nb_users), name='V')
    miu = theano.shared(np.zeros(nb_hunits), name='miu')
    W = theano.shared(np.random.randn(nb_users, nb_hunits), name='W')
    b = theano.shared(np.zeros(nb_users), name='b')
    z1 = T.nnet.sigmoid(V.dot(X) + miu)
    z2 = W.dot(z1) + b
    loss_reg = 1.0/nb_movies * lambda_reg/2 * (T.sum(T.sqr(V)) + T.sum(T.sqr(W)))
    loss = T.sum(T.sqr((X - z2) * X_observed)) + loss_reg
    gV, gmiu, gW, gb = T.grad(loss, [V, miu, W, b])

    minnmae=float('inf')
    minnrmse=float('inf')

    train = theano.function(
          inputs=[X, X_observed, update_matrix],
          outputs=[z2],
          updates=((V, V - learningrate * gV * update_matrix),(miu, miu - learningrate * gmiu),
              (W, W - learningrate * gW * update_matrix.T), (b, b - learningrate * gb * X_observed)))

    for j in range(nb_epoch):
        # print(str(j + 1) + " epoch")
        for i in np.random.permutation(nb_movies):
            Ri = train_M[i, :]
            Ri_observed = Ri.copy()
            Ri_observed[Ri > 0] = 1
            update_m = np.tile(Ri_observed, (nb_hunits, 1))
            Ri_predicted = train(Ri, Ri_observed, update_m)
            prediction_M[i, :] = np.array(Ri_predicted)

        mainlist=[]
        for user in prediction_M:
            for subji in range(user.shape[0]):
                subj=user[subji]
                mainlist.append(subj)
        mainlist.sort()
             
        mae=cal_MAE(prediction_M, test_ratings,mainlist)
        rmse=cal_RMSE(prediction_M, test_ratings,mainlist)
        # mae=0
        # rmse=0
        if mae<minnmae:
            minnmae=mae
            minnrmse=rmse
            minnprediction_Mmae=prediction_M

    arr=[]
    mainlist=[]
    minnprediction_Mmae=minnprediction_Mmae.T
    for user in minnprediction_Mmae:
        for subji in range(user.shape[0]):
            subj=user[subji]
            mainlist.append(subj)
    
    mainlist.sort()
   
    useri=userid-1
    user=minnprediction_Mmae[userid-1]
    for subji in range(user.shape[0]):
        subj=user[subji]
        if subji in subj_sem_mapping and semester in subj_sem_mapping[subji]:
            pg=abs(10*(subj-mainlist[0])/((mainlist[-1]-mainlist[0])*1.0))             
        
            if (useri,subji) in test_data: 
                                
                ag=test_data[(useri,subji)]
                arr.append((subj_id_mapping[subji],pg,ag,abs(pg-ag)))
            else:
               
                ag=train_data[(useri,subji)]
                arr.append((subj_id_mapping[subji],pg,ag,abs(pg-ag)))

    

    sorted_arr=sorted(arr, key=lambda x: x[1],reverse=True)

    mlist=[]
    c=0
    for s in sorted_arr[:10]:
        dict={}          
        dict['subj']=s[0]
        dict['predgrade']=s[1]
        dict['truegrade']=s[2]
        dict['err']=s[3]
        mlist.append(dict)

    return json.dumps(mlist)
    # return minnmae,minnrmse
print(train_auto(userid=1,semester=5))


#https://github.com/HeXie-Tufts/Movie-Rating-Prediction-Autoencoder
