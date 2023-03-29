import os
import pandas as pd
import pickle
import re
import collections

#%%%

os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/Panch WS Extraction/Temp Files")
file_list = ['odishaBalangir']
filename = 'balangir'
    
data = pd.DataFrame()

for file in file_list:
    with open(file+'.pkl', 'rb') as f:
        temp_df = pickle.load(f)
        
    data = pd.concat([data, temp_df], axis = 0)

os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/Panch WS Extraction/Final District files")
data.to_csv('odisha_'+filename+'_gp_ws_scraping.csv')



#%%%

os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/District-Village XHR Data")
odisha_latest = pd.read_csv('odisha_latest.csv')

#%%%
#Merge csv xhr data with csv scraped data
os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/Panch WS Extraction/Final District files")
file_list = os.listdir()
i = 1
for file in file_list:
    os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/Panch WS Extraction/Final District files")
    # print(i)
    i += 1
    file_data = pd.read_csv(file)
    
    dist_name = re.search(r'odisha_(.*?)_gp', file).group(1)
    # print(dist_name)
    odisha_dist = odisha_latest[odisha_latest.district == dist_name]
    odisha_dist['village_name'] = odisha_dist['village_name'].str.lower()
    # print(len(odisha_dist))
    merged_data = pd.merge(odisha_dist, file_data, on = ['village_id', 'village_name'])
    merged_data = merged_data[merged_data.village_id != 0]
    print(dist_name, len(odisha_dist), len(merged_data))
    merged_data['district'] = dist_name


    #given our merged data, we need to fuzzy matching to clean the dataset
    

    os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/XHR Panch WS Merged")
    merged_data.to_csv("odisha_"+dist_name+"_2022_xhr_panch_merged.csv")   

#%%%
#all merged data into one big file.
os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/XHR Panch WS Merged")
file_list = os.listdir()
file_list = file_list[1:]

temp_df = pd.DataFrame()

for file in file_list:
    file_data = pd.read_csv(file)
    
    temp_df = pd.concat([temp_df, file_data], axis = 0)

temp_df.drop_duplicates(subset = ['village_name', 'village_id'], inplace = True)

os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/XHR Panch WS Merged/Main File")
temp_df.to_csv('odisha_2022_merged_main.csv')

#%%%

#merge main merged file with lgd 

#read merged file
os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/XHR Panch WS Merged/Main File")
merged_file = pd.read_csv('odisha_2022_merged_main.csv')

#read lgd
os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/LGD")
lgd = pd.read_excel('odisha_village_gp_mapping.xlsx')

#main mergiing
lgd_main_merge = pd.merge(merged_file, lgd, left_on = 'village_id', right_on = 'Village Code', how = 'left')
os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/LGD, Census merge")
lgd_main_merge.to_csv('odisha_lgd_merged.csv')

test = pd.merge(merged_file, lgd, left_on = 'village_id', right_on = 'Village Code', how = 'inner')
#difference in length: 79 villages not matched. 


setdiff = set((set(lgd_main_merge['village_name']) - set(test.village_name)))

#lgd columns are nan when left merged with orignal jjm data. 

#%%%
set(lgd['District Name'])

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import copy

fuzz_ratio = 0
def fuzzymatch(village_name, district_name):
    lgd['District Name'] = (lgd['District Name']).str.lower()
    df = lgd[lgd['District Name'] == district_name.lower()]
    # print(df.head(5))
    temp = 0
    for village, village_id in zip(df['Village Name'], df['Village Code']):
        
        village = village.lower()
        fuzz_ratio = fuzz.ratio(village_name, village) 
        if fuzz_ratio > temp:
            temp = fuzz_ratio    
            high_village = village
            high_village_id = village_id
            high_fuzz_ratio = fuzz_ratio
            row_append = df[(df['Village Code'] == high_village_id)]

            # print(fuzz_ratio, high_village_id)
            
    # try: 
    #     row_append = df[(df['Village Code'] == high_village_id)]
    # except: 
    #     print('error', village_name, district_name, len(df))
    #     row_append = ''
    
    # print(fuzz_ratio, high_fuzz_ratio, high_village, high_village_id)
    return row_append


test = fuzzymatch('lehedi', 'sundargarh')
fuzzymatch('liakhai', 'JHARSUGUDA')

fuzzymatch('gudiali', 'JHARSUGUDA')
fuzzymatch('goindola', 'JHARSUGUDA')

fuzzymatch('tinginimal', 'JHARSUGUDA')
fuzzymatch('semilia', 'JHARSUGUDA')

