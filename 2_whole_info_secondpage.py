from selenium import webdriver
from bs4 import BeautifulSoup
import random
import pandas as pd

UserAgent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

def addsExtract(tempo_soup):
    address_links = list()
    # Set waiting time to avoid high traffic
    browser.implicitly_wait(random.randint(1, 2))

    try:
        collect_add = tempo_soup.find('dl', {'class':'ui-ncbi-toggler-slave-open ui-ncbitoggler ui-ncbitoggler-slave-open'}).find_all('dd')
        for single in collect_add:
            address_links.append(single.get_text())
    except:
        address_links = 'N'

    return address_links

def datesExtract(tempo_soup):
    browser.implicitly_wait(random.randint(2, 3))
    try:
        collect_time = tempo_soup.select('div.cit')[0].get_text()
    except:
        collect_time = 'N'

    return collect_time

def absExtract(tempo_soup):
    browser.implicitly_wait(random.randint(2, 3))
    try:
        collect_abs = tempo_soup.find('div', {'class': 'abstr'}).find('p').get_text()
    except:
        collect_abs = 'N'

    return collect_abs

def keywdsExtract(tempo_soup):
    browser.implicitly_wait(random.randint(2, 3))
    try:
        collect_keywds = tempo_soup.find('div', {'class': 'keywords'}).find('p').get_text()
    except:
        collect_keywds = 'N'

    return collect_keywds

browser = webdriver.Chrome('chromedriver.exe')
address=list()
pmids=list()
dates=list()
abs=list()
keywds=list()

links = pd.read_csv('pub_links_in.csv', low_memory=False, header=None).values.flatten()
PMID = pd.read_csv('pub_links_in.csv', low_memory=False, header=None)
ID = PMID[PMID.columns[0]].map(lambda x : x.lstrip('/pubmed/'))

for (cnt, i) in enumerate(links):
    url = 'https://www.ncbi.nlm.nih.gov{}'.format(i)

    # Get target page information
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "lxml")
    address.append(addsExtract(soup))
    dates.append(datesExtract(soup))
    abs.append(absExtract(soup))
    keywds.append(keywdsExtract(soup))
    pmids.append(ID[cnt])

### stop at 30743248, 30717497 doesn't work

whole_info = pd.DataFrame(
    {'add': address,
     'id': pmids,
     'abstract': abs,
     'Keywords': keywds,
     'date': dates,
    })
whole_info.to_csv("whole_info_cn.csv", encoding='utf-8', index=False)

with open('address_cn.csv', "w+", encoding='utf-8') as file:
    for item in address:
        file.write("{}\n\n".format('\n'.join(item)))
### address_cn.csv will use regex to clear before adding GIS info
