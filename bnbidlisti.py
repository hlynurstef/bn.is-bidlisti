# coding=utf-8
# Hlynur Stefánsson - hlynurstef@gmail.com - github.com/hlynurstef/

from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

with requests.session() as c:
	# Place your username and password for bn.is here
	USERNAME = input("Username: ")
	PASSWORD = input("Password: ")
	

	login_url = "http://www.bn.is/minar-sidur/innskraning/"
	bidlisti_url = "http://www.bn.is/minar-sidur/stada-a-bidlista/"

	# Logging into bn.is
	login_data = dict(username=USERNAME, 
					  password=PASSWORD, 
					  action="login")
	c.post(login_url, 
		   data=login_data, 
		   headers={"Referer": "http://www.bn.is/"})

	# Use BeautifulSoup to find the correct part 
	# of the page and put it in a list
	page = c.get(bidlisti_url)
	soup = BeautifulSoup(page.content, "html.parser")
	info_list = soup.find_all("span")
	list_length = len(info_list)

	# Regular expressions to find the name of the 
	# location and number in the waiting list
	location_re = re.compile("(Reykjavík|Hafnarfjörður)" + 
							 "[a-zA-Z ðæíúÞ()]*")
	number_re = re.compile("[0-9]+")

	# Search by string "Númer" with unicode characters
	search_string = "Númer"

	# Open file bn.txt to append, creates the file if it doesn't exist
	with open("bn.txt", "a+") as myfile:

		now = datetime.now()
		date = "Date: %s/%s/%s" % (now.day, now.month, now.year)
		time = "Time: %s:%s:%s" % (now.hour, now.minute, now.second)
		print(date)
		print(time)
		myfile.write(date + "\n")
		myfile.write(time + "\n")
	
		# For loop that runs regex to find the info we want and prints 
		# out the results to console and to file
		for i in range(1, list_length-1):
			current_item = info_list[i].getText()
			if search_string in current_item:

				# Print to console
				location = re.search(location_re, current_item).group()
				number = re.search(number_re, current_item).group()
				print(location)
				print(number)

				# Print to file
				myfile.write(location + "\n")
				myfile.write(number + "\n")
			else:

				# Nothing was found, possibly due to 
				# incorrect username/password
				not_found = ("Not found - make sure you entered " + 
							 "username/password correctly")
				print(not_found)
				myfile.write(not_found + "\n")
				break

		myfile.write("\n")
