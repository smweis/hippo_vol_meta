# -*- coding: utf-8 -*-

import pandas as pd
import os

# Assume the csv is in the directory with this script
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Web_of_science_search_results.csv')

# Read in the web of science coded CSV
df = pd.read_csv(filename)

# Split authors on semi-colons (and spaces to remove leading split)
def split_authors(author_string):
    if isinstance (author_string,str):
        return author_string.split(';')


#Assign author_list
df['author_list'] = df['Author Full Names'].apply(split_authors)


# Only select articles that meet criteria (human-coded as hippocampal data)
df = df[df['Meets Criteria?'] == 'Y']

# %%
# Find corresponding author using Reprint Addresses column by splitting using 'corresponding author' tag
def split_corresponding_authors(author_string):
    if isinstance (author_string,str):
        return author_string.split(' (corresponding author), ')

#Assigning another df to make changes
df1 = df.copy()

#Splitting Reprint Addresses
df1['address_list'] = df1['Reprint Addresses'].apply(split_corresponding_authors)

# taking out the first element of the split caused above
def temp_corr_author(address_list):
    if isinstance(address_list,list) and len(address_list) > 0:
        return address_list.pop(0)
    
df1['temp_corresponding_author'] = df1['address_list'].apply(temp_corr_author)

# splitting the above result again to take care of cases where multiple names are present before the split
def corr_author_split(temp_corresponding_author):
    if isinstance (temp_corresponding_author,str):
        return temp_corresponding_author.split('; ')
    
df1['corresponding_author_split'] = df1['temp_corresponding_author'].apply(corr_author_split)

#taking the last name present in the split as the corresponding author
def corr_author(corresponding_author_split):
    if isinstance(corresponding_author_split,list) and len(corresponding_author_split) > 0:
        return corresponding_author_split.pop(-1)

df1['corresponding_author'] = df1['corresponding_author_split'].apply(corr_author)

#splitting email addresses to get email id
def email_split(Email_Addresses):
    if isinstance (Email_Addresses,str):
        return Email_Addresses.split('; ')

df1['email_addresses'] = df1['Email Addresses'].apply(email_split)

def corr_email(email_addresses):
    if isinstance(email_addresses,list) and len(email_addresses) > 0:
        return email_addresses.pop(-1)
    
df1['corresponding_email'] = df1['email_addresses'].apply(corr_email)


# %%
# This creates new dataframe used to create the relevant csv file

corresponding_author_list = df1['corresponding_author'].unique()

author_series = pd.Series(corresponding_author_list).unique()

output1_df = pd.DataFrame(index=corresponding_author_list,columns=['corres_author','co-author','doi','title','corresponding_author_email'])


for i in author_series:
    output1_df.loc[i,'doi'] = df1[df1['corresponding_author']==i]['DOI'].to_list()
    
    output1_df.loc[i,'title'] = df1[df1['corresponding_author']==i]['Article Title'].to_list()
    
    output1_df.loc[i,'co-author'] = df1[df1['corresponding_author']==i]['author_list'].to_list()
    
    output1_df.loc[i,'corresponding_author_email'] = df1[df1['corresponding_author']==i]['corresponding_email'].to_list()

        
output1_df['corres_author'] = output1_df.index
output1_df.reset_index(inplace=True)
output1_df.drop(columns='index',inplace=True)

#output csv file
output1_df.to_csv(r'output_search_results.csv',index=False)