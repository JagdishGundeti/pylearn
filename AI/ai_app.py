import requests
import csv
from bs4 import BeautifulSoup

# Set the URL of the page you want to scrape
url = "http://books.toscrape.com/"

# Send an HTTP request to the URL
response = requests.get(url)

# Parse the HTML of the page
soup = BeautifulSoup(response.text, "html.parser")

# Find all the div elements with the class "product_pod"
products = soup.find_all("article", class_="product_pod")

# Open a CSV file for writing
with open("books.csv", "w", newline="", encoding="utf-8") as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)

    # Write the headers to the CSV file
    writer.writerow(["Title", "Price", "Link"])

    # Iterate through the products and extract the data we want
    for product in products:
        # Find the title element and extract the text
        title = product.h3.a.text

        # Find the price element and extract the text
        price = product.find("p", class_="price_color").text

        # Find the link element and extract the URL
        link = product.h3.a["href"]

        # Write the data to the CSV file
        writer.writerow([title, price, link])
