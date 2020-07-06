import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_URL = "https://manchester.craigslist.org/search/sss?query={}"
IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"


# Create your views here.
def home(request):
    return render(request,'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search = search)
    final_url = BASE_URL.format(quote_plus(search))
    response= requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features= 'html.parser')

    post_listings = soup.find_all('li',{'class':'result-row'})
    
    final_postings= []
    
    for post in post_listings:
        post_title= post.find(class_= 'result-title').text
        post_url= post.find('a').get('href')
        if post.find(class_= 'result-price'):
         post_price= post.find(class_= 'result-price').text
        else:
         post_price = "n/a"

        if post.find(class_= 'result-image').get('data-ids'):
             post_image = post.find(class_= 'result-image').get('data-ids').split(',')[0].split(':')[1]
             final_image = IMAGE_URL.format(post_image)
        else:
            final_image = "https://images-wixmp-530a50041672c69d335ba4cf.wixmp.com/templates/image/b77fe464cfc445da9003a5383a3e1acf.jpg/v1/fill/w_322,h_182,q_90,usm_0.60_1.00_0.01/b77fe464cfc445da9003a5383a3e1acf.jpg"#




        final_postings.append((post_title,post_url,post_price,final_image))


    frontend_stuff = {
        'search':search,
        'final_postings':final_postings,   
    }

    return render(request,'shopping/new_search.html',frontend_stuff)