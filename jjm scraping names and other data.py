import os
import pandas as pd
import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC

import pickle

import numpy as np
from collections import Counter

#%%%
#Global Vars
district_name = 'Kendujhar'


#%%%
os.chdir("C:/Users/savas/Documents/Ashoka/Courses/Development Economics/Dev Course Research/Data Extraction From JJM/Odisha/District-Village XHR Data")
test_district_data = pd.read_csv('odisha_latest.csv')

test_district_data = test_district_data[test_district_data.district == district_name.lower()].reset_index(drop = True)
 
loop_village_name_list = test_district_data['village_name'].str.lower()
loop_village_code_list = test_district_data['village_id']

# #if stopped:
#id_stopped = 402462
#index = list(loop_village_code_list).index(id_stopped)

# test_district_data = test_district_data.iloc[index + 1:]

# loop_village_name_list = test_district_data['village_name'].str.lower()
# loop_village_code_list = test_district_data['village_id']



#%%%
##Create lists to append to village data

panchayat_table_list = list()
ws_table_list= list()
beneficiary_table_list = list()
service_level_list = list()
scheme_table_list = list()
habitat_table_list = list()
water_source_list = list()


#Village name list, just to keep track of everything. 
village_name_list = list()
village_code_list= list()

list_zeros = [0] * len(loop_village_name_list)
village_name_counter_dict = dict(zip(loop_village_name_list, list_zeros))

#%%%

def click_xpath(xpath, sleep_time):
    try:
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
                                                                xpath))).click()
    except:
        time.sleep(sleep_time)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
                                                                xpath))).click()
        
def send_keys_xpath(xpath, sleep_time, key):
    try:
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
                                                                    xpath))).send_keys(key)
    except:
        time.sleep(sleep_time)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
                                                                    xpath))).send_keys(key)
        
#Trim list to trim lists that stopped in the middle and some rows are longer than other rows. 
def trim_list(list_name):
    list_name = list_name[:-1]
    return list_name


#%%%

url = 'https://ejalshakti.gov.in/jjmreport/JJMIndia.aspx'

options = webdriver.ChromeOptions()
options.headless = True #Dont put headless on for some time. Once code is sorted, then do headless. 
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
# options.add_argument("start-maximized")
driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)

#%%%

#If loop stops:
driver.get(url)

time.sleep(30)

state_table = pd.read_html(driver.page_source)
#Enter state
click_xpath('//*[@id="tblBody"]/tr[23]/td[1]/div[2]/a', 10)

#Click district
district_table = pd.read_html(driver.page_source)[0]
district_table.columns = district_table.columns.get_level_values(0)

index_district = np.where(district_table['District'] == district_name)[0][0] + 1

click_xpath('//*[@id="tblBody"]/tr['+str(index_district)+']/td[1]/div[2]/a', 5)

