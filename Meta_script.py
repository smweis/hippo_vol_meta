# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 16:20:06 2021

@author: zboogaart
"""

import pandas as pd
import numpy as np
import os

# Assume the csv is in the directory with this script
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Web_of_science_search_results.csv')


df = pd.read_csv(filename)


def split_authors(author_string):
    if isinstance (author_string,str):
        return author_string.split(';')

df['author_list'] = df['Author Full Names'].apply(split_authors)


def first_author(author_list):
    if isinstance(author_list,list) and len(author_list) > 0:
        return author_list.pop(0)
    
df['first_author'] = df['author_list'].apply(first_author)

def last_author(author_list):
    if isinstance(author_list,list) and len(author_list) > 0:
        return author_list.pop(-1)
    
df['last_author'] = df['author_list'].apply(last_author)

# Only select articles that meet criteria (human-coded as hippocampal data)
df = df[df['Meets Criteria?'] == 'Y']

# %%
melted = pd.melt(df,id_vars=['first_author','last_author'],value_vars=['DOI'],
                    var_name='DOI')
#output_df.set_index(['first_author','last_author'],inplace=True)

author_list = melted['first_author'].unique()
author_list = np.append(author_list,melted['last_author'].unique())


output_df = pd.DataFrame(index=author_list,columns=['author','co-author','doi'])

for i in author_list:
    output_df.loc[i,'doi'] = melted[melted['first_author']==i]['value'].to_list()
    output_df.loc[i,'doi'].append(melted[melted['last_author']==i]['value'].to_list())
    output_df.loc[i,'co-author'] = melted[melted['first_author']==i]['last_author'].to_list()
    output_df.loc[i,'co-author'].append(melted[melted['last_author']==i]['last_author'].to_list())

output_df['author'] = output_df.index
output_df.reset_index(inplace=True)
output_df.drop(columns='index',inplace=True)







