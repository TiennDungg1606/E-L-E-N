import pyscreenshot as ImageGrab
import time
import os
import subprocess
from pynput.keyboard import Key, Controller
import psutil
import requests
from bs4 import BeautifulSoup
import webbrowser

class SystemTasks:
	def __init__(self):
		self.keyboard = Controller()


	def write(self, text):
		text = text[5:]
		for char in text:
			self.keyboard.type(char)
			time.sleep(0.02)

	def select(self):
		self.keyboard.press(Key.ctrl)
		self.keyboard.press('a')
		self.keyboard.release('a')
		self.keyboard.release(Key.ctrl)

	def hitEnter(self):
		self.keyboard.press(Key.enter)
		self.keyboard.release(Key.enter)

	def delete(self):
		self.keyboard.press(Key.backspace)
		self.keyboard.release(Key.enter)

	def save(self, text):
		if "don't" in text:
			self.keyboard.press(Key.right)
		else: 
			self.keyboard.press(Key.ctrl)
			self.keyboard.press('s')
			self.keyboard.release('s')
			self.keyboard.release(Key.ctrl)
		self.hitEnter()

class TabOpt:
	def __init__(self):
		self.keyboard = Controller()

	def switchTab(self):
		self.keyboard.press(Key.ctrl)
		self.keyboard.press(Key.tab)
		self.keyboard.release(Key.tab)
		self.keyboard.release(Key.ctrl)

	def closeTab(self):
		self.keyboard.press(Key.ctrl)
		self.keyboard.press('w')
		self.keyboard.release('w')
		self.keyboard.release(Key.ctrl)

	def newTab(self):
		self.keyboard.press(Key.ctrl)
		self.keyboard.press('n')
		self.keyboard.release('n')
		self.keyboard.release(Key.ctrl)


class WindowOpt:
	def __init__(self):
		self.keyboard = Controller()

	def openWindow(self):
		self.maximizeWindow()
	
	def closeWindow(self):
		self.keyboard.press(Key.alt_l)
		self.keyboard.press(Key.f4)
		self.keyboard.release(Key.f4)
		self.keyboard.release(Key.alt_l)
	
	def minimizeWindow(self):
		for i in range(2):
			self.keyboard.press(Key.cmd)
			self.keyboard.press(Key.down)
			self.keyboard.release(Key.down)
			self.keyboard.release(Key.cmd)
			time.sleep(0.05)
	
	def maximizeWindow(self):
		self.keyboard.press(Key.cmd)
		self.keyboard.press(Key.up)
		self.keyboard.release(Key.up)
		self.keyboard.release(Key.cmd)

	def moveWindow(self, operation):
		self.keyboard.press(Key.cmd)

		if "left" in operation:
			self.keyboard.press(Key.left)
			self.keyboard.release(Key.left)
		elif "right" in operation:
			self.keyboard.press(Key.right)
			self.keyboard.release(Key.right)
		elif "down" in operation:
			self.keyboard.press(Key.down)
			self.keyboard.release(Key.down)
		elif "up" in operation:
			self.keyboard.press(Key.up)
			self.keyboard.release(Key.up)
		self.keyboard.release(Key.cmd)

	def switchWindow(self):
		self.keyboard.press(Key.alt_l)
		self.keyboard.press(Key.tab)
		self.keyboard.release(Key.tab)
		self.keyboard.release(Key.alt_l)
		

	def takeScreenShot(self):
		from random import randint
		im = ImageGrab.grab()
		im.save(f'Files and Document/ss_{randint(1, 100)}.jpg')

def isContain(text, lst):
	for word in lst:
		if word in text:
			return True
	return False

def Win_Opt(operation):
	w = WindowOpt()
	if isContain(operation, ['open']):
		w.openWindow()
	elif isContain(operation, ['close']):
		w.closeWindow()
	elif isContain(operation, ['mini']):
		w.minimizeWindow()
	elif isContain(operation, ['maxi']):
		w.maximizeWindow()
	elif isContain(operation, ['move', 'slide']):
		w.moveWindow(operation)
	elif isContain(operation, ['switch','which']):
		w.switchWindow()
	elif isContain(operation, ['screenshot','capture','snapshot']):
		w.takeScreenShot()
	return

