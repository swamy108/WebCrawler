from django.shortcuts import render
from django.template.context_processors import csrf
# Create your views here.
from crawler.models import Images

import urllib
from html.parser import HTMLParser
from crawler.pycrawler import Crawler

urlText = []
def home_page(request):
	context = {};
	context.update(csrf(request));
	return render(request, "home.html", context);
	
def start_crawl(request):
	url = request.POST['url'];
	depth = request.POST['depth'];
	data = {'url' : url, 'depth' : depth};
	
	crawler = Crawler();
	crawler.web_crawler(data);
	
	print("In Views : "+ str(Images.imageSrcs));
	data['images'] = Images.imageSrcs;
	return render(request, "results.html", data);