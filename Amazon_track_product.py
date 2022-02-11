import csv
import datetime

def check_price():
    URL = 'https://www.amazon.ca/Retractable-Barrier-Case-CCW-WMB-230-Yellow/dp/B07VVMFN4Z/ref=sr_1_3_sspa?crid=29GFXKJ89B66Y&keywords=stanchions&qid=1643866797&sprefix=stanchi%2Caps%2C341&sr=8-3-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzQUxIUDhaVldTVlExJmVuY3J5cHRlZElkPUEwMzE2MzQ3MzZaVksyWEZHMFZQMCZlbmNyeXB0ZWRBZElkPUEwMTU2ODEzMzVHOEVBN1pQSTA0QSZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU&th=1'

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id='productTitle').get_text()
    price = soup2.find(id='priceblock_ourprice').get_text()
    print(title)
    price = price.strip()[1:]
    title = title.strip()



    today = datetime.date.today()



    header = ['Title', 'Price', 'Date']
    data = [title, price, today]
    print(data)

    with open('C:/Users/suen6/PycharmProjects/amazon scraper/data/AmazonWebScraperDataset.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        for row in data:
            writer.writerow(data)