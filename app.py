from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from flask import Flask,url_for,request,render_template,redirect
from apscheduler.schedulers.background import BackgroundScheduler
from gevent.pywsgi import WSGIServer
from werkzeug.utils import secure_filename
from email_bot_oops import Email_Bot
import sys
import time

# Define a flask app
app = Flask(__name__,static_folder='./static')


def load_chrome_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/ASUS/AppData/Local/Google/Chrome/User Data/Default')
    options.add_argument('--profile-directory=Default')
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    return options
    

def new_chat(user_name,chrome_browser,messages):
    try:
        search_box = chrome_browser.find_element_by_xpath('//div[@class="_2_1wd copyable-text selectable-text"]')
        search_box.click()
        search_box.send_keys(user_name)
        time.sleep(5)
        user = chrome_browser.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
        user.click()
        for message in messages:
            print(message)
            message_box = chrome_browser.find_element_by_xpath('//div[@class="_2A8P4"]')
            message_box.send_keys("{}".format(message))
            time.sleep(5)
            message_box = chrome_browser.find_element_by_xpath('//button[@class="_1E0Oz"]')
            message_box.click()
            time.sleep(10)
    except Exception as e:
        print(e)
        chrome_browser.close()
        sys.exit()
    


dict = {}
@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        email_id = request.form['mail']
        dict['email_id'] = email_id
        email_password = request.form['pwd']
        dict['email_password'] = email_password
        domain_name = request.form['domain']
        dict['domain_name'] = domain_name
        numbers = request.form['number']
        numbers_list = numbers.split(',')
        dict['numbers_list'] = numbers_list
        subject_filter = request.form['subject']
        dict['subject'] = subject_filter
        emailbot_obj = Email_Bot(email_id,email_password)
        mail = emailbot_obj.login(imap_url='imap.gmail.com')
        dict['mail_logger'] = mail
        if mail != None:
            messages = emailbot_obj.fetch_email(domain_name,subject_filter,mail)
            if len(messages) != 0:
                options = load_chrome_browser()
                chrome_browser = webdriver.Chrome(executable_path = 'D:/softwares and datasets zips/zipfiles and installer files/chromedriver.exe',options=options)
                chrome_browser.get('https://web.whatsapp.com/')
                # Time to sleep during QR processing
                time.sleep(50) 
                for user_name in numbers_list:
                    try:
                        user = chrome_browser.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
                        user.click()
                        for message in messages:
                            print(message)
                            message_box = chrome_browser.find_element_by_xpath('//div[@class="_2A8P4"]')
                            message_box.send_keys("{}".format(message))
                            time.sleep(5)
                            message_box = chrome_browser.find_element_by_xpath('//button[@class="_1E0Oz"]')
                            message_box.click()
                            time.sleep(10)
                    except NoSuchElementException as se:
                        new_chat(user_name,chrome_browser,messages)
                        time.sleep(20)
                    except Exception as e:
                        print(e)
                        chrome_browser.close()
                        sys.exit()
                chrome_browser.close()
                return redirect(url_for('predict'))  
            else:
                print("Unable to fetch email messages.This can be because of three reasons: 1) Login failed 2) No email messages are sent from the particular domain 3) Subject field is incorrect(no enquiry)")    
                return render_template('./index.html')
        else:
            print("Login Failed")
            return render_template('./index.html')
    else:
        return render_template('./index.html')


@app.route('/predict',methods=['GET'])
def predict():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(schedule_task,'interval',minutes=7)
    scheduler.start()
    return render_template('./predict.html')

def schedule_task():
    email_id = dict['email_id']
    email_password = dict['email_password']
    domain_name = dict['domain_name']
    numbers_list = dict['numbers_list']
    subject_filter = dict['subject']
    mail = dict['mail_logger']
    print(numbers_list)
    emailbot_obj = Email_Bot(email_id,email_password)
    messages = emailbot_obj.fetch_email(domain_name,subject_filter,mail)
    if len(messages) != 0:
        options = load_chrome_browser()
        chrome_browser = webdriver.Chrome(executable_path = 'D:/softwares and datasets zips/zipfiles and installer files/chromedriver.exe',options=options)
        chrome_browser.get('https://web.whatsapp.com/')
        # Time to sleep during QR processing
        time.sleep(50) 
        for user_name in numbers_list:
            try:
                user = chrome_browser.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
                user.click()
                for message in messages:
                    print(message)
                    message_box = chrome_browser.find_element_by_xpath('//div[@class="_2A8P4"]')
                    message_box.send_keys("{}".format(message))
                    time.sleep(5)
                    message_box = chrome_browser.find_element_by_xpath('//button[@class="_1E0Oz"]')
                    message_box.click()
                    time.sleep(10)
            except NoSuchElementException as se:
                new_chat(user_name,chrome_browser)
                time.sleep(20)

            except Exception as e:
                chrome_browser.close()
                sys.exit()
            
        chrome_browser.close()
    else:
        print("No new messages are received in the last 7 minutes.")

if __name__ == '__main__':
    app.run(debug=True)

