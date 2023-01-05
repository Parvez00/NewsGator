from django.shortcuts import render
from django.http import HttpResponse

from bs4 import BeautifulSoup
import requests


def news_scrap(request, domain):
    all_news = {}
    url = "https://www.bbc.com/news/" + domain
    r = requests.get(url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent,'html.parser')
    parent_div = soup.find_all("a", class_="gs-c-promo-heading")

    news_count = 1

    for parent in parent_div:
        news_link = parent['href']
        all_headings = parent.find('h3')
        news_heading = all_headings.text

        if (news_link[:5] != 'https'):
            news_link = "https://www.bbc.com" + news_link
        
        all_news[news_count] = [news_link,news_heading]

        news_count += 1
    
    dicts = {}
    dicts['data'] =  all_news
    

    print(dicts['data'])

    return render(request,"news.html",dicts)


