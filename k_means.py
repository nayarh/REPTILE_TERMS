# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 15:07:28 2022

@author: nayar


"""
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import pdist
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import pickle
import sys
import seaborn as sns
sns.set()
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler




if os.path.isfile("pandas_df"):
    infile = open("pandas_df",'rb')
    mat_pd = pickle.load(infile)
    infile.close()


    plt.figure(figsize=(10, 7))
    plt.title("Reptile Genus Clusters by Feature")
    plt.xlabel('Reptile Genus')
    plt.ylabel('Euclidean Distance of Binary Terms Vectors')
    species = mat_pd.columns
    print(species)
    print(mat_pd.index)
    mat_pd_T = mat_pd.T

    f = open("Genus_Terms.txt", "w")
    f.write(mat_pd_T.to_string())
    f.close()

    scaler = StandardScaler()
    mat_pd_T = scaler.fit_transform(mat_pd_T)
    pca = PCA(n_components=62)
    pca.fit(mat_pd_T)
    scores_pca = pca.transform(mat_pd_T)

    # wcss = []
    # for i in range(1, 21):
    #     k_p = KMeans(i)
    #     k_p.fit(scores_pca)
    #     wcss.append(k_p.inertia_)
    # plt.plot(range(1,21),wcss)
    # plt.show()
    k_p = KMeans(4)
    k_p.fit(scores_pca)
    pca_k_p = pd.concat([mat_pd_T.reset_index(drop=True), pd.DataFrame(scores_pca)], axis=1)
    pca_k_p.columns.values[-3:] = ['Component1', 'Component2', 'Component3']
    pca_k_p['Segment K-Means PCA'] = k_p.labels_
    pca_k_p['Segment'] = pca_k_p['Segment K-Means PCA'].map({0: 'first',1:'second',2:'third', 3:'fourth'})

    sns.scatterplot(pca_k_p['Component1'], pca_k_p['Component3'], hue=pca_k_p['Segment'], palette=['g','r','c','m'])
    plt.show()
    # print(pca.explained_variance_ratio_)
    # plt.plot(range(1, 705), pca.explained_variance_ratio_.cumsum())
    # plt.show()


else:

    with open("reptile_terms.csv", "r", encoding='cp1252') as terms:
        lines = terms.readlines()

    abb_terms=set()
    abb_terms_2 = set()

    #putting abbreviations and terms into one set to remove repetitions
    for t in lines:


        abb_terms.add((t.split(',')[0], t.split(',')[1]))


    abb_terms = list(abb_terms)


    #Sparse Matrix
    mat = [set() for x in range(len(abb_terms))]



    #read from reptile database
    with open("reptile_database_2021_11.txt", encoding="utf_16") as f:
        species_list = []
        species_list_set = set()
        lines = []
        for line in f.readlines():

            s = line.split("\t")
            species_name = s[1]
            species_list.append(species_name)
            lines.append(line)
            species_list_set.add(species_name)

        for species_name, line in zip(species_list, lines):
            for a in abb_terms:



                #cross checking
                if a[0] in line or a[1] in line:

                    if mat[abb_terms.index(a)] is not None:
                        mat[abb_terms.index(a)].add(species_name)



                    else:
                        mat[abb_terms.index(a)] = []
                        mat[abb_terms.index(a)].add(species_name)






    species_list_set = list(species_list_set)
    mat_np = np.zeros(shape=(len(abb_terms), len(species_list_set)))
    for i in range(len(mat)):
        if mat[i]:
            for specie in mat[i]:
                mat_np[i][species_list_set.index(specie)] = 1

    abb_terms_detup = [i[1] for i in abb_terms]
    mat_pd = pd.DataFrame(mat_np,columns=species_list_set, index=abb_terms_detup)

    outfile = open("pandas_df",'wb')
    pickle.dump(mat_pd,outfile)
    outfile.close()
