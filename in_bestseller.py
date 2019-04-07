import requests
import csv
from bs4 import BeautifulSoup
name = ["Name"]
avgrate = ["Average Rating"]
writer = ["Author"]
novlink = ["URL"]
paisa = ["Price"]
nom = ["Number of Ratings"]


def spider(max_pages):
    page = 1
    while page <= max_pages:

        url = 'https://www.amazon.in/gp/bestsellers/books/ref = zg_bs_pg_'
        url += str(page)+'/258-6664636-5080305?ie = UTF8&pg = '+str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        for link in soup.findAll('div', {'class': 'zg_itemImmersion'}):
            href = link.find('a')
            if(link.find('a')):
                book_link = 'https://www.amazon.in'+href.get('href')
            else:
                book_link = "Not available"
            str_short = 'p13n-sc-truncate p13n-sc-line-clamp-1'
            if(link.find('div', {'class': str_short})):
                title = link.find('div', {'class': str_short}).string
                title = title.split(' ')
                while '' in title:
                    title.pop(title.index(''))
                title = ' '.join(title)
                title = title.strip('\n')
            else:
                title = "Not available"
            if(link.find('div', {'class': 'a-row a-size-small'})):
                short = 'a-row a-size-small'
                author = link.find('div', {'class': short}).string
            else:
                author = "Not available"
            if(link.find('div', {'class': 'a-icon-row a-spacing-none'})):
                short = 'a-icon-row a-spacing-none'
                ratings = link.find('div', {'class': short}).find('i').string
            else:
                ratings = "Not available"
            if(link.find('a', {'class': 'a-size-small a-link-normal'})):
                short = 'a-size-small a-link-normal'
                reviews = link.find('a', {'class': short}).string
            else:
                reviews = "Not available"
            key_word = 'a-link-normal a-text-normal'
            if(link.find('a', {'class': key_word})):
                price = link.find('a', {'class': key_word})
                short = 'p13n-sc-price'
                price = price.find('span', {'class': short}).getText()
            else:
                price = "Not available"
            name.append(title)
            writer.append(author)
            avgrate.append(ratings)
            novlink.append(book_link)
            paisa.append(price)
            nom.append(reviews)
        page += 1


def other(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

spider(5)
rows = zip(name, novlink, writer, paisa, nom, avgrate)
csvfile = "output/in_book.csv"
with open(csvfile, "w") as output:
    writ = csv.writer(output, delimiter=";")
    for row in rows:
        writ.writerow(row)
