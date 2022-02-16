from aiohttp import request
from attr import attrs
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

START_URL="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser=webdriver.Chrome("/Users/samva/Downloads/chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
headers=["Name","Lightyears_from_Earth","Planet_Mass","Stellar_Magnitude",'Discovery_Date','Hyperlink',"Planet_Type","Planet_Radius","Orbital_Radius","Orbital_Period","Eccentricity"]
planet_data=[]
new_planet_data=[]

def scrape():
    for i in range(0,491):
        soup=BeautifulSoup(browser.page_source,"html.parser")
        for ul_tag in soup.find_all("ul",attrs={"class","exoplanet"}):
            li_tags=ul_tag.find_all("li")
            temp_list=[]
            for index,li_tags in enumerate(li_tags):
                if index==0:
                    temp_list.append(li_tags.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tags.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tags=li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov/"+hyperlink_li_tags.find_all("a",href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i} page done 1")
    #with open("scraper.csv",'w') as f:
        #csvwriter=csv.writer(f)
        #csvwriter.writerow(headers)
        #csvwriter.writerows(planet_data)

def scrape_more_data(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.passer")
        temp_list=[]
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):    
            td_tags=tr_tag.find_all("td")
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
        #write to the csv file
scrape()