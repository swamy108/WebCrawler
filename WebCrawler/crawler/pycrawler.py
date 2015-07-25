import urllib


from queue import Queue
from crawler.models import ParseHTML
from crawler.models import Anchors
from crawler.models import Host
from crawler.models import Images



class Crawler:	
	depth = 0;
	url = '';
	links_depth_visited = {};
	links_visited = [];
	next_level_links = [];
	links = [];
	anchor = Anchors();	
	
	def set_url(self, url):
		self.url = url;
	
	def web_crawler(self, data):
		
		handle = urllib.request.urlopen(data['url'])
		
		Host.set_hostname(data['url']);

		self.anchor = Anchors();
		dataParser = ParseHTML();
		dataParser.set_anchor(self.anchor);
		dataParser.feed(str(handle.read()))
		dataParser.close()
		
	#	for a in self.anchor.anchorUrls:
	#		print(a);
		
		self.links_depth_visited[self.depth] = list();
		self.links_depth_visited[self.depth].append(data['url']);
		
		self.links_visited.append(data['url']);
		
		print(len(Images.imageSrcs));
		print(len(self.anchor.anchorUrls));
		self.depth = 1;
		
		self.links = list(self.anchor.anchorUrls);
		del self.anchor.anchorUrls[:];
		
		while(self.depth <= int(data['depth'])):
			self.links_depth_visited[self.depth] = list();
			print(str(self.depth) + ' : ' + str(len(self.links)))
			for link in self.links:
				dataParser = ParseHTML();
				self.anchor = Anchors();
				try:
					handle = urllib.request.urlopen(link);
					dataParser.set_anchor(self.anchor);
					dataParser.feed(str(handle.read()))
					dataParser.close();
				except:
					print(link);
					continue;
				self.links_depth_visited[self.depth].append(link);
				self.links_visited.append(link);
				self.update_next_level(self.anchor.anchorUrls);
				del self.anchor.anchorUrls[:];
			self.links = list(self.next_level_links);
			del self.next_level_links[:];
			self.depth = self.depth + 1;
			self.remove_visited_links();
			
	#	for link in anchor.anchorUrls:

		print(len(Images.imageSrcs));
		
		print(len(self.links));

		
	def update_next_level(self, links):
		for url in links:
			self.next_level_links.append(url);
	
	def remove_visited_links(self):
		unique_links = list(set(self.links));
		self.links = list(unique_links);
		for link in unique_links:
			if(link in self.links_visited):
				self.links.remove(link)