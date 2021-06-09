import time,sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class WhatsappBot():
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/ASUS/AppData/Local/Google/Chrome/User Data/Default')
    options.add_argument('--profile-directory=Default')
    options.add_argument('--disable-infobars')
    chrome_browser = webdriver.Chrome(executable_path = 'D:/softwares and datasets zips/zipfiles and installer files/chromedriver.exe')
    chrome_browser.get('https://web.whatsapp.com/')
    # Time to sleep during QR processing
    time.sleep(40)
    
    def __init__(self,numbers_list):
        self.numbers_list = numbers_list
        

    def inbox_chats(self):
        for user_name in numbers_list:
            try:
                user = chrome_browser.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
                user.click()
            except NoSuchElementException as se:
                new_chat(user_name)
                time.sleep(20)
            message_box = chrome_browser.find_element_by_xpath('//div[@class="_2A8P4"]')
            
            if len(message) != 0:
                message_keys = list(message.keys())
                message_values = list(message.values())
                print(message_values)
                for i in range(len(message)):
                    message_box.send_keys("{} : {}".format(message_keys[i],message_values[i]))
                    ActionChains(chrome_browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
                message_box = chrome_browser.find_element_by_xpath('//button[@class="_1E0Oz"]')
                message_box.click()
                time.sleep(20)
            else:
                pass
        chrome_browser.close()


def new_chat(user_name):
    search_box = chrome_browser.find_element_by_xpath('//div[@class="_2_1wd copyable-text selectable-text"]')
    search_box.click()
    search_box.send_keys(user_name)
    try:
        user = chrome_browser.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
        user.click()
    except NoSuchElementException as se:
        print('Given user "{}" not found in the contact list')
    except Exception as e:
        chrome_browser.close()
        print(e)
        sys.exit()
