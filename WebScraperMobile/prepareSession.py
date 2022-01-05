# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 00:31:59 2021

@author: maxik

1. checks database for missing records (make & model)
2. gets user agent
3. start selenium-chrome with user agent
4. connects to random proxy
5. switches to empty site and returns driver object
"""
#!!! random proxy list on the fly generieren, da sonst bei fehler webdriver referenz nicht mehr richtig ist.

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium.webdriver.common.keys import Keys
import time
import random
import configSession



"""tasks of this class:
        - checks for new entries in the config and compares then to the DB (new models to be scraped?)
        - launches the webdriver (chrome instance) with a random user-agent
        - logs into the proxy
        - connects to a random proxy
        - return webdriver object for further actions (such as actual scraping)
"""
class SeleniumChrome:
    
    PATH = 'C:\\Users\\maxik\\Documents\\PythonProjects\\chromedriver'
    EXTENSION_ID = 'ailoabdmgclmfmhdagmlohpjlbpffblp'
    user_agent_list = []
    
    def __init__(self):
        self.__get_user_agent()
    
    """"creates webdriver instance and launches chrome with desired settings: random UA, extensions, page load strategy.
        also logs into the proxy(see method below)"""
    def start_webdriver(self):
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "normal"
        chrome_options = Options()
        ua = random.choice(self.user_agent_list)
        print(ua)
        chrome_options.add_argument("user-agent={}".format(ua))
        chrome_options.add_extension("surfshark.crx")
        chrome_options.add_extension("showIP.crx")
        self.driver = webdriver.Chrome(executable_path=self.PATH, options=chrome_options, desired_capabilities=caps)
        self.actions = ActionChains(self.driver)
        self.__proxy_login()
    
    """!!!must be called before anything with */proxy/*
        logs into the proxy
    """
    def __proxy_login(self, retry=False):
        self.driver.get("https://duckduckgo.com")
        #time.sleep(10)
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        #navigate to extension url and fill in forms
        self.driver.get(f"chrome-extension://{self.EXTENSION_ID}/index.html")
        if not retry:
            email_field = self.driver.find_element_by_name('email')
            self.actions.send_keys_to_element(email_field, '<youremail@example.com>')
            pwd_field = self.driver.find_element_by_name('password')
            self.actions.send_keys_to_element(pwd_field, '<yourpassword>').perform()
            submit = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/section/form/button[2]')
            submit.click()
        
        # wait for form to be submitted and then locate all listed proxies
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, '//span[@class="_2rgfu"]')))  #list of proxies
        print('logged into surfshark')
        
        
    """reads list of user agents from .txt file
        user agents are all different versions of chrome, because of compatibility issues
    """
    def __get_user_agent(self):
        with open("user_agents.txt", 'r') as f:
            useragents = []
            for line in f:
                useragents.append(line)
        self.user_agent_list = useragents
    
    
    """used by connect2_new_proxy() for connecting to desired proxy location and handling possible errors"""
    def connect_proxy(self, location):
        loop = True
        while loop:
            self.driver.switch_to.window(self.driver.window_handles[1])
            element = self.driver.find_element_by_xpath(location[0])
            element.click()
            try:
                WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div[@class="_3C3tn"]//div[@class="_1orui"]')))  #connectino establishment
                WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[3]/div[@class="_3C3tn"]//button')))  #connectino establishment
                loop = False
            except:
                print('connecting to proxy failed: ', location[1], '\nretrying...')
                self.close_tab()
                self.navigate_tab(0)
                self.__proxy_login(True)  # set retry to True
        try:
            location_text = self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/div[3]/div[2]/div/div[2]').text
            address_text  = self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/div//div[@class="_3cvF3"]').text
        except:
            location_text = 'location could not be found'
            address_text = 'address unknown'
        print('connection established: ', location_text, address_text)
    
    
    """returns a generator for all proxy locations"""
    global get_new_proxy
    def get_new_proxy():
        for location in configSession.proxies_sample:
            yield location # connect to each proxy in succession
        
        
    """return all proxy locations in printable format"""    
    global showAllProxies
    def showAllProxies():
        for location in configSession.proxies_sample:
            yield print(location)
            
            
    """makes an http request"""        
    def request(self, url):
        response = self.driver.get(url)
        return response
    
    
    """disconnects from current proxy"""
    def disconnect_proxy(self):
        self.navigate_tab(1)
        disconnect = self.driver.find_element(By.XPATH, '//button[@class="_2giRN _2r1Q_ _2amg4"]')  #search for disconnect button
        disconnect.click()
        print('disconnected from proxy')
        
        
    """opens a new tab and navigates to it"""    
    def open_new_tab(self, tab):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[tab])
        print('new tab created')
        
    
    """closes the current tab"""
    def close_tab(self):
        self.driver.execute_script("window.close('');")


    """navigates to the desired tab (starting from 0)"""
    def navigate_tab(self, tab):
        self.driver.switch_to.window(self.driver.window_handles[tab])
        
        
    """closes the current driver instance"""    
    def quit(self):
        self.driver.quit()
        print('browser terminated')
        
    
    """chrome webdriver getter and setter"""
    def set_driver(self, d):
        self.driver = d
        
    def get_driver(self):
        return self.driver
        
#-----------------------------------------------------------------------------

if __name__ == '__main__':
    num_instances = 2
    schs = [SeleniumChrome() for _ in range(num_instances)]
    gen = get_new_proxy()
    for sch in schs:
        sch.start_webdriver()
        sch.connect_proxy(next(gen))
        try:
            sch.open_new_tab(2)
            sch.request('https://www.httpbin.org/headers')
            print('#'*50)
        except Exception as e:
            print(e)
        #sss.quit()