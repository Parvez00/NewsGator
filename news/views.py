from django.shortcuts import render
from django.http import HttpResponse

from bs4 import BeautifulSoup
import requests

from apyori import apriori

from news.models import NewsDomainLink, NewsSite
from user.models import NewsPreference, NewsDomain

import pandas as pd

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

def user_home_view(request,user_id):
    send_context = {}
    menu = MenuItems(user_id)
    send_context['menu_items'] = menu.send_menu_items()
    return render(request, "news/home_page.html", send_context)



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
    domain_name_class = DomainName(domain)
    domain_name =  domain_name_class.domain_info()

    kaler_kantho_data = news.scrap_kaler_kantho()
    inquilab_data = news.scrap_inquilab()


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
    all_news['domain_name'] = domain_name
    all_news['user'] = user

    min_support = 0.10
    confidence = 0.50
    min_lift = 1.1

    recommendation = Recommendation(user.id,min_support,confidence,min_lift)
    recommended_items = recommendation.get_recommendation()
    all_news['recommendation'] = recommended_items

    return render(request,"news/news_page.html",all_news)


class DomainName():
    def __init__(self, domain):
        self.domain_id = domain

    def domain_info(self):
        domain_name = NewsDomain.objects.filter(id = self.domain_id, is_active = 1).values_list('domain_name', flat=True)
        domain_name = list(domain_name)
        domain_name = domain_name[0]
        return domain_name

class Scrapper():
    def __init__(self, domain):
        self.domain_id = domain
        self.no_img_available = "/media/no-img.jpg"

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
            news_url = "https://www.kalerkantho.com"+news_link['href']
            
            news_heading = parent.find('h4')
            news_heading_text = news_heading.text

            news_image = parent.find('img')
            news_image_url = "https://www.kalerkantho.com"+news_image['src']

            main_news.append([news_heading_text,news_url,news_image_url,'কালের কণ্ঠ'])

        sub_parent_divs = soup.find_all("li", class_="list-group-item")

        for sub_parent in sub_parent_divs:
            news_link = sub_parent.find('a')
            news_url_for_check = news_link['href']
            news_url = "https://www.kalerkantho.com"+news_link['href']
            news_slug = news_url_for_check.split("/")
            if((news_slug[2] == url[0][1]) or (news_slug[2] == (url[0][1]).capitalize())):
                news_heading = sub_parent.find('h5')
                news_heading_text = news_heading.text
                sub_news.append([news_heading_text,news_url,self.no_img_available,'কালের কণ্ঠ'])

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

        root_divs_in = soup.find("div", class_="row news_list")

        main_parent_divs_in = root_divs_in.find_all("a")


        for parent_in in main_parent_divs_in:
            news_url = parent_in['href']

            news_heading = parent_in.find('h2')
            news_heading_text = news_heading.text

            news_image = parent_in.find('img')

            if news_image is not None:
                news_image_url = news_image['src']
                main_news.append([news_heading_text,news_url,news_image_url,'ইনকিলাব'])
            else:
                main_news.append([news_heading_text,news_url,self.no_img_available,'ইনকিলাব'])

        all_news['main_news'] = main_news

        return all_news


class Recommendation():
    def __init__(self,user_id,min_support,confidence,min_lift):
        self.user_id = user_id
        self.min_support = min_support
        self.confidence = confidence
        self.min_lift = min_lift

    def get_recommendation(self):
        news_domains = NewsDomain.objects.all().values_list('id', flat=True)
        news_domains = list(news_domains)
        news_domains = map(str, news_domains)
        news_domains = list(news_domains)


        user_preferences = NewsPreference.objects.filter(user_id=self.user_id, is_active=1).values_list('news_preference', flat=True)
        user_news_preference = list(user_preferences)
        user_news_preference = user_news_preference[0].split(",")

        all_preferences = NewsPreference.objects.all().values_list('news_preference', flat=True)
        all_preferences = list(all_preferences)

        all_preferred_combination = []

        min_length = len(user_news_preference) + 1
        
        for domain_ids in all_preferences:
            all_preferred_combination.append(domain_ids.split(","))

        association_rules = apriori(all_preferred_combination, 
                        min_support = self.min_support,
                        min_confidence = self.confidence,
                        min_lift = self.min_lift,
                        min_length = 2)

        association_results = list(association_rules)

        all_items = []

        for results in association_results:
            items = list(results.items)
            if len(items) >= min_length:
                for item in items:
                    all_items.append(item)

        all_items = list(dict.fromkeys(all_items))

        if len(all_items) == 0:
            recommended_items = list(set(user_news_preference).symmetric_difference(set(news_domains)))

        else:
            recommended_items = list(set(user_news_preference).symmetric_difference(set(all_items)))

        recommended_items_detail = NewsDomain.objects.filter(id__in=recommended_items).values()

        return recommended_items_detail




    



        




