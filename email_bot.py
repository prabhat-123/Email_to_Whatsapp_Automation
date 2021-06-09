import imaplib,email
from datetime import datetime
from email.header import decode_header
import os
import webbrowser

user = 'srv.ale52@gmail.com'
password = 'prabhat9811956469'
imap_url = 'imap.gmail.com'
date = datetime.now().date()
date = "{}".format(date.strftime(("%d-%b-%Y")))
mail = imaplib.IMAP4_SSL(imap_url,993)
mail.login(user,password)
mail.select('inbox')
# Fetch email from specific domain and specific date
domain= 'srv.alemgr@gmail.com'
result,search_data = mail.search(None,f'(SENTSINCE {date})','ALL HEADER FROM {}'.format(domain))
fetch_date_time = datetime.now()
print(fetch_date_time)
required_fields = ['User Name','User City','User State','User Phone','User Email','User Area','User Requirement','Search Date & Time']


def fetch_email():
    if os.path.exists('checkpoint.txt'):
        a = open('checkpoint.txt','r')
        c = a.read()
        print(c)
        checkpoint_date = datetime.strptime(c,'%Y-%m-%d %H:%M:%S')
        print(checkpoint_date)
        outer_email_data = []
        outer_email_header = []
        for num in search_data[0].split():
            inner_email_data = {}
            inner_email_header = {}
            _,data = mail.fetch(num,'(RFC822)')
            _,b = data[0]
            email_message = email.message_from_bytes(b)
            for header in ['subject','to','from','date']:
                if header == 'date':
                    date_details = email_message[header]
                    date_splits = date_details.split(',')[1]
                    date_splits = date_splits.split('+')[0]
                    day = date_splits.split(' ')[1]
                    month = date_splits.split(' ')[2]
                    year = date_splits.split(' ')[3]
                    time = date_splits.split(' ')[4]
                    date_month = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
                    month = date_month[month]
                    date_time_str = "{}-{}-{} {}".format(year,month,day,time)
                    print(date_time_str)
                    date_time_dt = datetime.strptime(date_time_str,'%Y-%m-%d %H:%M:%S')
                    print(date_time_dt)
                    print(type(date_time_dt))
                    if date_time_dt > checkpoint_date:
                        inner_email_header[header] = email_message[header]
                        if header == 'from':
                            inner_email_header[header] = email_message[header][email_message[header].find('<') + 1 : email_message[header].find('>')]
                        else:
                            inner_email_header[header] = email_message[header]
                            
                        for part in email_message.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True)
                                all_data = body.decode()
                                split_data = all_data.split('\n')
                                for item in split_data:
                                    clean_item = item.split('\r')
                                    if len(clean_item) == 2:
                                        for field in required_fields:
                                            if clean_item[0].startswith(field):
                                                inner_email_data[field] = clean_item[0].split(':')[1].strip() 
                        outer_email_data.append(inner_email_data)
                        outer_email_header.append(inner_email_header)
        d = open('checkpoint.txt','w+')
        d.write("{}".format(fetch_date_time.strftime(('%Y-%m-%d %H:%M:%S'))))

    else:
        f = open('checkpoint.txt','w+')
        f.write("{}".format(fetch_date_time.strftime(('%Y-%m-%d %H:%M:%S'))))
        outer_email_data = []
        outer_email_header = []
        for num in search_data[0].split():
            inner_email_data = {}
            inner_email_header = {}
            _,data = mail.fetch(num,'(RFC822)')
            _,b = data[0]
            email_message = email.message_from_bytes(b)
            
            for header in ['subject','to','from','date']:
                if header == 'from':
                    inner_email_header[header] = email_message[header][email_message[header].find('<') + 1 : email_message[header].find('>')]
                else:
                    inner_email_header[header] = email_message[header]                          
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    all_data = body.decode()
                    split_data = all_data.split('\n')
                    for item in split_data:
                        clean_item = item.split('\r')
                        if len(clean_item) == 2:
                            for field in required_fields:
                                if clean_item[0].startswith(field):
                                    inner_email_data[field] = clean_item[0].split(':')[1].strip() 
                    outer_email_data.append(inner_email_data)
                    outer_email_header.append(inner_email_header)      
    return [outer_email_data,outer_email_header]



[outer_email_data,outer_email_header] = fetch_email()
print(len(outer_email_data))
print(len(outer_email_header))
print(outer_email_header)
print(outer_email_data)

                # if header == 'subject':
                #     header_subject = email_message[header]
                #     print(header_subject)
                #     if 'Enquiry' not in header_subject:
                #         pass
                #     else: