from bs4 import BeautifulSoup #library for parsing html
import requests #library for making http requests
import smtplib #library for sending emails
import time
import datetime
import csv
import pandas as pd
import os

def send_mail(to, subject,body):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    #server.starttls()
    server.ehlo()
    server.login("taruns994@gmail.com", "gmail-app-key")
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail("taruns994@gmail.com", to, message)
    server.close()
# Connect to Website - Amazon product link
URL = "https://www.amazon.com/dp/B0B6GLQJMV/ref=ods_gw_GW_US_EN_ViCC-Rg_Nm_Sep2023-US-AMWAC_H1_Y/?_encoding=UTF8&pd_rd_w=8dhiG&content-id=amzn1.sym.765e8e73-7a10-438a-a4ba-de664bb82f60&pf_rd_p=765e8e73-7a10-438a-a4ba-de664bb82f60&pf_rd_r=CM4FZDF7WNY9TSQWPDVJ&pd_rd_wg=OPGCA&pd_rd_r=612b6b43-540b-4983-b819-95c47e164448"

# Enter time in seconds
check_time = 5

 # TO find header information : https://httpbin.org/get
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "DNT":"1",
            "Connection":"close",
            "Upgrade-Insecure-Requests":"1"
            }

page = requests.get(URL, headers=headers)

soup1 = BeautifulSoup(page.content, 'html.parser') #Used to pull in all html of the webpage

soup2 = BeautifulSoup(soup1.prettify(), 'html.parser') # formatted version of soup1

title  = soup2.find(id="productTitle").get_text().strip() #Returns the title of the product
price = soup2.find(id="corePriceDisplay_desktop_feature_div") #Returns div containing the price of the product
price = price.find('span', class_='a-offscreen').get_text().strip()[1:] #Returns the price of the product
rating = (soup2.find(id="acrPopover")).find('span', class_="a-size-base a-color-base").get_text().strip() #Returns the rating of the product
date = datetime.date.today() #Returns the date of the product
current_time = time.strftime("%H:%M:%S")
#Storing data in a csv file
header = ['Date', 'Time','Title', 'Price', 'Rating']
data = [[date,current_time,title, price, rating]]

if os.path.isfile('amazon_ringcam.csv'): #if file exists then update prices
    while(True):
        with open('amazon_ringcam.csv', 'a+', newline='', encoding="UTF8") as f: # Appending data to csv file
            writer = csv.writer(f)
            title  = soup2.find(id="productTitle").get_text().strip() #Returns the title of the product
            price = soup2.find(id="corePriceDisplay_desktop_feature_div") #Returns div containing the price of the product
            price = price.find('span', class_='a-offscreen').get_text().strip()[1:] #Returns the price of the product
            rating = (soup2.find(id="acrPopover")).find('span', class_="a-size-base a-color-base").get_text().strip() #Returns the rating of the product
            date = datetime.date.today() #Returns the date of the product
            current_time = time.strftime("%H:%M:%S")
            data = [[date,current_time,title, price, rating]]
            writer.writerows(data)
            print("Checking current price @", current_time, "Price:",price)
        if(float(price) < 40.0):
            to = "clanmaster65@gmail.com"
            subject = "Price of Amazon Ringcam is below 60.00"
            body = "Please buy it from: "+ URL
            send_mail(to, subject ,body)
            print("Sent discount email")
        time.sleep(check_time)
else:
    with open('amazon_ringcam.csv', 'w', newline='', encoding="UTF8") as f: #writing data to csv file
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
        print("Created file")

# df = pd.read_csv("amazon.csv")