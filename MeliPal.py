"""
 MeliPal  is a MercadoLibre.com.ar web scraper that gathers data for Item Name, Item Price, Item Location 
 from the items that come as a result of user search (input) and save it in an excel file through a pandas dataframe.

 The goal is to use that data for price and location analysis.  

 Some items are not supported yet, like some home appliances, but for most things it works!

 Use at your own risk, I don't think MeLi would like to know this is available to anyone :)
"""


import bs4
from urllib.request import urlopen as siterequest
from bs4 import BeautifulSoup as soup
import pandas as pd


# Variables to format URL
interest = input('Input your search keywords: ')
interestHyphen = interest.replace(' ','+')
pageCount = 1

# Dataframe to store data
column_names = ["productName", "productPrice", 'productLocation']
grid = pd.DataFrame(columns = column_names)

# Start URL
url = f"https://listado.mercadolibre.com.ar/{interestHyphen}_Desde_0_DisplayType_G"

while url is not None:
    # Connect to website, Get website HTML then close connection
    website = siterequest(url)
    websitehtml = website.read()
    page_soup = soup(websitehtml, "html.parser") 
    website.close()

    # Get relevant chunks of HTML
    containers = page_soup.findAll("div",{"class":"ui-search-result__content-wrapper"})
    
    # Notification
    print(f'Scraping page {str(pageCount)}...')
   
    # From relevant HTML chunks, get the name and price of each item
    for eachContainer in containers:
        itemName = eachContainer.find("h2", class_="ui-search-item__title ui-search-item__group__element").text
        
        # Get Price of Item:
        try:
            itemPrice = eachContainer.find("span", class_="price-tag-fraction").text.replace('.','')
        
        except:

            itemPrice = 'Price Could not be extracted'

        # Get Location of Item:
        try:
            itemLocation = eachContainer.find("span", {"class": "ui-search-item__group__element ui-search-item__details"}).text.replace(' - ','-')
                       
        except:            
            itemLocation = 'No Data'
                   
        # Add found items to DataFrame
        newrow = [itemName, itemPrice, itemLocation]
        print(newrow)
        grid.loc[len(grid)] = newrow


# Find Next page button based on the "Siguiente" title text and extract URL:
    try:
        nextPage = page_soup.find_all("a", title="Siguiente")[0]['href']
        url = nextPage
        pageCount += 1
        
        
    except:
        url = None
        print('Reached last page.')
   
 
# Report findings
print(f'Gathered {len(grid)-1} items from {pageCount} pages.')

# Fill blanks with 'No Data' Save dataframe to Excel

grid.fillna('No Data')
grid.to_excel(f'{interestHyphen}.xlsx', index=False)
