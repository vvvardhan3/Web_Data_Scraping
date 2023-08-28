from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import pandas as pd
import time
driver = webdriver.Chrome()
driver.get("https://www.ebay.com/")
search_box = driver.find_element(By.ID,'gh-ac')
search_box.send_keys('Electronics')

search_btn = driver.find_element(By.ID,'gh-btn')
search_btn.click()

def get_next_btn():
    next_btn = None
    try:
        next_btn = driver.find_element(By.CLASS_NAME,'pagination__next')
    except:
        pass
    return next_btn

items = driver.find_elements(By.CLASS_NAME,'s-item')

item_list=[]
counter = 1
while True:
    items = driver.find_elements(By.CLASS_NAME,'s-item')
    for i,item in enumerate(items):
        print('scraping item - ', i+1)
        try:
            item_details={}
            e_title = item.find_element(By.CLASS_NAME,'s-item__link')
            title = e_title.text
            item_details['Title'] = title

            item_link = e_title.get_attribute('href')
            item_details['Item link'] = item_link

            e_price = item.find_element(By.CLASS_NAME,'s-item__price')
            price = e_price.text
            item_details['Price'] = price

            e_shipping = item.find_element(By.CLASS_NAME,'s-item__shipping')
            shipping = e_shipping.text
            item_details['Shipping'] = shipping
            item_list.append(item_details)
        except Exception as ex:
            print(ex)


    next_btn = get_next_btn()
    if next_btn is not None:
         classes = next_btn.get_attribute('class')
         if 'icon-link' not in classes:
              break
         else:
              counter += 1
              if counter == 4:
                   break
              next_btn.click()
              time.sleep(3)

df = pd.DataFrame(item_list)
df.to_csv('Ebay_Scraped_Data.csv')