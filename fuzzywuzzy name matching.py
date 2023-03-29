import os
import pandas as pd

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import numpy as np
os.chdir('C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data for GP Elections')
data = pd.read_excel("up_Village_Gram.xlsx")

gp_election_list = pd.read_excel("gp_election_list.xlsx")
gp_election_list  = gp_election_list['eng_match_nodist']

gp_list = data['Local Body Name'].str.lower()

fr = 0
gp_max_fr = ''
for gp in gp_list:
    
    if str(gp).lower() == 'nan':
        continue
    
    else:
        new_fr = fuzz.ratio('dabaka', gp)
        if new_fr > fr:
            gp_max_fr = gp
            fr = new_fr

