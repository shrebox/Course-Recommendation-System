import pickle
import numpy as np


def get_data():
    with open('train_dic_with_sem.pkl','rb') as f:
        data=pickle.load(f)

    test_grades=[]
    train_grades=0
    studs=set()
    subjs=set()
    mapping_subj={}
    c=0
    for d in data:
        studs.add(d)
        for dd in data[d]:
            subjs.add(dd)
            if dd not in mapping_subj:
                mapping_subj[dd]=c
                c=c+1

    train_matrix=np.zeros((len(studs), len(subjs)))
    test_matrix=np.zeros((len(studs), len(subjs)))
    train_data={}
    test_data={}

    for d in data:
        if d>=636:
            for dd in data[d]:
                
                if int(data[d][dd]['semester']) in [5,6,7,8]:
                    if (d-1,mapping_subj[dd]) not in test_data:
                        test_data[(d-1,mapping_subj[dd])]=int(data[d][dd]['grade'])
                    test_matrix[d-1,mapping_subj[dd]]=int(data[d][dd]['grade'])
                    test_grades.append((d-1,mapping_subj[dd],int(data[d][dd]['grade'])))
                else:
                    if (d-1,mapping_subj[dd]) not in train_data:
                        train_data[(d-1,mapping_subj[dd])]=int(data[d][dd]['grade'])
                    train_matrix[d-1,mapping_subj[dd]]=int(data[d][dd]['grade'])
                    train_grades=train_grades+1

        else:
            for dd in data[d]:
                    
                if (d-1,mapping_subj[dd]) not in train_data:
                    train_data[(d-1,mapping_subj[dd])]=int(data[d][dd]['grade'])
                train_matrix[d-1,mapping_subj[dd]]=int(data[d][dd]['grade'])
                train_grades=train_grades+1

    # filew=open("own_train.txt",'w')
    # for item in train_data:
    #     filew.write(str(item[0])+"\t"+str(item[1])+"\t"+str(train_data[item])+"\n")
    # filew.close()

    # filew=open("own_test.txt",'w')
    # for item in test_data:
    #     filew.write(str(item[0])+"\t"+str(item[1])+"\t"+str(test_data[item])+"\n")
    # filew.close()

    return train_matrix, test_matrix, train_grades, test_grades, train_data, test_data, train_matrix.shape[0],train_matrix.shape[1]
