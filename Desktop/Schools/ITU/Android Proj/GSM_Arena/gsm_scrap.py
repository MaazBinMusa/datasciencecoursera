import requests
import re
import pyexcel as pe
from bs4 import BeautifulSoup
import csv

def function3(link4):
	'''scrap all the phone attribute from the page ie http://www.gsmarena.com/apple_ipad_air-5797.php
	 and add it to the database '''
	print(link4)
	data3 = requests.get(link4)
	soup5 = BeautifulSoup(data3.text, "lxml")
	soup6 = BeautifulSoup(str(soup5.findAll("div", { "id" : "specs-list" })),"lxml")
	#print(soup6)
	attr_arr=soup6.find_all('td',{'class':'ttl'})
	val_arr=soup6.find_all('td',{'class':'nfo'})
	disp=['Super AMOLED','IPS LCD','AMOLED']
	display_resolution = "NULL"
	version= "NULL"
	sensors= "NULL"
	flash_type= "NULL"
	auto_focus= "NULL"
	aperture= "NULL"
	primary_camera_resolution= "NULL"
	primary_camera_features= "NULL"
	FM= "NULL"
	wifi_type= "NULL"
	bluetooth_type= "NULL"
	weight= "NULL"
	display_type= "NULL"
	screen_protection= "NULL"
	available_colors= "NULL"
	usb_type= "NULL"
	screen_size= "NULL"
	sim_type= "NULL"
	non_removable_battery= "NULL"
	battery_type= "NULL"
	battery_capacity= "NULL"
	expandable_memory= "NULL"
	ram_memory= "NULL"
	internal_memory= "NULL"
	processor_frequency= "NULL"
	processor_type= "NULL"
	gpu= "NULL"
	no_of_cores= "NULL"
	def OS(text):
	    ios=re.search('ios[a-z0-9-._]*',text)
	    ver=re.search('v[0-9.]*',text)
	    os=ios.group(0).split('ios')[1] if ios else ver.group(0)[1:]
	    return os
	for i in range(len(attr_arr)):
	    #print("Enter")
	    attr=attr_arr[i].text.encode('ascii','ignore').decode('utf-8')
	    val=val_arr[i].text.encode('ascii','ignore').decode('utf-8')
	    prim=re.search('\\d+ MP',val)
	    mem=re.findall('[0-9]* GB',val)
	    if('Resolution' in attr):
	        display_resolution=val.split('pixels')[0]
	    elif('OS' in attr):
	        #version=OS(val.encode('ascii','ignore').decode('utf-8'))
	        version =val
	        #print(val)
	    elif('Sensor' in attr):
	        sensors=val
	    elif('Primary' in attr):
	        aper=re.search('f[0-9./]*',val)
	        flash_type='LED' if('LED' in val) else 'No'
	        auto_focus='Yes' if('autofocus' in val) else 'No'
	        aperture=aper.group(0) if aper else 'No'
	        if prim: primary_camera_resolution=prim.group(0).split('MP')[0]
	    elif('Features' in attr):
	        primary_camera_features=val
	    elif('Secondary' in attr):
	        if prim: front_camera_resolution=prim.group(0).split('MP')[0]
	    elif('Radio' in attr):
	        FM='Yes' if ('FM' in val) else 'No'
	    elif('WLAN' in attr):
	        wifi_type=val
	    elif('Bluetooth' in attr):
	        bluetooth_type=val
	    elif('Weight' in attr):
	        weight=val
	    elif('Type' in attr):
	        for i in disp:
	            if(i in val):
	                display_type=i
	                break
	    elif('Protection' in attr):
	        screen_protection=val    
	    elif('Colors' in attr):
	        available_colors=val
	    elif('Size' in attr):
	        screen_size=val[:3]
	#screen_pixel_density
	    elif('USB' in attr):
	        usb_type=val
	    elif('SIM' in attr):
	         sim_type=val
	    elif('battery' in val):
	        val=val.split(' ')
	        non_removable_battery='Yes' if('Non' in val[0]) else 'No'
	        battery_type=val[1]
	        if len(val) > 2:
	        	battery_capacity=val[2]
	    elif('Card slot' in attr):
	    	if(len(mem) != 0):
	        	expandable_memory=mem[0][:-2]
	    elif('Internal' in attr):
	        if(len(mem) > 1):
	        	ram_memory=mem[1][:-3]
	        	internal_memory=mem[0][:-3]
	        elif(len(mem) == 1):
	        	internal_memory=mem[0][:-3]
	    elif('GPU' in attr):
	        gpu=val
	    elif('Chipset' in attr):
	        processor_type=val
	    elif('CPU' in attr):
	    	cpu = val
	    	#processor_frequency=cp.group(0)[:-4]
	        #no_of_cores=val.split(' ')[0]
	lis=['Link','display_resolution','version','sensors','flash_type','auto_focus','aperture','primary_camera_resolution','primary_camera_features','FM','wifi_type','bluetooth_type','weight','display_type','screen_protection','available_colors','usb_type','screen_size','sim_type','non_removable_battery','battery_type','battery_capacity','expandable_memory','ram_memory','internal_memory','processor_type','gpu','cpu']
	lis_data=[link4,display_resolution,version,sensors,flash_type,auto_focus,aperture,primary_camera_resolution,primary_camera_features,FM,wifi_type,bluetooth_type,weight,display_type,screen_protection,available_colors,usb_type,screen_size,sim_type,non_removable_battery,battery_type,battery_capacity,expandable_memory,ram_memory,internal_memory,processor_type,gpu,cpu]
	#sheet = pe.get_sheet(file_name="gsm_data.xlsx")
	#sheet.row += lis
	#sheet.row +=lis_data
	#sheet.save_as("gsm_data.xlsx")
	#print(display_resolution,version,sensors)
	myData = [lis_data]
	myFile = open('Phones.csv', 'a', newline='')
	with myFile:
		writer = csv.writer(myFile)
		writer.writerows(myData)

