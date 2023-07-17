#-----------LIBS---------#
import random
import requests
from bs4 import BeautifulSoup as bsoup
import urllib3
import threading
import time
#------------------------#


#-----------SYSTEM---------#
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#--------------------------#


#--------VARIABLES---------#
ua_file_path = "useragents.txt"


dm_file_path = "dork//domain.txt"
kw_file_path = "dork//keywords.txt"
ext_file_path = "dork//pageext.txt"
pt_file_path = "dork//pagetypes.txt"

http_proxy = 'brd-customer-hl_733ecf85-zone-web_unlocker1:nc89mm6t15cd@brd.superproxy.io:22225/'
#--------------------------#

#--------------------------#
RESULT_URLS = []
MAX_URLS_TO_SCRAPE= 1000
#--------------------------#

def randomDm():
    with open(dm_file_path, 'r') as file:return random.choice(file.readlines()).strip()
def randomKw():
   with open(kw_file_path, 'r') as file:return random.choice(file.readlines()).strip()
def randomEx():
   with open(ext_file_path, 'r') as file:return random.choice(file.readlines()).strip()
def randomPt():
   with open(pt_file_path, 'r') as file:return random.choice(file.readlines()).strip()


def randomUserAgent(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if not lines:
            return None
        random_line = random.choice(lines).strip()
        return random_line


def google_search(query, page):
    base_url = 'https://www.google.com/search'
    headers  = { 'User-Agent':randomUserAgent(ua_file_path) }
    params   = { 'q': query, 'start': page * 10 }
    s = requests.Session()
    proxy = {'http': f'http://{http_proxy}','https':f'http://{http_proxy}'}
    resp = s.get(base_url, params=params, headers=headers,proxies=proxy,verify=False)

    s.close()
    soup = bsoup(resp.text, 'html.parser')
    links = soup.findAll("div", { "class" : "yuRUbf" })
    result = []
    for link in links:
        if "?" in link.find('a').get('href'):
            RESULT_URLS.append(link.find('a').get('href'))



def generateDork():
    return "inurl:" + randomEx() + randomPt() +' "'+ randomKw() +'" site:' + randomDm()

def print_progress():
    while True:
        urls_scraped = len(RESULT_URLS)
        print(f"URLs Scraped: {urls_scraped}/{MAX_URLS_TO_SCRAPE}")
        time.sleep(1)

# Function to perform the search and scraping using threads
def search_and_scrape_with_threads(query_generator, search_function):
    threads = []
    urls_scraped = 0
    max_pages_per_thread = 1
    progress_thread = threading.Thread(target=print_progress)
    progress_thread.start()

    while urls_scraped < MAX_URLS_TO_SCRAPE:
        query = query_generator()
        for thread_num in range(25):  # We will use 5 threads
            start_page = thread_num * max_pages_per_thread
            for page in range(start_page, start_page + max_pages_per_thread):
                t = threading.Thread(target=search_function, args=(query, page))
                t.start()
                threads.append(t)

        # Wait for all threads to finish before generating the next query
        for t in threads:
            t.join()

        urls_scraped += len(RESULT_URLS)
        if urls_scraped >= MAX_URLS_TO_SCRAPE:
            break
    with open("scraped.txt", "w") as file:
        for url in RESULT_URLS:
            file.write(url + "\n")
    # Save the URLs in the RESULT_URLS list to the file (if needed)
    # ...

    # Wait for the progress thread to finish
    progress_thread.join()


search_and_scrape_with_threads(generateDork, google_search)
