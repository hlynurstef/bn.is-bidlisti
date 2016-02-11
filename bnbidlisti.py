# coding=utf-8
# Hlynur Stefánsson - hlynurstef@gmail.com

import requests
from bs4 import BeautifulSoup
import re

with requests.session() as c:
	# Place your username and password for bn.is here
	USERNAME = 'your_username_here'
	PASSWORD = 'your_password_here'

	login_url = 'http://www.bn.is/minar-sidur/innskraning/'
	bidlisti_url = 'http://www.bn.is/minar-sidur/stada-a-bidlista/'

	# Use the following code only to test offline with a file. Just copy the
	# source code of http://www.bn.is/minar-sidur/stada-a-bidlista into 
	# the a file called bn.html and then uncomment lines 21-23. Make sure to 
	# comment lines 26-31 as well if you want to try testing with a file.
	#
	# file = open('bn.html')
	# page = file.read()
	# soup = BeautifulSoup(page)

	# Logging into bn.is
	login_data = dict(username=USERNAME, password=PASSWORD, action='login')
	c.post(login_url, data=login_data, headers={"Referer": "http://www.bn.is/"})

	# Use BeautifulSoup to find the correct part of the page and put it in a list
	page = c.get(bidlisti_url)
	soup = BeautifulSoup(page.content)
	info_list = soup.find_all('span')
	list_length = len(info_list)

	# Regular expressions with unicode characters
	location_re = re.compile('(Reykjav(\xed)k|Hafnarfj(\xf6)r(\xf0)ur)[a-zA-Z (\xf0)(\xe6)(\xed)(\xfa)(\xde)()]*')
	number_re = re.compile('[0-9]+')

	# Search by string "Númer" with unicode characters
	search_string = u'N\xfamer'

	# For loop that runs regex to find the info we want and prints out the results
	for i in range(1, list_length-1):
		current_item = info_list[i].getText()
		if search_string in current_item:
			print re.search(location_re, current_item).group(0)
			print re.search(number_re, current_item).group(0)
		else:
			print 'Not found'