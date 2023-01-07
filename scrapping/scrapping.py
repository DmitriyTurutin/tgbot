#!/usr/bin/env python
# coding: utf-8

# Web scrapping hookah work website
# ---
# 
# ## TODOS: 
# - Распарсить страничку, получить из неё данные
# - Добавить эти данные в базу данных 
# 
# Парсинг
# ---
# 
# **В превую очередь**
# - Вход в crm'ку с помощью selenium — **done**
# - Сохранить данные продаж 
#   - перейти на вкладку sales с помощью selenium — **done**
#   - распарсить табличку (пока max 10 штук) — **done**
#   - создать таблицу в базе данных с названиями столбцов как на странице — **done**
#   - добавить данные таблички в таблицу базы данных — **done**
# 
# 05.01.23
# 
# - С помощью сервера как-то обновить данные таблицы — *to-do*

# ### Выручка за день

# In[83]:


import requests
from bs4 import BeautifulSoup
# import selenium to automate login part
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import os


# #### Вход с selenium

# In[84]:


driver = webdriver.Firefox()
# Refactor to use os.environ
driver.get("https://lab3.hookah.work/sales")
email = driver.find_element(By.ID, 'loginform-email')
password = driver.find_element(By.ID, 'loginform-password')
email.send_keys("lab3.bd@yandex.ru")
password.send_keys("bdpassword")

submit = driver.find_element(By.CLASS_NAME, 'btn-primary')
submit.click()

time.sleep(1)
sales = driver.find_element(By.LINK_TEXT, 'Продажи') 
sales.click()
time.sleep(2)

html = driver.page_source


# #### Распарсить табличку

# In[85]:


soup = BeautifulSoup(html, 'html.parser')

# Find all tr element with class 'odd' or 'even'
rows = soup.find_all('tr', class_=['odd', 'even'])


# #### Add table contents to postgresql database

# ✓ Bootstrap postgres and pg admin using docker-compose
# 
# ✓ Connect to db using python 
# - Write data to db

# Connect to the database

# In[86]:


import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="myuser",
    password="mypass",
    database="mydb"
)


# Create table if not exists

# In[87]:


create_table_statement = f"""
CREATE TABLE IF NOT EXISTS sales (
    title text,
    price  real,
    amount integer,
    payment_method text,
    client text,
    time_added timestamp NOT NULL PRIMARY KEY 
)
"""
cur = conn.cursor()
cur.execute(create_table_statement)
conn.commit()
cur.close()


# Insert sales table items to database table

# In[88]:


import re
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

to_parse = ""

for row in rows:
    tds = row.find_all('td')
    title = tds[1].text.strip()
    price = float(tds[4].text.strip())
    amount = int(re.search(r'\d', tds[3].text.strip()).group())
    payment_method = tds[5].text.strip()
    client = ""
    time_added_unformatted = tds[12].text.strip()
    to_parse = time_added_unformatted

    try:
        # Parse the string as a timestamp using the updated format string
        time_added = datetime.strptime(time_added_unformatted, "%d %b. %Y г., %H:%M:%S")
    except ValueError:
        # Handle the ValueError exception
        print(f"Unable to parse timestamp: {time_added_unformatted}")
        continue

    insert_statement = """
    INSERT INTO sales (title, price, amount, payment_method, client, time_added) 
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (time_added) DO NOTHING;
    """

    cur = conn.cursor()

    cur.execute(insert_statement, (
        title, 
        price,
        amount,
        payment_method,
        client,
        time_added))

    cur.close()
    conn.commit()


# Check table 

# In[89]:


cur = conn.cursor()

cur.execute("SELECT * FROM sales")

rows = cur.fetchall()

for row in rows:
    print(row)


cur.close()


# Create excel file from database table

# In[ ]:


import pandas as pd
cur = conn.cursor()

cur.execute("SELECT * FROM sales")

data = cur.fetchall()

columns = [desc[0] for desc in cur.description]

df = pd.DataFrame(data, columns)

df.to_excel


# Close connection

# In[90]:


conn.close()

