from django.db import models
from html.parser import HTMLParser
from urllib.parse import urlparse

# Create your models here.
class Images:
	imageSrcs = list();
	def add_to_imageSrcs(self, src):
		if(src not in self.imageSrcs):
			Images.imageSrcs.append(src);

	def set_image_url(self, tag, attrs):
		imgSrc = '';
#		print("Start tag:", tag)
		for attr in attrs:
			if(attr[0] == 'src'):
				imgSrc = attr[1];
		#		print (imgSrc);
		if(imgSrc != ''):
			if(imgSrc.startswith('http')):
				self.add_to_imageSrcs(imgSrc);
			else:
				self.add_to_imageSrcs(Host.host + imgSrc);
				
class Anchors:
	anchorUrls = list();
	links_visited = list();
	
	def add_to_anchorUrls(self, src):
		if((urlparse(src).netloc == Host.parsed_url.netloc) and (src not in self.anchorUrls)):
			self.anchorUrls.append(src);
	
	def set_links_visited(self, link):
		self.links_visited.append(link);
	
	def get_anchor_href(self, tag, attrs):
	#	print("Start tag:", tag)
		aUrl = '';
		for attr in attrs:
			if(attr[0] == 'href'):
				aUrl = attr[1];
		if(aUrl != ''):
			if(aUrl.startswith('http')):
				self.add_to_anchorUrls(aUrl);
			else:
				self.add_to_anchorUrls(Host.host + aUrl);

class ParseHTML(HTMLParser):
	image = Images();
	anchor = Anchors();
	
	def set_anchor(self, anchor):
		self.anchor = anchor;
		
	def handle_starttag(self, tag, attrs):
		if(tag == 'a'):
			self.anchor.get_anchor_href(tag, attrs);
		if(tag == 'img'):
			self.image.set_image_url(tag, attrs);
			
			
class Host:
	host = '';
	parsed_url = '';
	
	def set_hostname(url):
		Host.parsed_url = urlparse(url);
		Host.host = Host.parsed_url.scheme + '://' + Host.parsed_url.netloc;