#Send village name: selecting village name
i = 1
for village, village_id in zip(loop_village_name_list, loop_village_code_list):
    print(i, village, village_id) 
    i += 1
    
    key = village
    if i == 1:
        time.sleep(10)
    else: 
        pass
    
    village_name_list.append(village)
    village_code_list.append(village_id)
    
    #Send village name: Sending keys
    send_keys_xpath('//*[@id="myInput"]', 3, key)
       
    #click on j'th village name that appears
    click_element_village = list(loop_village_name_list[:list(loop_village_code_list).index(village_id)]).count(village) + 1
    
    click_xpath('//*[@id="tbl_search"]/tbody/tr['+str(click_element_village)+']', 5)       
    
    # print('clicked')
    #####################
    
    #Get table of GP memebrs
    # time.sleep(6)
    gp_panch_table = pd.DataFrame(columns = ['Name', 'Designation', 'Gender'])
    try: 
        for df in pd.read_html(driver.page_source):
            if list(df.columns) == ['Name', 'Designation', 'Gender']:
                gp_panch_table = df
    except: 
        time.sleep(5)
        for df in pd.read_html(driver.page_source):
            if list(df.columns) == ['Name', 'Designation', 'Gender']:
                gp_panch_table = df    
        
    panchayat_table_list.append(gp_panch_table)
    
    #####################
    
    #Get water samiti table
    water_samiti_table = pd.DataFrame(columns = ['Type', 'Name', 'Designation', 'Gender'])
    
    try:
        for df in pd.read_html(driver.page_source):
            if list(df.columns) == ['Type', 'Name', 'Designation', 'Gender']:
                water_samiti_table = df
    except:
        time.sleep(5)
        for df in pd.read_html(driver.page_source):
            if list(df.columns) == ['Type', 'Name', 'Designation', 'Gender']:
                water_samiti_table = df
    
    ws_table_list.append(water_samiti_table)
    
    #####################
    
    try:
        service_level = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
                                                                                    '//*[@id="lblWaterSupplylevel"]'))).text
    except:
        service_level = 'nan'
       
    # print(service_level)
    
    #####################
    # print('1')
    #beneficiary table
    if int((WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
                                                                '//*[@id="lblHC_link"]'))).text).replace(',', '')) > 0: 
        
        click_xpath('//*[@id="form1"]/div[6]/div[5]/div/div/div/div/div[2]/div', 5)
        
        for df in pd.read_html(driver.page_source):
            if list(df.columns) == ['S.No.', 'Beneficiary Name', 'Father/Husband Name', 'Gender',
                                    'Habitation Name']:
                beneficiary_table = df
                #close beneficiary list
       
        click_xpath('//*[@id="ModelPopBenif"]/div/header/span', 3)
        
    
    else:
        beneficiary_table = pd.DataFrame()
       
    beneficiary_table_list.append(beneficiary_table) 
    
    
    
    
    #####################
    
    #scheme list  
    if int((WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
                                                                '//*[@id="lblscheme_link"]'))).text).replace(',', '')) > 0: 
        
        click_xpath('//*[@id="form1"]/div[6]/div[5]/div/div/div/div/div[3]/div', 5)
        
        for df in pd.read_html(driver.page_source):
            if 'Sanction Year' in list(df.columns):
                scheme_table = df
                #close scheme list
        click_xpath('//*[@id="ModelPop_Id"]/div/header/span', 3)
        
     
    else:
        scheme_table = pd.DataFrame()
       
    scheme_table_list.append(scheme_table) 
    
    
     
   
    
    ####################    
    
    
    #water source list
    if int(WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
                                                                '//*[@id="lblwater_sources_link"]'))).text) > 0: 
        #water source list click if num water source > 0
        click_xpath('//*[@id="form1"]/div[6]/div[5]/div/div/div/div/div[4]/div', 5)
        
        for df in pd.read_html(driver.page_source):
            if list(df.columns) == ['S.No.', 'Source Type', 'Source type category', 'Habitation Name',  'Location']:
                water_source = df
                #close water source list
        click_xpath('//*[@id="ModelPop_Id"]/div/header/span', 3)
        
    
    else:
        water_source = pd.DataFrame()
       
    water_source_list.append(water_source) #append habitat table to list. 
    
    
    ####################
    
    #check number of habitations
    if int(WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH,
                                                                '//*[@id="lblTotalHab_link"]'))).text) > 0: 
        #habitatation list
        click_xpath('//*[@id="form1"]/div[6]/div[5]/div/div/div/div/div[1]/div', 5)
        
        for df in pd.read_html(driver.page_source):
            if list(df.columns) == ['S.No.', 'Habitation Name', 'Rural population', 
                              'Households',	'Nos. of tap connections provided', 'Water Quality Status']:
                habitat_table = df
                
                #close habitat list
        click_xpath('//*[@id="ModelPop_Id"]/div/header/span', 3)
        
    
    else:
        habitat_table = pd.DataFrame()
       
    habitat_table_list.append(habitat_table) #append habitat table to list. 
    
     
    
    
    #####################
    
    #Show what village over. 
    print(village, 'over')
    
    #back button press - goes to district page after clicking. 
    # driver.execute_script("window.history.go(-1)")
    
    # driver.back()
    
    #scroll up before pressing back button. 
    try:
        driver.execute_script("window.scrollTo(0,0)")
    except:
        time.sleep(5)
        driver.execute_script("window.scrollTo(0,0)")

    click_xpath('//*[@id="aid_Back"]', 20)


#Save tables
list_names = [panchayat_table_list, ws_table_list, beneficiary_table_list, 
              service_level_list, scheme_table_list, habitat_table_list, 
              water_source_list]

os.chdir("C:/Users/LAB-14/Documents/Sattva/Name and Schemes Data")
for lst in list_names:
    temp_df = pd.DataFrame()
    for village_name, village_id, df in zip(loop_village_name_list, loop_village_code_list, lst):
        df['village_name'] = village_name
        df['village_id'] = village_id
        temp_df = pd.concat([temp_df, df], axis = 0)
        
    with open('odisha_'+district_name+'_'+lst+'.pkl', 'wb') as f:
        pickle.dump(temp_df, f)


    
