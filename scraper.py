# Amazon Price scraper and an auto mailer in Python App
import requests
from bs4 import BeautifulSoup
import re
import smtplib

url = "https://www.amazon.in/gp/product/B07DJCN7C4/ref=s9_acss_bw_cg_Top_4b1_w?pf_rd_m=A1K21FY43GMZF8&pf" \
      "_rd_s=merchandised-search-5&pf_rd_r=X4D57A3PAJ9DGCGG07KS&pf_rd_t=101&pf_rd" \
      "_p=50e8253f-cd32-4485-86db-b433363f7609&pf_rd_i=6294306031"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " snap Chromium/76.0.3809.87 Chrome/76.0.3809.87 Safari/537.36"
}

req = requests.Session()
res = req.get(url, headers=headers)

# print(res.text)


def get_price():
    soup = BeautifulSoup(res.text, features='html.parser')
    # finding price
    price = soup.find(id='priceblock_ourprice').get_text()
    # removing comma and rupee sign we will be using regex
    price = float(re.sub(',', '', price[2:]))
    title = soup.find(id="productTitle").get_text()
    title = title.strip()
    print('Product:', title)

    # Now when the product price is lessthan the quoted price send a mail
    max_price = float(input("Enter the maximum price:"))
    if price < max_price:
        send_mail(price, title)
    else:
        print(f"Price still high --> {price}")


def send_mail(price, title):
    # Using gmail for sending the mail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # for login we will use google apps password
    try:
        server.login('guyled321@gmail.com', password='rwcmgyilyxgkekfd')
        subject = "Prices are falling Down!! :D"
        body = f"The price for this amazon product has come down \n\n Title - {title} \n\n Price - {price} \n\n Link - {url}"

        msg = f"subject: {subject} \n\n {body}"

        # now sending the mail
        server.sendmail(
            'guyled321@gmail.com',
            'guyled321@gmail.com',
            msg
        )
        print("Email Sent!!")
    except:
        print("Some error occured!!")


get_price()
