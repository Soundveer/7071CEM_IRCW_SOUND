#!/usr/bin/env python
# coding: utf-8

# In[13]:


from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import json
session = webdriver.Chrome()
session.maximize_window()

session.get("https://pureportal.coventry.ac.uk/en/organisations/centre-global-learning/persons/")    # Coventry URL Site
time.sleep(10)
session.find_element(By.XPATH,"//button[@id='onetrust-accept-btn-handler']").click() # Accept Cookies

for j in range(0 , 1):
    
        # Profiles per Page
        Cov_Page_Url = "https://pureportal.coventry.ac.uk/en/organisations/centre-global-learning/persons/?page=%d"%(j)
        session.get(Cov_Page_Url)
        a = browser.page_source
        resp=BeautifulSoup(a,"html.parser")
        
        Cov_Page_Profiles = resp.find(class_ = 'grid-results')
        Cov_Page_Profiles_2 = Cov_Page_Profiles.find_all('h3') # User details
        
        # Load Each Profile in page
        for prof in Cov_Page_Profiles_2:
            
            Profile_Url = prof.find('a')
            Profile_Url_2 = Profile_Url['href'] + '/publications'
            time.sleep(5)
            print("URL:" + Profile_Url_2)
            session.get(Profile_Url_2)
            b = session.page_source
            resp1 = BeautifulSoup(b,"html.parser")
            
#             Research_Output = browser.find_element_by_xpath("/html/body/main/div[1]/section/div[2]/div/div/nav/ul/li[4]/a/span/i")

            if(resp1.find(class_='icon icon-publications') != None):
                Cov_Research_Paper = resp1.find(class_='list-results')
                Cov_Research_Paper_2 = Cov_Research_Paper.find_all('h3')   #Research Papers Count in the first page
                
                # Create Empty array to store URL's of User Research Paper
                urls=[]
                
                for paper in Cov_Research_Paper_2:
                    Cov_Research_Paper_3 = paper.find('a')
                    Cov_Research_Paper_4 = Cov_Research_Paper_3['href'] # each research paper
                    urls.append(Cov_Research_Paper_4)
                    
                try:
                    while(browser.find_element(By.XPATH,"/html/body/main/div[1]/div/div/section/nav/ul/li[3]/a") != None):
                        Res_Pap_Page = resp1.find(class_='next')
    #                     Resp_Pap_Page_2 = Res_Pap_Page.find(class_='next')
                        Res_Pap_Page_3 = Res_Pap_Page.find('a')
                        Research_Url = 'https://pureportal.coventry.ac.uk' + Res_Pap_Page_3['href']
                        browser.get(Research_Url)
                        time.sleep(5)
#                         browser.find_element(By.XPATH,"/html/body/main/div[1]/div/div/section/nav/ul/li[3]/a").click()
                        e = browser.page_source
                        resp2 = BeautifulSoup(e,"html.parser")
                        Cov_Research_Paper = resp2.find(class_='list-results')
                        Cov_Research_Paper_2 = Cov_Research_Paper.find_all('h3') #Research Papers Count in the consecutive page
                        for paper in Cov_Research_Paper_2:
                            Cov_Research_Paper_3 = paper.find('a')
                            Cov_Research_Paper_4 = Cov_Research_Paper_3['href'] # each research paper
                            urls.append(Cov_Research_Paper_4)
                except:
                    time.sleep(0)
                
#                 print(urls)
                    
                print(len(urls))
                for Cov_Pap in urls:

                    session.get(Cov_Pap)
                    time.sleep(2)
                    c = session.page_source
                    resp3=BeautifulSoup(c,"html.parser")
            
                    Res_Title = resp3.find(class_='rendering')
                    Cov_Title = Res_Title.get_text()
                        
                    Res_Dept = resp3.find(class_='relations organisations')    # Capture Department Details                        
                    if(Res_Dept != None):
                        Cov_Dept_2 = Res_Dept.find('a')
                        if(Cov_Dept_2 != None):
                            Cov_Department = Cov_Dept_2.get_text()
                        else:
                            Cov_Department = ""
                    else:
                        Cov_Department = ""
                            
                    Res_Year = resp3.find(class_='status')     # Publication Year
                    if(Res_Year != None):
                        Cov_Publ = Res_Year.find(class_='date')
                        Cov_Publ_2 = Cov_Publ.get_text()
                        Cov_Year = Cov_Publ_2[-4:]
                    else:
                        Cov_Year = ""
                            
                    Res_Doc = resp3.find(class_='content-sidebar publication-sidebar')    # Access to Doc Link
                    Cov_Doc_2 = resp3.find(class_='doi')
                    if(Res_Doc != None and Cov_Doc_2 != None):
                        Cov_Doc_3 = Cov_Doc_2.find('a')
                        Cov_Document = Cov_Doc_3['href']
                    else:
                        Cov_Document = ""
                            
                    Res_Abstract = resp3.find(class_='textblock')             # Research_Paper_Abstract
                    if(Res_Abstract != None):
                        Cov_Abstract = Res_Abstract.get_text()
                    else:
                        Cov_Abstract = ""

                    authors = resp3.find(class_='relations persons')
                    if(authors != None):
                        Cov_Authors = authors.get_text()
                    else:
                        Cov_Authors = ""

                    if(resp3.find(class_= 'icon icon-fingerprint') != None):
                        interests = []
                        FP_Url = Cov_Pap + '/fingerprints'
                        session.get(FP_Url)
                        d = session.page_source
                        time.sleep(2)
                        resp4 = BeautifulSoup(d,"html.parser")
                        Res_FP = resp4.find_all(class_='publication-fingerprint-thesauri')
                        if (Res_FP != None):
                            for fp in Res_FP:
                                Cov_Interests = fp.find('h3').get_text()
                                interests.append(Cov_Interests)
                            Cov_Interests = ','.join(interests)
                        else:
                            Cov_Interests = ""
                    else:
                        Cov_Interests = ""
                        
                    Scrapped_Cov_Data = {
                            'Title': Cov_Title,
                            'Publications Authors': Cov_Authors,
                            'Department': Cov_Department,
                            'Publication Year': Cov_Year,
                            'Paper Link': Cov_Pap,
                            'Tags':Cov_Interests,
                            'Access to Doc.': Cov_Document,
                            'Abstract':Cov_Abstract
                          }

                    with open("Research_Papers.json", "a+") as outfile:
                        json.dump(Scrapped_Cov_Data, outfile)
                        outfile.write("\n")
            else:
                time.sleep(0)


# In[ ]:




