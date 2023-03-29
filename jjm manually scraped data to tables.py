import os
import pandas as pd
import re

os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/Raw XHR District Level Data")
dist_list = os.listdir()

key_value_list = list()
key_id_list = list()
name_list = list() 
percent_list = list() 
color_id_list = list() 
value_list = list() 
total_list = list() 
lat_list = list() 
long_list = list() 
    


village_cleaned_df = pd.DataFrame(list(zip(key_value_list, key_id_list, 
                                           name_list, percent_list, 
                                           color_id_list, value_list,
                                           total_list, lat_list,
                                           long_list)),
               columns =['village_id', 'key_id', 
                         'village_name', 'tap_perc_hh',
                         'color_id', 'num_hh',
                         'total_hh', 'latitude', 
                         'longitude'])

for dist in dist_list:
    
    if re.search("2019", dist):
        print("no", dist)
        continue
    else:
        
        print(dist)
        dist_list = list()
        key_value_list = list()
        key_id_list = list()
        name_list = list() 
        percent_list = list() 
        color_id_list = list() 
        value_list = list() 
        total_list = list() 
        lat_list = list() 
        long_list = list() 
        
        
        # print(dist)
        with open(dist) as f:
            text = f.read()
        
        dist = re.search(r'(.*?)_2022.txt', dist).group(1)
        
        i = 1
        breaker = 0
        village_raw_list = list()
        while True:
                #Get raw village data by taking substring contained within brackets.
                village_raw = str(re.search(r'\{(.*?)\}', text).group(1))
                village_raw = "{" + village_raw + "}," #add brakects and comma to make it easier to subtract 
                
                #Append village data to villag raw list
                village_raw_list.append(village_raw)
                
                #Replace orginal data. 
                if len(text) > 400:
                    text = text.replace(village_raw, "")
                
                else: 
                    village_raw = village_raw[:-1]
                    text = text.replace(village_raw, "")
                #When last village reached
                if len(text) < 400:
                    #Wait one time before breaking
                    if breaker > 0:
                        break
                    else:
                        #One time counter. Once else block reached, then entire loop breaks the next time. 
                        breaker += 1
                #Keep count of loops to see where errors arise.        
                # print(i)
                i += 1
            
    
        for village_raw in village_raw_list:
            
            dist_list.append(dist)
            
            try:
                key_value = re.search(r'\"KeyValue\"\:\"(.*?)\"', village_raw).group(1)
            except:
                # print(village_raw)
                key_value = re.search(r'KeyValue(.*?)\,KeyId', village_raw).group(1)
                # print(key_value)
            key_value_list.append(int(key_value))
            
            try:
                key_id = re.search(r'\"KeyId\"\:\"(.*?)\"', village_raw).group(1)
            except:
                key_id = re.search(r'KeyId(.*?)\,', village_raw).group(1)
            key_id_list.append(key_id)
            
            try:
                name = re.search(r'\"Name\"\:\"(.*?)\"', village_raw).group(1) 
            except:
                name = re.search(r'Name(.*?)\,', village_raw).group(1)
            name_list.append(name)
            
            try:
                percent = re.search(r'\"Per\"\:\"(.*?)\"', village_raw).group(1)
            except:
                percent = re.search(r'Per(.*?)\,', village_raw).group(1)
            percent_list.append(percent)
            
            try:
                color_id = re.search(r'\"ColorId\"\:\"(.*?)\"', village_raw).group(1)
            except:
                color_id = re.search(r'ColorId(.*?)\,', village_raw).group(1)
                
            color_id_list.append(color_id)
            
            try:
                value = re.search(r'\"Value\"\:\"(.*?)\"', village_raw).group(1)
            except:
                value = re.search(r'\,Value(.*?)\,', village_raw).group(1)
                
            value_list.append(value)
            
            try:
                total = re.search(r'\"Total\"\:\"(.*?)\"', village_raw).group(1)
            except:
                total = re.search(r'Total(.*?)\,', village_raw).group(1)
            total_list.append(total)
            
            try:
                lat = re.search(r'\"Lat\"\:\"(.*?)\"', village_raw).group(1)
                lat_list.append(lat)
            except:
                lat_list.append('nan')
            
            try:
                long = re.search(r'\"Long\"\:\"(.*?)\"', village_raw).group(1)
                long_list.append(long)
            except:
                long_list.append('nan')
                    
            
        temp_df = pd.DataFrame(list(zip(key_value_list, key_id_list, 
                                                   name_list, percent_list, 
                                                   color_id_list, value_list,
                                                   total_list, lat_list,
                                                   long_list, dist_list)),
                       columns =['village_id', 'key_id', 
                                 'village_name', 'tap_perc_hh',
                                 'color_id', 'num_hh',
                                 'total_hh', 'latitude', 
                                 'longitude', 'district'])
        
        
    
        village_cleaned_df = pd.concat([village_cleaned_df, temp_df], axis = 0)
        
#Convert datframe to csv 
os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/District-Village XHR Data")
village_cleaned_df.to_csv('odisha_latest.csv')

# os.chdir('C:/Users/savas/Documents/Ashoka/Economics/IGIDR/Mission Antyodaya/Data/Scrapped_Data/Goverment Directory')
# village_gram_dir = pd.read_excel('up_Village_Gram.xlsx')

#Merge gp-vilage dir with the dataframe
# merge_dir_jjm = pd.merge(village_cleaned_df, village_gram_dir, left_on= 'village_id', right_on= 'Village_Code')

#Save merged file. 
# os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Merged Data")
# merge_dir_jjm.to_csv("dir_jjm_merge_latest.csv")



        