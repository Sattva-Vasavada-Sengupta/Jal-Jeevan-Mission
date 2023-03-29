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
os.chdir("C:/Users/LAB-14/Documents/Sattva")
test_district_data = pd.read_csv('odisha_latest.csv')

test_district_data = test_district_data[test_district_data.district == district_name.lower()].reset_index(drop = True)
 
loop_village_name_list = test_district_data['village_name'].str.lower()
loop_village_code_list = test_district_data['village_id']

# #if stopped:
#id_stopped = 402462
#index = list(loop_village_code_list).index(id_stopped)

#test_district_data = test_district_data.iloc[index + 1:]

#loop_village_name_list = test_district_data['village_name'].str.lower()
#loop_village_code_list = test_district_data['village_id']



#%%%
##Create lists to append to village data
panch_sec_list = list()
panch_sarpanch_list = list()
panch_fem_member_num_list = list()
panch_male_member_num_list = list()

ws_chairperson_list = list()
ws_mem_secretary_list = list()
ws_advisory_member_list = list()
ws_member_female_count_list = list()
ws_member_male_count_list = list()

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
    
    #Get table of GP memebrs
    time.sleep(5)
    try:
        gp_panch_table = pd.read_html(driver.page_source)[0]
    except:
        gp_panch_table = pd.DataFrame(columns = ['Name', 'Designation', 'Gender'])

    # print(gp_panch_table)    
    
    #Get panchayat secretary gender
    try:
        panch_sec = gp_panch_table[gp_panch_table.Designation == 'Panchayat Secretary']['Gender'].reset_index()['Gender'][0]
    except:
        panch_sec = 'nan'
    panch_sec_list.append(panch_sec)
    
    #Get panchayat sarpanch gender. If not in table, then nan. 
    try:
        panch_sarpanch = gp_panch_table[gp_panch_table.Designation == 'Head /Sarpanch']['Gender'].reset_index()['Gender'][0]
    except:
        panch_sarpanch = 'nan'
    panch_sarpanch_list.append(panch_sarpanch)
        
      
    #Get number of female and male members in panchayat. If not available, then by default 0.    
    panch_member_female_count =  len(gp_panch_table[(gp_panch_table.Designation == 'Gp Member') &
                                                (gp_panch_table.Gender == 'Female')])
    panch_member_male_count =  len(gp_panch_table[(gp_panch_table.Designation == 'Gp Member') &
                                                (gp_panch_table.Gender == 'Male')])
    
    panch_fem_member_num_list.append(panch_member_female_count)
    panch_male_member_num_list.append(panch_member_male_count)
    
    #Get water Samiti table. If not available, create empty df so that code ahead has no errors. 
    try:
        water_samiti_table = pd.read_html(driver.page_source)[1]
    except:
        water_samiti_table = pd.DataFrame(columns = ['Type', 'Name', 'Designation', 'Gender'])
    

    # print(water_samiti_table)    
    #Get gender of water samiti chairperson. If none shown, then nan. 
    try:
        ws_chairperson = water_samiti_table[water_samiti_table.Designation == 'Chairperson']['Gender'].reset_index()['Gender'][0]
    except:
        ws_chairperson = 'nan'
        
    ws_chairperson_list.append(ws_chairperson)
    
    #Get gender of water samiti secretary. If none shown, then nan. 
    try:
        ws_mem_secretary = water_samiti_table[water_samiti_table.Designation == 'Member Secretary']['Gender'].reset_index()['Gender'][0]
    except:
        ws_mem_secretary = 'nan'
    ws_mem_secretary_list.append(ws_mem_secretary)
    
    #Get gender of water samiti advisory member. If none shown, then nan. 
    try:
        ws_advisory_member = water_samiti_table[water_samiti_table.Designation == 'Advisory Member']['Gender'].reset_index()['Gender'][0]
    except:
        ws_advisory_member = 'nan'
    ws_advisory_member_list.append(ws_advisory_member)
    
    #Get counts of water samiti male and female members. If none shown, then by default 0. 
    try:
        ws_member_female_count = len(water_samiti_table[(water_samiti_table.Designation == 'Members') &
                                                        (water_samiti_table.Gender == 'Female')])
        ws_member_male_count = len(water_samiti_table[(water_samiti_table.Designation == 'Members') &
                                                        (water_samiti_table.Gender == 'Male')])
    except:
        ws_member_female_count = 'nan'
        ws_member_male_count = 'nan'
        
    ws_member_female_count_list.append(ws_member_female_count)
    ws_member_male_count_list.append(ws_member_male_count)
    
    #Show what village over. 
    print(village, 'over')
    
    #back button press - goes to district page after clicking. 
    click_xpath('//*[@id="aid_Back"]', 5)

    
    
temp_table = pd.DataFrame(list(zip(village_name_list, village_code_list, 
                                   panch_sec_list, panch_sarpanch_list,
                                   panch_fem_member_num_list, panch_male_member_num_list, 
                                   ws_chairperson_list, ws_mem_secretary_list,
                                   ws_advisory_member_list, ws_member_female_count_list,
                                   ws_member_male_count_list)), 
                          columns = ['village_name', 'village_id', 
                                     'p_sec', 'p_sarpanch', 
                                     'p_fem_member_count', 'p_male_member_count',
                                     'ws_chairperson', 'ws_memsec',
                                     'ws_advisory_mem', 'ws_fem_mem_count', 
                                     'ws_male_mem_count'])

temp_table = temp_table.drop_duplicates()

os.chdir("C:/Users/LAB-14/Documents/Sattva")
with open('odisha'+district_name+'_latest.pkl', 'wb') as f:
    pickle.dump(temp_table, f)
    
