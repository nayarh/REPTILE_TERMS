# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 15:07:28 2022

@author: nayar

creating a matrix of terms and abbreviations and cross checking it with the diffrent species
they are associated to in relation to data curated in the reptile database
"""

#read csv 
#read database text file 
#run terms against database to save species and terms 

with open("reptile_terms.csv", "r") as terms:
    lines = terms.readlines(0)

abb_terms=set()



#putting abbreviations and terms in separate lists
for t in lines:
    
    
    abb_terms.add(t.split(',')[0])       #retrieving abbreviations of terms
    abb_terms.add(t.split(',')[1])       #retrieving terms
    
abb_terms = list(abb_terms)



#Sparse Matrix
mat = [None] * len(abb_terms)

#read from reptile database
with open("reptile_database_2021_11.txt", encoding="utf_16") as f:
    for line in f.readlines():
        s = line.split("\t")
        species_name = s[1] + " " + s[2]
        for a in abb_terms:
            
            #cross checking with the species in the database
            if a in line:
                if mat[abb_terms.index(a)] is not None:
                    mat[abb_terms.index(a)].append(species_name)
                else:
                    mat[abb_terms.index(a)] = []
                    mat[abb_terms.index(a)].append(species_name)
                    
                    
                    
abb_terms_name = input("What abbreviation or term?:")
print(mat[abb_terms.index(abb_terms_name)])
