# Step 1
# pip install requests
# pip install html5lib
# pip install bs4
# or use conda instead of pip
# conda install -n web_scrap ipykernel --update-deps --force-reinstall

import requests
from bs4 import BeautifulSoup
# get html
url = "https://en.wikipedia.org"
r = requests.get(url)
htmlcontent = r.content
# print(htmlcontent)

# Parse Html
soup = BeautifulSoup(r.content, 'html.parser')
# print(soup.prettify())


# Traverse html
# print(type(soup.title)) # 1. Tag
# print(type(soup)) # 2. BeautifulSoup
# print(type(soup.title.string)) # 3. NavigableString

# get the title of htmlpage
title = soup.title
# get all paras
paras = soup.find_all('p')
# print(paras)
# get all anchor
atg = soup.find_all('a')
# print(atg)


# get first para
# print(soup.find('p'))
# get first para class
# print(soup.find('p')['class'])

# find element with class mt-2
# print(soup.find('p',class_="mt-2"))


# find all element with class text-sm
# print(soup.find_all('p',class_="text-sm"))

all_links = set()
# get all the links on the page
for link in atg:
    all_links.add(link.get('href'))

# for link in all_links:
#     print(link)

# 4. Comment
html_c = "<p><!-- It is comment --></p>"
soup2 = BeautifulSoup(html_c, 'html.parser')
print(type(soup2.p.string))