def function1(link3):
	'''returns all the page to be scrap of a particular company http://www.gsmarena.com/samsung-phones-9.php
	It will extract all the navigation link present on the bottom of the page'''
	data2 = requests.get(link3)
	soup3 = BeautifulSoup(data2.text, "lxml")
	soup4= BeautifulSoup(str(soup3.findAll("div", { "class" : "nav-pages" })),"lxml")
	print(soup4)
	if soup4.get_text() == '[]': #some pages have no navigation pages thats why if is used
		print("NoNav")
		print (link3)
		function2(link3)
		#print ("-------------------No1--------------------------")
	else:
		print("Nav")
		#print (link3)
		function2(link3)
		link1=  "http://www.gsmarena.com/"+ soup4.a['href']
		#print (link1)
		function2(link1)
		for links in soup4.find_all('a'):
			link2 = "http://www.gsmarena.com/" + links['href']
			if link2 == link1:
				pass	
			else:
				link5 = "http://www.gsmarena.com/" + links['href']
				print (link5)
				function2(link5)
		#print ("--------------------------------Yes1--------------------------------")


def function2(phn_links):
	'''return all the phone links of the page ie http://www.gsmarena.com/amazon-phones-76.php'''
	#phn_links = "http://www.gsmarena.com/amazon-phones-76.php"
	phn_links_page = requests.get(phn_links)
	phn_soup = BeautifulSoup(phn_links_page.text, "lxml")
	phn_soup2 = BeautifulSoup(str(phn_soup.findAll("div", { "class" : "makers" })), "lxml")
	#print(phn_soup2)
	for link in phn_soup2.find_all('a'):
		#print("Func2")
		link = "http://www.gsmarena.com/" + link['href']
		put_in_csv(link)

def put_in_csv(link):
	if(check_in_csv(link) == 0):
		myFile = open('links.csv', 'a', newline='')
		with myFile:
			writer = csv.writer(myFile, delimiter=' ')
			writer.writerow([link,])
		function3(link)
	else:
		print("Already Done")

def check_in_csv(link):
	with open('links.csv', 'r') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if len(row) > 0:
				if link == row[0]:
					return 1
	return 0

link = "http://www.gsmarena.com/makers.php3" #start link to scrap gsm contains all the phone maker company
data = requests.get(link)
soup = BeautifulSoup(data.text, "lxml")
#print(soup)
myFile = open('links.csv', 'a', newline='')
soup2= BeautifulSoup(str(soup.findAll("div", { "class" : "st-text" })),"lxml")
lis = soup2.find_all('a')

for i in range(0,len(lis),2):
	link2 = "http://www.gsmarena.com/"+ lis[i]['href']
	function1(link2)
	