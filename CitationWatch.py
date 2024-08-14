import pystray
import PIL.Image
import sys
import requests
from bs4 import BeautifulSoup
import webbrowser 
import time
import threading

author = "Author Name"
author_url = 'https://scholar.google.com/citations?user=' #author google shcolar URL

def get_citation_data(author_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(author_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    citations = soup.find('td', string='Citations')
    
    if citations:
        citation_count = citations.find_next_sibling('td').text
        return citation_count
    else:
        return "Citation data not found"

citations = get_citation_data(author_url)
Run = True

image = PIL.Image.open("logo.png")

def open_browser(icon, item):
    webbrowser.open(author_url)

def close(icon, item):
    global Run
    icon.stop()
    Run = False

icon = pystray.Icon(name=author, title=author + ": "+ citations, icon=image, menu=pystray.Menu(
    pystray.MenuItem("View Profile", open_browser),
    pystray.MenuItem("Close", close)
))

def update_citations(a):
    global citations
    global Run
    global icon
    while Run:
        newcitations = get_citation_data(author_url)
        if newcitations != citations:
            citations = newcitations
            icon.notify('Author: ' + author + '\nHas ' + str(citations) + " citations", title="Citation Update:")
            icon.title = author + ": "+ str(citations)
            time.sleep(3600)
            

def main():
    threading.Thread(target=update_citations, args=(icon,)).start()
    icon.run()

if __name__ == "__main__":
    main()
