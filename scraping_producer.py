from cgi import test
from gettext import install
from platform import python_branch
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from kafka import KafkaProducer
from json import dumps

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

driver.get("https://www.google.com")
driver.maximize_window()
driver.get('https://www.strava.com/login')
username = driver.find_element_by_id("email")
password = driver.find_element_by_id("password")
username.send_keys("INSERT EMAIL ADDRESS")
password.send_keys("INSERT PASSWORD")
driver.find_element_by_id("login-button").click()

diz = {}
start_time = time.time()
seconds = #INSERT DESIDERED SCRAPING TIME IN SECONDS
i = #INSERT INITIAL ID ACTIVITY
#YOU CAN CREATE A FICTITIOUS ACTIVITY AND TAKE ITS ID FOR NEAR REAL-TIME SCRAPING
#EACH ACTIVITY FOLLOWS THE FOLLOWING URL STRUCTURE: https://www.strava.com/activities/NUMBER_ID/overview

while True:
    driver.get('https://www.strava.com/activities/' + str(i) + '/overview')

    try:
        athlete = driver.find_element_by_class_name("minimal").text
        if athlete == '':
            error = driver.find_element_by_class_name("error_nodiz").text
        diz[i] = {}
        diz[i]['athlete'] = athlete

        title = driver.title.split('|')
        diz[i]['title'] = title[0].strip()
        diz[i]['activity'] = title[1].strip()

        details = driver.find_element_by_class_name("details").text
        details = details.split('2022')[0]+'2022'
        details = details.split(',')

        if ':' in details[0]:
            diz[i]['daytime'] = {}
            diz[i]['daytime']['time'] = details[0].strip()
            date = details[1].strip().split(' ',1)
            diz[i]['daytime']['day_week'] = date[0].strip()
            diz[i]['daytime']['day'] = date[1].strip()
        else:
            diz[i]['daytime'] = {}
            diz[i]['daytime']['day_week'] = details[0].strip()
            if len(details)>1:
                diz[i]['daytime']['day'] = details[1].strip()

        kudos = driver.find_element_by_class_name("count").text
        diz[i]['social'] = {}
        diz[i]['social']['kudos'] = kudos

        list = []
        for li in driver.find_elements_by_xpath("//ul[@class='inline-stats section']/li/strong"):
            list.append(li.text)
        diz[i]['statistics'] = list

        i+=100

    except NoSuchElementException:
        i+=100

    if (i-100) in diz.keys():
        try:
            location = driver.find_element_by_class_name("location").text
            diz[i-100]['location'] = location
        except NoSuchElementException:
            pass

        try:
            list1 = []
            list2 = []
            for li in driver.find_elements_by_xpath("//div[@class='weather-label']"):
                list1.append(li.text)
            for li in driver.find_elements_by_xpath("//div[@class='weather-value']"):
                list2.append(li.text)

            if len(list1)>0:
                diz[i-100]['weather'] = {}
                diz[i-100]['weather']['Condition'] = list1[0]
                for j in range(1,len(list1)):
                    diz[i-100]['weather'][list1[j]] = list2[j-1]
        except NoSuchElementException:
            pass

        try:
            list = []
            for li in driver.find_elements_by_xpath("//ul[@class='inline-stats section secondary-stats']/li/strong"):
                list.append(li.text)
            if len(list)>0:
                diz[i-100]['statistics_advanced'] = list
        except NoSuchElementException:
            pass

        try:
            list = []
            for li in driver.find_elements_by_xpath("//div[@class='section more-stats']/div/div/strong"):
                list.append(li.text)
            if len(list)>0:
                diz[i-100]['more_statistics'] = list
        except NoSuchElementException:
            pass

        try:
            comments = driver.find_element_by_id("comments").text
            if int(comments)>0:
                driver.find_element_by_id("comments").click()
                list=[]
                for li in  driver.find_elements_by_xpath("//div[@class='comment-text']"):
                    list.append(li.text)
                diz[i-100]['social']['comments'] = list
        except NoSuchElementException:
            pass

        if diz[i-100]['activity'] == 'Ciclismo' or diz[i-100]['activity'] == 'Pedalata con e-bike' or diz[i-100]['activity'] == 'Handbike' or diz[i-100]['activity'] == 'Pedalata virtuale':
            producer.send('Ciclismo', value=diz)
        elif diz[i-100]['activity'] == 'Corsa' or diz[i-100]['activity'] == 'Corsa virtuale':
            producer.send('Corsa', value=diz)
        elif diz[i-100]['activity'] == 'Nuotata' or diz[i-100]['activity'] == 'Canoa' or diz[i-100]['activity'] == 'Kayak' or diz[i-100]['activity'] == 'Kitesurf' or diz[i-100]['activity'] == 'Canottaggio' or diz[i-100]['activity'] == 'Surf' or diz[i-100]['activity'] == 'Windsurf' or diz[i-100]['activity'] == 'Stand Up Paddle':
            producer.send('Sport_Acquatici', value=diz)
        else:
            producer.send('Altro', value=diz)

        diz = {}

    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time > seconds:
        break

    time.sleep(random.randint(3,5))