# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 16:20:06 2021

@author: zboogaart
"""

import pandas as pd

df = pd.read_csv("C:/Users/zboogaart/Documents/SCANN_Lab/Web_of_science_search_results.csv")

def split_authors(author_string):
    if isinstance (author_string,str):
        return author_string.split(';')

df['author_list'] = df['Author Full Names'].apply(split_authors)

df['first_author'] = df['author_list'].apply(split_authors)

def first_author(author_list):
    if isinstance(author_list,list) and len(author_list) > 0:
        return author_list.pop(0)
    
df['first_author'] = df['author_list'].apply(first_author)

def last_author(author_list):
    if isinstance(author_list,list) and len(author_list) > 0:
        return author_list.pop(-1)
    
df['last_author'] = df['author_list'].apply(last_author)

# %%

