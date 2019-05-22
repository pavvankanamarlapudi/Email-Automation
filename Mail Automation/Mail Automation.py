
# coding: utf-8




import os, smtplib, ssl, getpass, datetime,imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders as Encoders
import pandas as pd





def send_mail(username, password, from_addr, to_addrs, msg):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, msg.as_string())


# In[65]:


port = 465 
username="pavvankanamarlapudi@gmail.com"

password  = getpass.getpass("Enter your Password: ")
fromaddr = username

files  = '.\Attachments'
filenames = [os.path.join(files, f) for f in os.listdir(files)]




recruiter_list = pd.read_csv("recruiter_list.csv")

recruiter_list = recruiter_list[['Company', 'Location', 'Email', 'Sent']]

recruiter_list["Email"]=recruiter_list["Email"].apply(lambda x:x.lower())

recruiter_list = recruiter_list.drop_duplicates(['Email'])

recruiter_list['TimeStamp']=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

receivers = list(recruiter_list.loc[recruiter_list.Sent!="Done"]['Email'])

if len(receivers)>=1:
    print("Receivers: \n"+"\n".join(receivers))
else:
    print("Couldn't Found New receipents!")
    recruiter_list.to_csv("recruiter_list.csv",index=False)





Body =   """
            Dear Hiring Manager,<p style="text-indent: 40px">I’m seeking for the postion of <b><font color="#5727A1">Data Scientist/Data Analyst</b></font>  at your Organization. Currently, I have been working as <b><font color="#5727A1">Jr.Data Scientist</font></b> at <b>GSPANN Technologies</b> having <b>2 Years</b> of experience. 
            PFA for updated <b>Resume</b> and <b>Cover letter</b> for your own reference. </p>I am looking forward to hear more about work role in the form of a formal interview. Please also feel free to call me via the Phone number or Email address listed on my attached resume.

            """




for receiver in receivers:
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = receiver
    msg['Subject'] = "Job Application - Data Science"
    Mail_Body=MIMEText(Body, 'html')
    msg.attach(Mail_Body)
    
    for file in filenames:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        Encoders.encode_base64(part)
        FileName=file.split("\\")[-1]
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % FileName)    
        msg.attach(part)
    
    try:
        send_mail(username=username, password=password, from_addr=fromaddr, to_addrs=receiver, msg=msg)
        recruiter_list.loc[recruiter_list.Email==receiver,"Sent"]="Done"
        recruiter_list.loc[recruiter_list.Email==receiver,"TimeStamp"]=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        recruiter_list.to_csv("recruiter_list.csv",index=False)
        print("Mail send to {} Succesfully and Database has updated!".format(receiver))
       
        
    except SMTPAuthenticationError:
        print('SMTPAuthenticationError')
        print("Email not sent to", to_addrs)
    except Exception as e:
        print(e)





datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# ### Reference:
#==============
# https://stackoverflow.com/questions/882712/sending-html-email-using-python

# https://stackoverflow.com/questions/26582811/gmail-python-multiple-attachments