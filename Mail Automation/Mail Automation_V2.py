
# coding: utf-8

# In[ ]:


import os, smtplib, ssl, getpass, datetime,imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders as Encoders
import pandas as pd
import numpy as np
from tkinter import *
from tkinter import ttk

recruiter_list = pd.read_csv("recruiter_list.csv")
recruiter_list.Email=recruiter_list.Email.apply(lambda x:x.lower())
files  = '.\Attachments'
filenames = [os.path.join(files, f) for f in os.listdir(files)]
global port
port = 465 
username="pavvankanamarlapudi@gmail.com"

password  = "XXXXXXXXXX"
fromaddr = username

Body =   """
        Dear Hiring Manager,<p style="text-indent: 40px">I’m seeking for the postion of <b><font color="#5727A1">Data Scientist/Data Analyst</b></font>  at your Organization. Currently, I have been working as <b><font color="#5727A1">Jr.Data Scientist</font></b> at <b>GSPANN Technologies</b> having <b>2 Years</b> of experience. 
        PFA for updated <b>Resume</b> and <b>Cover letter</b> for your own reference. </p>I am looking forward to hear more about work role in the form of a formal interview. Please also feel free to call me via the Phone number or Email address listed on my attached resume.

        """

def send_mail(username, password, from_addr, to_addrs, msg):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, msg.as_string())

def sendemail():
#     print('mail will sent to {}'.format(receiver.get()))
    recruiter_list = pd.read_csv("recruiter_list.csv")
    last_row_index=len(recruiter_list)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = receiver.get()
    msg['Subject'] = "Job Application - Data Science"
    Mail_Body=MIMEText(Body, 'html')
    msg.attach(Mail_Body)
    
    if not receiver.get().lower() in list(recruiter_list.Email):
        
        for file in filenames:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(file, 'rb').read())
            Encoders.encode_base64(part)
            FileName=file.split("\\")[-1]
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % FileName)    
            msg.attach(part)
        
        try:
            send_mail(username=username, password=password, from_addr=fromaddr, to_addrs=receiver.get(), msg=msg)
            ttk.Label(mainframe, text="Your CV has Send to {} Successfully & Database has Updated!".format(receiver.get())).grid(column=4,row=9,sticky=W)
            print("last row index: {}".format(last_row_index))
            recruiter_list.loc[last_row_index,"Sent"]="Done"
            recruiter_list.loc[last_row_index,"TimeStamp"]=datetime.datetime.now()
            recruiter_list.loc[last_row_index,"Email"]=receiver.get()
            recruiter_list.to_csv("recruiter_list.csv",index=False)
#         except SMTPAuthenticationError:
#             print("Email not sent to", to_addrs)
        except Exception as e:
            ttk.Label(mainframe, text="Invalid Email Address!Please check again").grid(column=4,row=9,sticky=W)

    else:
#         print(np.array(recruiter_list.loc[recruiter_list.Email==receiver.get(),]['TimeStamp'])[0])
        Time=pd.to_datetime(np.array(recruiter_list.loc[recruiter_list.Email==receiver.get(),]['TimeStamp'])[0])
        Time_=Time.strftime('%d-%b-%Y')+" at "+Time.strftime('%H:%M:%S')
        ttk.Label(mainframe, text="Mail Already Sent to {} at {} ".format(receiver.get(),Time_)).grid(column=4,row=9,sticky=W)
        #print("Mail Already Sent to {}".format(receiver.get()))

if __name__ == "__main__":
    root = Tk()
    root.title("Send CV via G-Mail to Recuiter!")
    
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    
    receiver = StringVar()
    ttk.Label(mainframe, text="Recruiter Mail-ID: ").grid(column=0, row=3, sticky=W)
    receiver_entry = ttk.Entry(mainframe, width=30, textvariable=receiver)
    receiver_entry.grid(column=4, row=3, sticky=(W, E))
    
    ttk.Button(mainframe, text="Send Resume", command=sendemail).grid(column=4,row=8,sticky=E)
    for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
    root.mainloop()

