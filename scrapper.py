import requests
from bs4 import BeautifulSoup
from send_mail import Report
from comparator import Comparator
import time
import pickle
import os
import sys

class Phone:
	def __init__(self, name, price, model, url):
		self.model = model
		self.name = name
		self.price = price.replace(',', '')
		self.url = url
	
	def __eq__(self, other):
		return self.name == other.name

	def __lt__(self, other):
		return int(self.price) < int(other.price)

class Scrapper:
	def __init__(self):
		self.base_url = "https://mobileshop.com.eg/en/mobiles"
		self.brands = {} # Stores all the phone brands available on the website
		self.phones = [] # Stores all the phones after crawling them

	def request_page(self, url):
		result = requests.get(url)
		c = result.content
		soup = BeautifulSoup(c, "html.parser")
		return soup

	def get_mobile_brands(self):
		self.brands = {}
		soup = self.request_page(self.base_url + "/Mobile-brands")
		parent = soup.find("div", {"class": "refine-images" })

		for brand in parent.findChildren('div'):
			brand_name = brand.a.img['alt']
			brand_url = brand.a['href']
			self.brands[brand_name] = brand_url
		return self.brands

	def get_models(self, brand_name):
		all_phones = []
		brand_url = self.brands[brand_name]
		soup = self.request_page(brand_url)
		parent = soup.find("div", {"class": ["main-products", "product-grid"]})
		if parent is None:
			return all_phones
		models = parent.findChildren('div', {"class": "struct"})
		for model in models:
			model_name_tag = model.find("div", {"class": "name"})
			model_price_tag = model.find("div", {"class": "price"})
			
			model_name = model_name_tag.a.string.strip()
			model_url = model_name_tag.a['href']
			try:
				model_price = model_price_tag.string.strip().split(" ")[0]
			except:
				model_price = model_price_tag.find("span", {"class": "price-new"}).string.strip().split(" ")[0]

			phone = Phone(model_name, model_price, brand_name, model_url)
			all_phones.append(phone)
		return all_phones

	def build_knowledge_base(self):
		self.get_mobile_brands()
		print "Crawling all phones at: " + time.strftime("%c")
		print "-------------"
		for brand in self.brands:
			print "Processing brand: " + brand
			phones = self.get_models(brand)
			self.phones.extend(phones)
		print "-------------"
		print "Finished crawling all phones. Total number = " + str(len(self.phones))
		return self.phones

if __name__ == "__main__":
	script_loc = os.path.dirname(os.path.realpath(__file__))
	os.chdir(script_loc)

	scrapper = Scrapper()
	phones = scrapper.build_knowledge_base()
	if os.path.isfile("save.p"):
		old_phones = pickle.load(open( "save.p", "rb"))
	
	comparator = Comparator(old_phones, phones)
		
	new_phones = comparator.get_new_phones()
	removed_phones = comparator.get_removed_phones()
	updated_phones = comparator.get_updated_phones()

	# Dumping the new data to the disk
	print "Storing today's data to disk .."
	pickle.dump(phones, open( "save.p", "wb" ) )

	# Sending mail results
	print "Sending mail results .."
	reporter = Report(phones, new_phones, removed_phones, updated_phones)
	reporter.send_updates()