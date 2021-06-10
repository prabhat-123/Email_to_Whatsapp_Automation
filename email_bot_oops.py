import imaplib,email
from datetime import datetime
from email.header import decode_header
import os
import webbrowser
# from socket import gaierror
import sys

class Email_Bot():

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def login(self,imap_url):
        self.imap_url = imap_url
        try:
            mail = imaplib.IMAP4_SSL(imap_url,993)
            mail.login(self.username,self.password)
            print("Login successful")
            return mail
        except Exception as e:
            print("Login Failed")
            mail = None
            return mail

    def fetch_email(self,domain,enquiry,mail):
        self.domain = domain
        self.enquiry = enquiry
        self.mail = mail
        date = datetime.now().date()
        date = "{}".format(date.strftime(("%d-%b-%Y")))
        mail.select('inbox')
        # Fetch email from specific domain and specific date
        result,search_data = mail.search(None,f'(SENTSINCE {date})','ALL HEADER FROM {}'.format(domain))
        fetch_date_time = datetime.now()
        required_fields = ['User Name','User City','User State','User Phone','User Email','User Area','User Requirement','Search Date & Time']
        processed_enquiry = enquiry[0].upper() + enquiry[1:]
        if os.path.exists('checkpoint.txt'):
            a = open('checkpoint.txt','r')
            c = a.read()
            checkpoint_date = datetime.strptime(c,'%Y-%m-%d %H:%M:%S')
            outer_email_data = []
            for num in search_data[0].split():
                inner_email_data = {}
                _,data = mail.fetch(num,'(RFC822)')
                _,b = data[0]
                email_message = email.message_from_bytes(b)
                date_details = email_message['date']
                header_subject = email_message['subject']
                date_splits = date_details.split(',')[1]
                date_splits = date_splits.split('+')[0]
                day = date_splits.split(' ')[1]
                month = date_splits.split(' ')[2]
                year = date_splits.split(' ')[3]
                time = date_splits.split(' ')[4]
                date_month = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
                month = date_month[month]
                date_time_str = "{}-{}-{} {}".format(year,month,day,time)
                date_time_dt = datetime.strptime(date_time_str,'%Y-%m-%d %H:%M:%S')
                if date_time_dt > checkpoint_date and '{}'.format(processed_enquiry) in header_subject:
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True)
                            all_data = body.decode()
                            split_data = all_data.split('\n')
                            for item in split_data:
                                clean_item = item.split('\r')
                                if len(clean_item) == 2 and clean_item[0].startswith('User'):
                                    data = clean_item[0]
                                    if ':' not in data:
                                        inner_email_data['User Name'] = data.split(' ')[1] 
                                    for field in required_fields:
                                        if data.startswith(field):
                                            inner_email_data[field] = data.split(':')[1].strip()
                                        else:
                                            pass 
                    outer_email_data.append(inner_email_data)
            d = open('checkpoint.txt','w+')
            d.write("{}".format(fetch_date_time.strftime(('%Y-%m-%d %H:%M:%S'))))
            return outer_email_data
            sys.exit()

        else:
            outer_email_data = []
            for num in search_data[0].split():
                inner_email_data = {}
                _,data = mail.fetch(num,'(RFC822)')
                _,b = data[0]
                email_message = email.message_from_bytes(b)
                header_subject = email_message['subject']
                if '{}'.format(processed_enquiry) in header_subject:                       
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True)
                            all_data = body.decode()
                            split_data = all_data.split('\n')
                            for item in split_data:
                                clean_item = item.split('\r')
                                if len(clean_item) == 2 and clean_item[0].startswith('User'):
                                    data = clean_item[0]
                                    if ':' not in data:
                                        inner_email_data['User Name'] = data.split(' ')[1] 
                                    for field in required_fields:
                                        if data.startswith(field):
                                            inner_email_data[field] = data.split(':')[1].strip()
                                        else:
                                            pass
                    outer_email_data.append(inner_email_data)   
            f = open('checkpoint.txt','w+')
            f.write("{}".format(fetch_date_time.strftime(('%Y-%m-%d %H:%M:%S'))))
            return outer_email_data
            sys.exit()

