#!/usr/bin/env python
# coding: utf-8

# In[3]:


from selenium import webdriver
import time
import requests
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
from csv import writer
import json
session = webdriver.Chrome()
session.maximize_window()
language = 'English'
Profile = 0
session.get("https://pureportal.coventry.ac.uk/en/organisations/centre-global-learning/persons/")
time.sleep(10)
session.find_element(By.XPATH,"//button[@id='onetrust-accept-btn-handler']").click()
for j in range(0 , 1):
        urls = []
        base_url = "https://pureportal.coventry.ac.uk/en/organisations/centre-global-learning/persons/?page=%d"%(j)
        session.get(base_url)
#         time.sleep(1)
        b = session.current_url
        b1 = requests.get(b)
        resp=BeautifulSoup(b1.text,"html.parser")
        title_3 = resp.find(class_ = 'grid-results')
        title_4 = title_3.find_all('h3') # User details
        for h in title_4:
            resh_3 = h.find('a')
            resh_4 = resh_3['href'] # each research paper
            urls.append(resh_4)

        for k in urls:
            
            tag = k + '/fingerprints'
            session.get(tag)
#             time.sleep(1)
            b = session.current_url
            ab = requests.get(b)
            resp1=BeautifulSoup(ab.text,"html.parser")
#             title3 = resp1.find(class_ = 'stacked-trend-widget large')            
#             if(title3 != None):
            head = resp1.find(class_='header person-details')
            h = head.find('h1').get_text()
            Desig = head.find_all('div')
            Designation = []
            Designation_1 = resp1.find(class_='rendering rendering_person rendering_persontitlerendererportal rendering_person_persontitlerendererportal')
            if (Designation_1 != None):
                de = Designation_1.find('p').get_text()
                Designation.append(de)
            else:
                time.sleep(0)
            for d in Desig:
                des = d.find_all('li')
                
                if(d.find_all('li') != None):                   
                    for s in des:
                        if(s.find(class_='job-title')!= None or s.find(class_='job-description')!= None):
                            Designation_1 = s.find('span')
                            de = Designation_1.get_text()
                            Designation.append(de)
                        else:
                            time.sleep(0)
                else:
                    time.sleep(0)
            
            Des = ','.join(Designation)

#             print(Designation)
                    
            try:
#                 cit2 = 0
                cit = resp1.find(class_='citations')
                cit2 = cit.find(class_='count increment-counter').get_text()
            except:
                cit2 = ""
                
            interests = ""                  
            c4 = resp1.find_all(class_='person-fingerprint-thesauri')
            if (c4!= None):
                interests = []
                for fing in c4:
                    c5 = fing.find('h3').get_text()
                    interests.append(c5)
                inter = ','.join(interests)
            else:
                interests = ""
            
            Profile = Profile +1
            profile_details = {
                            'Profile ID': Profile,
                            'Name': h,
                            'Profile Link': r,
                            'Designation': Des,
                            'Active Interests': inter,
                            'No. of Citations': cit2
                          }
            
            with open("Department_Profiles.json", "a+") as outfile:
                json.dump(profile_details, outfile)
                outfile.write("\n")

