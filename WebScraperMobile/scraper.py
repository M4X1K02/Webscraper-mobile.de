# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 15:10:47 2021

@author: maxik
"""
import regex as re
import datetime
from selenium.webdriver.common.keys import Keys


"""return current timestamp"""
def timestamp():
    return datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    
class Scraper:
    
    """pass webdriver to class"""
    def __init__(self, webdriver):
        self.driver = webdriver

    
    def links(self):
        allLinks = []
        return allLinks
    
    def getHTML(self):
        html = self.driver.page_source
        return html
    
    
    """return mobileID (addID) as Integer"""
    def adID(self, inserat: object):
        try:
            id_raw = inserat.find_element_by_xpath(".//a[@class='link--muted no--text--decoration result-item']")
            id = id_raw.get_attribute('data-ad-id')
            return int(id)
        except Exception as e:
            print(e)
            
    
    """returns title of add as string"""
    def title(self, inserat: object):
        try:
            title = inserat.find_element_by_xpath(".//span[@class='h3 u-text-break-word']")
            return title.text
        except Exception as e:
            print(e)
            
    
    """return price as integer"""
    def price(self, inserat: object):
        try:
            content = inserat.find_element_by_xpath(".//div[@class='g-col-9']")
            title_container = content.find_element_by_xpath(".//div[@class='g-row']")
            price_raw = title_container.find_element_by_xpath(".//span[@class='h3 u-block']")
            price_txt = price_raw.text
            price = int(price_txt.split(" ")[0].replace('.', '')) # 10.000 € -> 10.000 -> 10000 -> int 10000
            return price
        except Exception as e:
            print(e)
            return None
        
        
    """return regdate, mileage, power as tuple"""
    def regMilPow(self, inserat: object):
        try:
            regMilPow_raw = inserat.find_element_by_xpath(".//div[@data-testid='regMilPow']")
            # searches for reg.Date, mileage and power and adds them
            regMilPowSplit = regMilPow_raw.text.split(",")
            reg=None
            mil=None
            power=None
            for j in regMilPowSplit:
                if "EZ " in j:
                    reg = j
                    reg = re.findall("\d*\/?\d+", reg)[0]
                if "km" in j:
                    mil = j.strip()
                    milSplits = re.findall("[0-9]+", mil)
                    if len(milSplits) == 2:
                        mil = int(milSplits[0] + milSplits[1])
                    elif len(milSplits) == 3:
                        mil = int(milSplits[0] + milSplits[1] + milSplits[2])
                    elif len(milSplits) == 1:
                        mil = int(milSplits[0])
                if "kW" in j:
                    power = j.strip()
                    power = int(re.findall("\d*\d+", power)[0])
            return mil,reg, power
        except Exception as e:
            print(e)
    

    """return boolean accident: True/False, else None"""
    def accident(self, inserat: object):
        try:
            content = inserat.find_element_by_xpath(".//div[@class='g-col-9']")
            details = content.find_element_by_xpath(".//div[@class='g-col-12']")
            if 'Unfallfrei' in details.text:
                return False
            else:
                return None
        except Exception as e:
            print(e)
            
            
    """return boolean driveable: True/False, else None"""
    def driveable(self, inserat: object):
        try:
            content = inserat.find_element_by_xpath(".//div[@class='g-col-9']")
            details = content.find_element_by_xpath(".//div[@class='g-col-12']")
            if 'Nicht fahrtauglich' in details.text:
                return False
            else:
                return True
        except Exception as e:
            print(e)   
            return None
            
            
    """return boolean damaged: True/False, else None"""
    def damaged(self, inserat: object):
        try:
            content = inserat.find_element_by_xpath(".//div[@class='g-col-9']")
            details = content.find_element_by_xpath(".//div[@class='g-col-12']")
            if 'Beschädigt' in details.text:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return None
            
            
    """return boolean gasoline: True/False"""
    def gasoline(self, inserat: object):
        try:
            content = inserat.find_element_by_xpath(".//div[@class='g-col-9']")
            details = content.find_element_by_xpath(".//div[@class='g-col-12']")
            
            if 'Benzin' in details.text:
                return True
            elif 'Diesel' in details.text:
                return False
            else:
                return None
        except Exception as e:
            print(e)
            
            
    """return boolean manual: True/False, else None"""
    def manual(self, inserat: object):
        try:
            content = inserat.find_element_by_xpath(".//div[@class='g-col-9']")
            details = content.find_element_by_xpath(".//div[@class='g-col-12']")
            
            if ('Automatik' or 'Halbautomatik') in details.text:
                return False
            elif 'Schaltgetriebe' in details.text:
                return True
            else:
                return None
        except Exception as e:
            print(e)
    
    
    """return boolean dealer: True/False, else None"""
    def dealer(self, inserat: object):
        try:
            cssClass = inserat.get_attribute("class")
            if "dealerAd" in cssClass:
                return True
            elif "fsboAd" in cssClass:
                return False
            else:
                return None
        except Exception as e:
            return None
            print(e)
            
            
    # print(urllib.request.urlretrieve(img))
    # image = PIL.Image.open("{}.png".format(self.adID(inserat)))
    # image.show()
    """returns image url"""
    def get_image_url(self, inserat: object):
        try:
            img_raw = inserat.find_element_by_xpath('.//img[contains(@class,"img-responsive")]')
            img = img_raw.get_attribute("src")
            return img
        except Exception as e:
            return None
            print(e)


    """
    def save_image_from_url(self, adID: str, url: str):
        # code for img download (requests or whatever)
        try:
            r= urllib.request.urlopen(url)
            with open("{}.jpg".format(adID), "wb") as f:
                    f.write(r.read())
                    f.close()
        except Exception as e:
            print(e)
    """      
    
    
    """returns link for next page, if last page (no link) return None"""
    def next_page(self):
        try:
            page = self.driver.find_element_by_xpath(".//span[@title='Zur nächsten Seite']")
            return page.get_attribute('data-href')
        except Exception as e:
            try:
                bot_detect_container = self.driver.find_element_by_xpath("//div[@class='u-pad-bottom-18 u-margin-top-18']")
                bot_detect_text = bot_detect_container.text
                if (bot_detect_text == 'Ups, bist Du ein Mensch? / Are you a human?'):
                    print('bot has been detected! #?*$! ')
                    return 1
            except:
                print("bot has NOT been detected yet ^^")
            self.driver.find_element_by_xpath()
            print(e, "link not found, page end reached")
            return None

    
    def collect_data(self):
        
        # scroll by pressing pagedown twice
        html = self.driver.find_element_by_tag_name('html')
        html.send_keys(Keys.PAGE_DOWN)
        html.send_keys(Keys.PAGE_DOWN)
        
        # loop through all adds
        inserate = self.driver.find_elements_by_xpath("//div[contains(@class,'cBox-body cBox-body--resultitem')]")
        add_list = []
        for inserat in inserate:
            mil, reg, pow  = self.regMilPow(inserat)
            add_list.append((   self.adID(inserat),
                                self.title(inserat),
                                self.price(inserat),
                                mil,
                                reg,
                                pow,
                                self.accident(inserat),
                                self.driveable(inserat),
                                self.damaged(inserat),
                                self.gasoline(inserat),
                                self.manual(inserat),
                                self.dealer(inserat),
                                self.get_image_url(inserat),
                                timestamp()))
        return add_list
    
    def current_url(self):
        url = self.driver.getCurrentUrl();
        return url