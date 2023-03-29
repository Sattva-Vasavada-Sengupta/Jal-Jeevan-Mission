import os
import pandas as pd
import pickle 

os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/Name PKL Files")

with open('odisha_Nuapada_beneficiary_table_list.pkl', 'rb') as f:
    df = pickle.load(f)

df['Beneficiary Name'].str.split(pat = " ", expand = True)

df.groupby('Gender')['Gender'].count()
