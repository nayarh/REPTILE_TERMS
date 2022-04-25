# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 15:07:28 2022

@author: nayar


"""

#read csv 
#read database text file 
#run terms against database to save species and terms 

outfile = open("Terms_Species.txt", "a+", encoding="utf_16")

with open("ReptileTerms_V2.csv", "r") as terms:
    lines = terms.readlines(0)

abb_terms=set()
abb_terms_2 = set()

#putting abbreviations and terms into one set to remove repetitions 
for t in lines:
    
    
    #abb_terms.add(t.split(',')[0])
    #abb_terms.add(t.split(',')[2])
    #abb_terms.add(t.split(',')[3])
    abb_terms.add(t.split(',')[4])
    
abb_terms = list(abb_terms)
# print(abb_terms)
# quit()

#Sparse Matrix
mat = [None] * len(abb_terms)



#read from reptile database
with open("reptile_database_2021_11.txt", encoding="utf_16") as f:
    for line in f.readlines():
        s = line.split("\t")
        species_name = s[1] + " " + s[2]
        for a in abb_terms:
            
            
            
            #cross checking 
            if a in line:
                
                if mat[abb_terms.index(a)] is not None:
                    mat[abb_terms.index(a)].append(species_name)
                    
                    
                    
                else:
                    mat[abb_terms.index(a)] = []
                    mat[abb_terms.index(a)].append(species_name)
                    
                   
                    
                    

for a in abb_terms:
    if a!= "TERM" and mat[abb_terms.index(a)] is not None :
        outfile.write(str(a).upper() + "\n" + "\t" + str(mat[abb_terms.index(a)]) +"\n")
              
                
outfile.close()                   
            
                    
          


# abb_terms_name = input("What abbreviation or term?:")
# print(abb_terms_name,mat[abb_terms.index(abb_terms_name)])

#outfile.write(str(a) + "\t" + str(mat[abb_terms.index(a)]))
