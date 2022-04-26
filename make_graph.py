import pandas as pd
import matplotlib.pyplot as plt

def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False

with open("reptile_terms.csv", "r", encoding='cp1252') as terms:
    terms.readline()
    lines = terms.readlines()


articles = []

for t in lines:
    val = t.split(',')[3].strip()
    if containsNumber(val):
        articles.append(val)

art_pd = pd.DataFrame(articles).value_counts().rename_axis('Names').reset_index(name='Counts')
art_pd = art_pd[art_pd.Counts > 1]
art_pd.loc[:,'CumulativeCount'] = art_pd.Counts.cumsum()
print(art_pd)
plt.plot(art_pd.Names, art_pd.CumulativeCount)

plt.title('Terms Found Per Paper (Cumulative)')
plt.xlabel('Paper Name')
plt.ylabel('Total Terms Found')
plt.subplots_adjust(bottom=0.5)
# plt.subplots_adjust(left=0.6)
plt.rcParams.update({'font.size': 11})

plt.xticks(rotation=90)

plt.show()
