import requests
from bs4 import BeautifulSoup

# Set the URL of the page you want to scrape
url = "http://books.toscrape.com/"

# Send an HTTP request to the URL
response = requests.get(url)

# Parse the HTML of the page
soup = BeautifulSoup(response.text, "html.parser")

# Find all the div elements with the class "product_pod"
products = soup.find_all("article", class_="product_pod")

# Iterate through the products and extract the data we want
for product in products:
    # Find the title element and extract the text
    title = product.h3.a.text

    # Find the price element and extract the text
    price = product.find("p", class_="price_color").text

    # Find the link element and extract the URL
    link = product.h3.a["href"]

    # Print the data
    print(f"Title: {title}\nPrice: {price}\nLink: {link}\n---")
