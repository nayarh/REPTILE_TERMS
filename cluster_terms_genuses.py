# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 15:07:28 2022

@author: nayar


"""
import numpy
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import pdist
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import pickle
import sys
import seaborn as sns
from sklearn.preprocessing import StandardScaler





if os.path.isfile("pandas_df"):
    infile = open("pandas_df",'rb')
    mat_pd = pickle.load(infile)
    infile.close()


    plt.figure(figsize=(10, 7))
    plt.title("Reptile Genus Clusters by Feature")
    plt.xlabel('Reptile Genus')
    plt.ylabel('Jaccard Similarity of Binary Terms Vectors')
    species = mat_pd.columns
    mat_pd_T = mat_pd.T

    #c_dist = pdist(mat_pd_T) # computing the distance
    c_link = linkage(mat_pd_T,  metric='jaccard', method='complete')# computing the linkage
    t = 0.7*max(c_link[:,2])
    clusters = fcluster(c_link, t, criterion="distance")

    ugh = {}
    for c in set(clusters):
        ugh[c] = []
        for i, cluster in enumerate(clusters):
            if cluster == c:
                ugh[c].append(species[i])
    species_small = []
    for u in ugh.keys():
        species_small.append(ugh[u][0])
    ss = mat_pd_T.loc[species_small]
    print(ss)
    c_link = linkage(ss,  metric='jaccard', method='complete')# computing the linkage
    print(c_link)
    plt.subplots_adjust(bottom=0.2)


    B=dendrogram(c_link, labels=ss.index)


    ss_unique = ss.loc[:, (ss != ss.iloc[0]).any()]
    ss_unique = ss.loc[:, ss.std() > .3]

    normalized_df=(ss_unique-ss_unique.mean())/ss_unique.std()
    normalized_df = normalized_df.fillna(0)
    g = sns.clustermap(ss_unique)
    g.fig.subplots_adjust(right=0.7)
    g.fig.subplots_adjust(bottom=0.35)

    g.ax_cbar.set_position((0.8, .2, .03, .4))

    plt.show()
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
    mat_np = numpy.zeros(shape=(len(abb_terms), len(species_list_set)))
    for i in range(len(mat)):
        if mat[i]:
            for specie in mat[i]:
                mat_np[i][species_list_set.index(specie)] = 1

    mat_pd = pd.DataFrame(mat_np,columns=species_list_set, index=abb_terms)

    outfile = open("pandas_df",'wb')
    pickle.dump(mat_pd,outfile)
    outfile.close()