fuzzymatch('banjipali', 'JHARSUGUDA')
fuzzymatch('banjara', 'JHARSUGUDA')

fuzzymatch('manapali', 'SAMBALPUR')
fuzzymatch('mahulpali', 'SAMBALPUR')

fuzzymatch('ramtal(kusamura r.f.', 'SAMBALPUR')
fuzzymatch('nuabarangamal', 'SAMBALPUR')

#%%%

#in our JJM main file: df where there are no duplicates
merged_file_no_dup = merged_file.drop_duplicates('village_id', keep = False)

#
lgd_merge_no_dup = pd.merge(merged_file_no_dup, lgd, left_on = 'village_id', right_on = 'Village Code', how = 'left')

#in our JJM main: df where there are duplicates.
merged_file_dup = merged_file[merged_file.duplicated('village_id', keep = False)]
merged_file_dup['duplicate_matching_id'] = list(range(0, len(merged_file_dup)))

collections.Counter(lgd['District Name']) 

collections.Counter(merged_file_dup['district'])

for district in set(lgd['District Name'].str.lower()):
    if district in list(set(merged_file_dup['district'])):
        continue
    else:
        print(district)

lgd_to_merge_dup = pd.DataFrame()
list_village_name = list()

i = 0
for village, village_id, district_name in zip(merged_file_dup['village_name'],
                                         merged_file_dup['village_id'], 
                                         merged_file_dup['district']):
    if district_name == 'balasore':
        district_name = 'baleshwar'
    elif district_name == 'jajpur':
        district_name = 'jajapur'
    elif district_name == 'khurda':
        district_name = 'khordha'
    elif district_name == 'subarnapur': 
        district_name = 'sonepur'
    elif district_name == 'nabarangapur': 
        district_name = 'nabarangpur' 
    elif district_name == 'angul':
        district_name = 'anugul'
    elif district_name == 'debagarh':
        district_name = 'deogarh'
    
    row = fuzzymatch(village, district_name)
    # print(row['Village Name'])
    lgd_to_merge_dup = pd.concat([lgd_to_merge_dup, row], axis = 0)
    # print(village)
    list_village_name.append(village)
    
    
 
lgd_to_merge_dup['old_village_name'] =  list_village_name
lgd_to_merge_dup['duplicate_matching_id'] = list(range(0, len(lgd_to_merge_dup)))

lgd_merge_with_dup = pd.merge(merged_file_dup, lgd_to_merge_dup,
                              on = 'duplicate_matching_id', how = 'left')

test = copy.deepcopy(lgd_merge_with_dup)
test1 = test[['village_id', 'village_name', 'Village Code', 'Village Name']]

os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/LGD, Census merge")
test1.to_csv('check fuzzy matching_jjm and lgd village names.csv')

lgd_merge_with_dup.drop(['old_village_name', 'duplicate_matching_id'], axis = 1, inplace = True)

#drop old village id column and create new one (or rename Village Code - from LGD). 
#wait wait, do not drop old village_id column. It may change the positioning of columns which may
#disrupt the appending/concat process. 
lgd_merge_with_dup['village_id'] = lgd_merge_with_dup['Village Code']


lgd_final_cleaned_merge = pd.concat([lgd_merge_no_dup, lgd_merge_with_dup], 
                                    axis = 0)

os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/LGD, Census merge")
lgd_final_cleaned_merge.to_csv('odisha_lgd_merged_cleaned.csv')

#%%%
#Searching for more duplicates
dup_in_lgd_merge_no_dup = lgd_merge_no_dup[lgd_merge_no_dup.duplicated('village_id', keep = False)]

dup_in_lgd_merge_with_dup = lgd_merge_with_dup[lgd_merge_with_dup.duplicated('village_id', keep = False)]

dup_in_lgd_final_cleaned_merge = lgd_final_cleaned_merge[lgd_final_cleaned_merge.duplicated('village_id', keep = False)]

#%%%

#merging lgd_main_merge with census 2001 2011 data for odisha. 
os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Odisha Census Data")
census = pd.read_stata('odisha_census_01_11.dta')
census['vill_code_11_extract'] = census['vill_code_11'].str.extract('(\d+)') 

census['vill_code_11_extract'] = census['vill_code_11_extract'].astype(int)

#was using leg_main_merge before. Now using lgd_final_cleaned_merge. 
census_lgd_main_merge = pd.merge(lgd_final_cleaned_merge, census, left_on = 'Village Census 2011 Code', 
                                 right_on = 'vill_code_11_extract', how = 'left')
os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/LGD, Census merge")
census_lgd_main_merge.to_csv('odisha_census_lgd_merged.csv')



#%%%

