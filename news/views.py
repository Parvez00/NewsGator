from django.shortcuts import render
from django.http import HttpResponse

from bs4 import BeautifulSoup
import requests

from news.models import NewsDomainLink, NewsSite
from user.models import NewsPreference, NewsDomain

# def news_scrap(request, domain):
#     all_news = {}
#     url = "https://www.bbc.com/news/" + domain
#     r = requests.get(url)
#     htmlContent = r.content
#     soup = BeautifulSoup(htmlContent,'html.parser')
#     parent_div = soup.find_all("a", class_="gs-c-promo-heading")

#     news_count = 1

#     for parent in parent_div:
#         news_link = parent['href']
#         all_headings = parent.find('h3')
#         news_heading = all_headings.text

#         if (news_link[:5] != 'https'):
#             news_link = "https://www.bbc.com" + news_link
        
#         all_news[news_count] = [news_link,news_heading]

#         news_count += 1
    
#     dicts = {}
#     dicts['data'] =  all_news
    

#     print(dicts['data'])

#     return render(request,"news.html",dicts)


def user_home_view(request,user_id):
    send_context = {}
    menu = MenuItems(user_id)
    send_context['menu_items'] = menu.send_menu_items()
    return render(request, "news/home_page.html", send_context)

class MenuItems():
    def __init__(self,user_id):
        self.user_id = user_id

    def send_menu_items(self):
        menu_items = {}
        user_news_preference = NewsPreference.objects.filter(user_id=self.user_id, is_active=1).values_list('news_preference', flat=True)
        user_news_preference = list(user_news_preference)
        user_news_preference = user_news_preference[0].split(",")

        for domain_id in user_news_preference:
            news_domain = NewsDomain.objects.filter(id=domain_id, is_active=1).values()
            menu_items[news_domain[0]['id']] = news_domain[0]['domain_name']

        return menu_items



def news_scrap(request, domain):
    user = request.user
    all_news = {}
    main_news_data = {}
    sub_news_data = {}

    menu = MenuItems(user.id)
    all_news['menu_items'] = menu.send_menu_items()

    main_news_count = 1
    sub_news_count = 1

    news = Scrapper(domain)

    kaler_kantho_data = news.scrap_kaler_kantho()
    inquilab_data = news.scrap_inquilab()

    # print(kaler_kantho_data['main_news'])

    for main_news_detail in kaler_kantho_data['main_news']:
        main_news_data[main_news_count] = main_news_detail
        main_news_count+=1

    for main_news_detail in inquilab_data['main_news']:
        main_news_data[main_news_count] = main_news_detail
        main_news_count+=1

    for sub_news_detail in kaler_kantho_data['sub_news']:
        sub_news_data[sub_news_count] = sub_news_detail
        sub_news_count+=1

    all_news['main_news'] = main_news_data
    all_news['sub_news'] = sub_news_data


    return render(request,"news/news_page.html",all_news)


class Scrapper():
    def __init__(self, domain):
        self.domain_id = domain

    def scrap_kaler_kantho(self):
        main_news = []
        sub_news = []
        all_news= {}
        site_info = NewsSite.objects.filter(id = 1, is_active = 1).values_list('id', flat=True)
        site_info = list(site_info)
        url = NewsDomainLink.objects.filter(domain_id=self.domain_id, site_id=site_info[0], is_active = 1).values_list('domain_url', 'domain_slug')
        url = list(url)

        site_loader = requests.get(url[0][0])
        htmlContent = site_loader.content
        soup = BeautifulSoup(htmlContent,'html.parser')

        main_parent_divs = soup.find_all("div", class_="card border-0")

        for parent in main_parent_divs:
            news_link = parent.find('a')
            news_url = news_link['href']
            
            news_heading = parent.find('h4')
            news_heading_text = news_heading.text

            news_image = parent.find('img')
            news_image_url = news_image['src']

            main_news.append([news_heading_text,news_url,news_image_url])

        sub_parent_divs = soup.find_all("li", class_="list-group-item")

        for sub_parent in sub_parent_divs:
            news_link = sub_parent.find('a')
            news_url = news_link['href']
            news_slug = news_url.split("/")
            if(news_slug[2] == url[0][1]):
                news_heading = sub_parent.find('h5')
                news_heading_text = news_heading.text
                sub_news.append([news_heading_text,news_url])

        all_news['main_news'] = main_news
        all_news['sub_news'] = sub_news

        return all_news

    def scrap_inquilab(self):
        main_news = []
        sub_news = []
        all_news= {}

        site_info = NewsSite.objects.filter(id = 2, is_active = 1).values_list('id', flat=True)
        site_info = list(site_info)
        url = NewsDomainLink.objects.filter(domain_id=self.domain_id, site_id=site_info[0], is_active = 1).values_list('domain_url', 'domain_slug')
        url = list(url)

        site_loader = requests.get(url[0][0])
        htmlContent = site_loader.content
        soup = BeautifulSoup(htmlContent,'html.parser')

        root_divs = soup.find("div", class_="row news_list")

        main_parent_divs = root_divs.find_all("a")

        for parent in main_parent_divs:
            news_url = parent['href']

            news_heading = parent.find('h2')
            news_heading_text = news_heading.text

            news_image = parent.find('img')

            news_image_url = None

            if news_image is not None:
                news_image_url = news_image['src']

            main_news.append([news_heading_text,news_url,news_image_url])

            all_news['main_news'] = main_news

            return all_news


        