def Tab_Opt(operation):
	t = TabOpt()
	if isContain(operation, ['new','open','another','create']):
		t.newTab()
	elif isContain(operation, ['switch','move','another','next','previous','which']):
		t.switchTab()
	elif isContain(operation, ['close','delete']):
		t.closeTab()
	else:
		return


def System_Opt(operation):
	s = SystemTasks()
	if 'delete' in operation:
		s.delete()
	elif 'save' in operation:
		s.save(operation)
	elif 'type' in operation:
		s.write(operation)
	elif 'select' in operation:
		s.select()
	elif 'enter' in operation:
		s.hitEnter()
	elif isContain(operation, ['website']):
		search_and_open(operation)
	else:
		open_application(operation)	
#	else:
#		open_website(operation)
		return


###############################
###########  VOLUME ###########
###############################

keyboard = Controller()
def mute():
	for i in range(50):
		keyboard.press(Key.media_volume_down)
		keyboard.release(Key.media_volume_down)

def full():
	for i in range(50):
		keyboard.press(Key.media_volume_up)
		keyboard.release(Key.media_volume_up)


def volumeControl(text):
	if 'full' in text or 'max' in text: full()
	elif 'mute' in text or 'min' in text: mute()
	elif 'incre' in text:
		for i in range(5):
			keyboard.press(Key.media_volume_up)
			keyboard.release(Key.media_volume_up)
	elif 'decre' in text:
		for i in range(5):
			keyboard.press(Key.media_volume_down)
			keyboard.release(Key.media_volume_down)

def systemInfo():
	import wmi
	c = wmi.WMI()  
	my_system_1 = c.Win32_LogicalDisk()[0]
	my_system_2 = c.Win32_ComputerSystem()[0]
	info = ["Total Disk Space: " + str(round(int(my_system_1.Size)/(1024**3),2)) + " GB",
			"Free Disk Space: " + str(round(int(my_system_1.Freespace)/(1024**3),2)) + " GB",
			"Manufacturer: " + my_system_2.Manufacturer,
			"Model: " + my_system_2. Model,
			"Owner: " + my_system_2.PrimaryOwnerName,
			"Number of Processors: " + str(my_system_2.NumberOfProcessors),
			"System Type: " + my_system_2.SystemType]
	return info

def batteryInfo():
	# usage = str(psutil.cpu_percent(interval=0.1))
	battery = psutil.sensors_battery()
	pr = str(battery.percent)
	if battery.power_plugged:
		return "Your System is currently on Charging Mode and it's " + pr + "% done."
	return "Your System is currently on " + pr + "% battery life."

def OSHandler(query):
	if isContain(query, ['system', 'info']):
		return ['Here is your System Information...', '\n'.join(systemInfo())]
	elif isContain(query, ['cpu', 'battery']):
		return batteryInfo()


from difflib import get_close_matches
import json
from random import choice
from googlesearch import search
import webbrowser

data = json.load(open('extrafiles/websites.json', encoding='utf-8'))

#def open_website(query):
#	query = query.replace('open','')
#	if query in data:
#		response = data[query]
#		if len(query)==0: return "None"
#		response = choice(data[query[0]])
#	webbrowser.open(response)
def search_and_open(query):
    # Tìm kiếm trên Google và lấy URL của kết quả đầu tiên
	query = query.replace('open website','')
	search_results = list(search(query, num_results=1))
	if search_results:
		first_result_url = search_results[0]
		print(f"Mở trang: {first_result_url}")
        
        # Mở trang kết quả đầu tiên trong trình duyệt mặc định
		webbrowser.open(first_result_url)
	else:
		return "I found no results:))"

import pyautogui
import pyperclip

def open_application(query):
    # Sao chép từ khóa vào clipboard
	query = query.replace('open','')
	pyperclip.copy(query)

    # Mở thanh tìm kiếm Start bằng phím tắt Windows + S
	pyautogui.hotkey('win', 's')
	time.sleep(0.5)  # Giảm thời gian chờ để cửa sổ tìm kiếm mở

    # Dán từ khóa vào thanh tìm kiếm
	pyautogui.hotkey('ctrl', 'v')
	time.sleep(0.5)  # Giảm thời gian chờ để kết quả tìm kiếm hiển thị

    # Nhấn Enter để chọn ứng dụng đầu tiên
	pyautogui.press('enter')


