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

# Read in the web of science coded CSV
df = pd.read_csv(filename)

# Split authors on semi-colons (and spaces to remove leading split)
def split_authors(author_string):
    if isinstance (author_string,str):
        return author_string.split('; ')

#Assign author_list
df['author_list'] = df['Author Full Names'].apply(split_authors)

# Create lists of first and last authors
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

# This creates the dataframe from which we will generate emails

author_list = df['first_author'].unique()
author_list = np.append(author_list,df['last_author'].unique())

author_series = pd.Series(author_list).unique()

output_df = pd.DataFrame(index=author_series,columns=['author','co-author','doi','co-author_list','title'])


for i in author_series:
    output_df.loc[i,'doi'] = df[df['first_author']==i]['DOI'].to_list()
    output_df.loc[i,'doi'].extend(df[df['last_author']==i]['DOI'].to_list())
    
    output_df.loc[i,'title'] = df[df['first_author']==i]['Article Title'].to_list()
    output_df.loc[i,'title'].extend(df[df['last_author']==i]['Article Title'].to_list())
    
    output_df.loc[i,'co-author'] = df[df['first_author']==i]['last_author'].to_list()
    output_df.loc[i,'co-author'].extend(df[df['last_author']==i]['first_author'].to_list())
    
    output_df.loc[i,'co-author'] = list(filter(None,output_df.loc[i,'co-author']))

    try:
        output_df.loc[i,'co-author_list'] = set(output_df.loc[i,'co-author'])
    except:
        print(output_df.loc[i,'co-author'])
        
output_df['author'] = output_df.index
output_df.reset_index(inplace=True)
output_df.drop(columns='index',inplace=True)







