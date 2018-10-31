import theano
import theano.tensor as T
import numpy as np
import math
import matplotlib.pyplot as plt

from matrix_creation import get_data


def cal_RMSE(prediction_M, test_ratings):
    RMSE = 0
    for rating in test_ratings:
        RMSE += (rating[2] - prediction_M[int(rating[1] - 1), int(rating[0] - 1)])**2
    RMSE = math.sqrt(RMSE / len(test_ratings))
    return RMSE

def cal_MAE(prediction_M, test_ratings):
    MAE = 0
    for rating in test_ratings:
        MAE += (rating[2] - prediction_M[int(rating[1] - 1), int(rating[0] - 1)])
    MAE = math.sqrt(MAE / len(test_ratings))
    return MAE

def train_auto(nb_epoch = 10, test_p = 0.1, nb_hunits = 10, lambda_reg = 0.001, learningrate = 0.01):
    test_ratings, train_M, nb_users, nb_movies, k = get_data()
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

    train = theano.function(
          inputs=[X, X_observed, update_matrix],
          outputs=[z2],
          updates=((V, V - learningrate * gV * update_matrix),(miu, miu - learningrate * gmiu),
              (W, W - learningrate * gW * update_matrix.T), (b, b - learningrate * gb * X_observed)))

    for j in range(nb_epoch):
        print(str(j + 1) + " epoch")
        for i in np.random.permutation(nb_movies):
            Ri = train_M[i, :]
            Ri_observed = Ri.copy()
            Ri_observed[Ri > 0] = 1
            update_m = np.tile(Ri_observed, (nb_hunits, 1))
            Ri_predicted = train(Ri, Ri_observed, update_m)
            prediction_M[i, :] = np.array(Ri_predicted)
        RMSE_list[j] = cal_MAE(prediction_M, test_ratings)

    print("training complete")
    return nb_epoch, RMSE_list

print(train_auto())
