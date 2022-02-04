import csv
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#Generate a url from search term
def get_url(search_term):
    template = 'https://www.amazon.ca/s?k={}&crid=1K0C38AZEX0M5&sprefix=stanc%2Caps%2C493&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ','+')

    #add term query to url
    url = template.format(search_term)

    #add page query placeholder
    url += '&page{}'

    return url

def num_there(s):
    return any(i.isdigit() for i in s)

def extract_record(item):
    #description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.ca' + atag.get('href')

    #extract quantity from description
    try:
        quantity = ''
        line = re.sub('[\(\)]', '', description).lower()
        name = line.split()
        # quatity identifiers
        keywords = ['pack', 'pcs']
        for word in name:
            for keyword in keywords:
                if keyword in word:
                    # check 'pack'
                    if word == keywords[0]:
                        i = name.index(word)
                        quantity = name[i + 2]
                    # check 'pcs'
                    elif keywords[1] in word:
                        # remove 'pcs' text
                        if num_there(word):
                            quantity = re.sub('[pcs]', '', word)
                        # in case quantity and 'pcs' are separated
                        else:
                            i = name.index(word)
                            quantity = name[i - 1]
                    else:
                        pass
    except AttributeError:
        quantity = ''

    #extract price
    try:
        price = item.find('span', 'a-price-whole').text
    except AttributeError:
        return

    #extract rating
    try:
        #remove out of 5 text
        rating = item.i.text[:-15]
        #use full name of class to prevent using stock volume
        review_count = item.find('span', {'class': 'a-size-base s-underline-text'}).text
    except AttributeError:
        rating = ''
        review_count = ''

    #create tupple
    result = (description, quantity, price, rating, review_count, url)

    return result

def main(search_term):
    #start webdriver
    #download chromedriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    records = []
    url = get_url(search_term)

    #search all available 20 pages
    for page in range(1, 2):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div',{'data-component-type':'s-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()

    #save data to csv file
    with open('C:/Users/suen6/PycharmProjects/amazon scraper/data/amazon_data5.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Quantity', 'Price', 'Rating', 'Review Count', 'Url'])
        for row in records:
            writer.writerow(row)

main('stanchions')

