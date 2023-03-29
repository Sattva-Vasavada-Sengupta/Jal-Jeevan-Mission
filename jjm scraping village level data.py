import os
import pandas as pd

import requests 
import json

from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC

import re



url = 'https://ejalshakti.gov.in/jjmreport/JJMIndia.aspx'

options = webdriver.ChromeOptions()
options.headless = True #Dont put headless on for some time. Once code is sorted, then do headless. 
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)


driver.get(url)

def get_xhr_list(driver):
    xhr = []
    for r in driver.requests:
        if r.headers.get('X-Requested-With'): 
            driver.wait_for_request(r.path)
            xhr.append(r)

    for x in xhr:
        print(x)
        
get_xhr_list(driver)

driver.find_element(By.ID, 'lblchk_toggles').click()

get_xhr_list(driver)
 
url_req = 'https://ejalshakti.gov.in/jjmreport/JJMIndia.aspx/BindDistrictMap'
myobj = {'DtCode11': 2511, 'StCode11': "1%3A1",  'Cat': 11, 'SubCat': 11, 'Param': 11}

x = requests.post(url_req, json = myobj)
print(x.text)


#%%%

#Subtracting string from another string example. 
text_1 = "string_test"
text_2 = "s"

if text_2 in text_1:
    text_1 = text_1.replace(text_2, "")

#%%%

#Processing text: Step 1: Get raw village data

text = x.text
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
        text = text.replace(village_raw, "")
        
        #When last village reached
        if len(text) < 250:
            #Wait one time before breaking
            if breaker > 0:
                break
            else:
                #One time counter. Once else block reached, then entire loop breaks the next time. 
                breaker += 1
        #Keep count of loops to see where errors arise.        
        print(i)
        i += 1
        
#%%%


key_value_list = list()
key_id_list = list()
name_list = list() 
percent_list = list() 
color_id_list = list() 
value_list = list() 
total_list = list() 
lat_list = list() 
long_list = list() 

for village_raw in village_raw_list:
    key_value = re.search(r'\"KeyValue\"\:\"(.*?)\"', village_raw).group(1)
    key_value_list.append(key_value)
    
    key_id = re.search(r'\"KeyId\"\:\"(.*?)\"', village_raw).group(1)
    key_id_list.append(key_id)
    
    name = re.search(r'\"Name\"\:\"(.*?)\"', village_raw).group(1) 
    name_list.append(name)
    
    percent = re.search(r'\"Per\"\:\"(.*?)\"', village_raw).group(1)
    percent_list.append(percent)
    
    color_id = re.search(r'\"ColorId\"\:\"(.*?)\"', village_raw).group(1)
    color_id_list.append(color_id)
    
    value = re.search(r'\"Value\"\:\"(.*?)\"', village_raw).group(1)
    value_list.append(value)
    
    total = re.search(r'\"Total\"\:\"(.*?)\"', village_raw).group(1)
    total_list.append(total)
    
    lat = re.search(r'\"Lat\"\:\"(.*?)\"', village_raw).group(1)
    lat_list.append(lat)
    
    long = re.search(r'\"Long\"\:\"(.*?)\"', village_raw).group(1)
    long_list.append(long)
            
    

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
        









