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
    invmapping_subj={}
    c=0
    filew=open('subj_id_mapping.txt','w')
    for d in data:
        studs.add(d)
        for dd in data[d]:
            if int(data[d][dd]['semester'])!=0 and int(data[d][dd]['semester'])<=8:
                subjs.add(dd)
                if dd not in mapping_subj:
                    mapping_subj[dd]=c
                if c not in invmapping_subj:
                    invmapping_subj[c]=dd
                c=len(subjs)
    for m in mapping_subj:
        filew.write(str(m)+"\t"+str(mapping_subj[m])+"\n")
    filew.close()


    train_matrix=np.zeros((len(studs), len(subjs)))
    test_matrix=np.zeros((len(studs), len(subjs)))
    train_data={}
    test_data={}
    subj_sem_mapping={}

    filew=open('subj_sem_mapping.txt','w')
    maxx={}
    for d in data:
      
        for dd in data[d]:
               
                if dd in mapping_subj:
                    if mapping_subj[dd] not in subj_sem_mapping:
                        subj_sem_mapping[mapping_subj[dd]]=set()
                    if (d-1,mapping_subj[dd]) not in maxx:
                        maxx[(d-1,mapping_subj[dd])]=0
                    if int(data[d][dd]['grade'])>maxx[(d-1,mapping_subj[dd])]:
                        maxx[(d-1,mapping_subj[dd])]=int(data[d][dd]['grade'])
                
                if int(data[d][dd]['semester'])!=0 and int(data[d][dd]['semester'])>=5 and int(data[d][dd]['semester'])<=8:
                    subj_sem_mapping[mapping_subj[dd]].add(int(data[d][dd]['semester']))                
                
               
                      
     
    for d in data:
      
        if d>=517:
            for dd in data[d]:
                          
                if dd in mapping_subj:
                    if int(data[d][dd]['semester']) in [5,6,7,8]:               
                        if (d-1,mapping_subj[dd]) not in test_data and len(subj_sem_mapping[mapping_subj[dd]])!=0:
                            test_data[(d-1,mapping_subj[dd])]=maxx[(d-1,mapping_subj[dd])]
                            test_matrix[d-1,mapping_subj[dd]]=maxx[(d-1,mapping_subj[dd])]
                            test_grades.append((d-1,mapping_subj[dd],maxx[(d-1,mapping_subj[dd])]))
                    else:
                        if (d-1,mapping_subj[dd]) not in train_data and len(subj_sem_mapping[mapping_subj[dd]])!=0:
                            train_data[(d-1,mapping_subj[dd])]=maxx[(d-1,mapping_subj[dd])]
                            train_matrix[d-1,mapping_subj[dd]]=maxx[(d-1,mapping_subj[dd])]
                            train_grades=train_grades+1

        else:
            for dd in data[d]:
                if dd in mapping_subj:
                        
                    if (d-1,mapping_subj[dd]) not in train_data and len(subj_sem_mapping[mapping_subj[dd]])!=0:
                        train_data[(d-1,mapping_subj[dd])]=maxx[(d-1,mapping_subj[dd])]
                        train_matrix[d-1,mapping_subj[dd]]=maxx[(d-1,mapping_subj[dd])]
                        train_grades=train_grades+1

    for s in subj_sem_mapping:
        if len(subj_sem_mapping[s])!=0:
            filew.write(str(s)+"\t"+str(list(subj_sem_mapping[s]))+"\n")
    filew.close()

    # filew=open("data/own_train.txt",'w')
    # for item in train_data:
    #     filew.write(str(item[0])+"\t"+str(item[1])+"\t"+str(train_data[item])+"\n")
    # filew.close()

    # filew=open("data/own_test.txt",'w')
    # for item in test_data:
    #     filew.write(str(item[0])+"\t"+str(item[1])+"\t"+str(test_data[item])+"\n")
    # filew.close()

    return train_matrix, test_matrix, train_grades, test_grades, train_data, test_data, train_matrix.shape[0],train_matrix.shape[1]

get_data()

# max grade taken
# sem only <=8
# 5 6 7 8 sems taken ft test set