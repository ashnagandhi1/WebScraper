import pandas as pd
import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os

product_name=[]
prices=[]
description=[]

for i in range(2,12):
    url='https://www.flipkart.com/search?q=mobiles+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page='+str(i)
    r=requests.get(url)
    soup=BeautifulSoup(r.text,"html.parser")
    box=soup.find("div",class_="_1YokD2 _3Mn1Gg")

    names=box.find_all("div",class_="_4rR01T")

    for i in names:
        name=i.text
        product_name.append(name)

    price=box.find_all("div",class_="_30jeq3 _1_WHN1")

    for i in price:
        name=i.text[1:].replace(',', '.')  
        prices.append(float(name))  
    desc=box.find_all("ul",class_="_1xgFaf")

    for i in desc:
        name=i.text
        description.append(name)

    df=pd.DataFrame({"Product Name":product_name,"Prices":prices,"Description":description})
    df.to_csv("flipkart_mobiles.csv")
    print('lol')

    if 'Prices' in df.columns and df['Prices'].dtype == 'float64' and df['Prices'].min() < 6:
        
        smt=smtplib.SMTP('smtp.gmail.com',587)
        smt.ehlo()
        smt.starttls()
        smt.login('ruihungry@gmail.com', 'qrrqtinwyaibmeao')
        smt.sendmail('ruihungry@gmail.com',
                     'ashnagandhi14@gmail.com',
                     f"Subject:Price notifier\n\nHi.Price has dropped to {df['Prices'].min():.2f}k.buy it!")
        smt.quit()


print("done")
