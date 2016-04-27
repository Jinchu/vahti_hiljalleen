# -*- coding: utf-8 -*-

from optparse import OptionParser
import os
import glob
import smtplib
import hashlib
import urllib2
import time
import logging
import difflib
import errno
import socket

from twx.botapi import TelegramBot

from config import RECIPIENT, GMAIL_USER, GMAIL_PWD, RECIPIENT, MAIL_SUBJECT, MAIL_TEMPLATE
from config import USER_AGENT, INTERVAL, BOT_ID, TARGET_CHAN_ID, DEV_PERSONAL_ID
import send_email
import sys, time
# from daemon import Daemon

LOG_FORMAT = '%(asctime)-15s    %(message)s'
URL = "http://google.fi"
OUTPUT_DIR = '/home/username/vahti/'
ARCHIVE = OUTPUT_DIR + 'archive/'

MATCH_START = '<h2 class="post-title">'
MATCH_END = '</h2>'

class titles():
	def __init__(self, html):
		    self.title_list = []
		    tmp = html.split(MATCH_START,10)

		    for i in range(1,(len(tmp) - 1)):
			    tem = tmp[i].split(MATCH_END)
			    self.title_list.append(tem[0])

	def clear(self):
		self.title_list = []

	def print_all(self):
		for t in self.title_list:
			print(t)

	def has_changed(self, another):
		larger = max(len(self.title_list), len(another.title_list))
		for i in range(0,(larger - 1)):
			if (self.title_list[i] != another.title_list[i]):
				return i
		return -1

	def get_title(self, element=0):
		if (element >= len(self.title_list)):
			return ''
		return self.title_list[element]


def init_logging():
	logging.getLogger(__name__)
	logging.basicConfig(filename=OUTPUT_DIR+'periodic_check.log',level=logging.DEBUG, format=LOG_FORMAT)
	logging.info('Logs iniated and program running')

def download(url):
	user_agent = USER_AGENT
	headers = { 'User-Agent' : user_agent }
	req = urllib2.Request(url, None, headers)
	response = urllib2.urlopen(req)
	page = response.read()
	return page

def save_index(page):
	current_time = time.strftime("%m.%d.%y-%H.%M", time.localtime())
	output_name = ARCHIVE + 'index_%s.html' % current_time
	output = open(output_name, "w")
	output.write(page)
	output.close()
	logging.info("new index saved to archive")

def get_latest_html():
	newest = min(glob.iglob(ARCHIVE + '*.html'), key=os.path.getctime)
	f = open(newest,'r')
	return f

def lib_compare_html(old_html, new_html):
	old_lines = old_html.splitlines()
	new_lines = new_html.splitlines()
	d = difflib.Differ()
	diff = d.compare(old_lines, new_lines)

	logging.info("file differences calculated")
	return '\n'.join(diff)

def my_compare_html(old, new):
	changed_line = ''
	line_old = old.readline()
	line_new = new.readline()
	while (line_old and line_new):
		if (line_old != line_new):
			changed_line = line_new
        line_old = old.readline()
        line_new = new.readline()

	return changed_line

class message_hj():
	def __init__ (self):
		self.body = "New blog published: "

	def add_title_in_html(self, html_row):
		self.body = self.body + html_row + "\n\n"

	def add_title_in_cleartxt(self, html_row):
		tg_message = " "
		tmp = html_row.split('"',10)

		self.body = self.body + tmp[3] + " Go check it out in " + tmp[1] + "\n\n"

	def fallback_without_title(self):
		self.body = self.body + "Go check it out in http://google.fi "

	def send_to_telegram(self, bot):
		result = bot.send_message(TARGET_CHAN_ID, self.body).wait()
		print("Telegram notification sent - No need for email: " + str(result))
		logging.info("Telegram notification sent - No need for email: " + str(result))

	def send_to_email(self):
		send_email.send_email("google.fi updated!", self.body)
		print("Email sent to %s", RECIPIENT)
		logging.info("Email sent to %s", RECIPIENT)


# class MyDaemon(Daemon):
class Not_Really_Daemon():
	def run(self):
		init_logging()
		"""
		TODO: create directory for archive if it does not excist already
		"""
		bot = TelegramBot(BOT_ID)
		bot.update_bot_info().wait()
		print(bot.username)
		logging.info("Bot %s running", bot.username)

		page_source = download(URL)
		old_titles = titles(page_source)

		logging.info("First set of titles parsed")
		minutes = 60 * INTERVAL

		# Disabled sending messages to the channel to decrease spam

		result = bot.send_message(DEV_PERSONAL_ID, "The blog will be watched").wait()
#		print("Sending channel: " + str(result))
		logging.info("Sending channel: " + str(result))

		while True:
			time.sleep(minutes)
			try:
				page_source = download(URL)
				new_titles = titles(page_source);
				diff = new_titles.has_changed(old_titles)
			except socket.error:
				diff = -2

			if (diff == -2):
				print("No internet connection")
				logging.info("No internet connection")
			elif (diff < 0):
				print("no changes were made")
				logging.info("No changes were made")
			else:
				print("Changes on target")
				logging.info("Changes on target")
				save_index(page_source)
				message = message_hj()
				old_titles = new_titles
				try:
					message.add_title_in_cleartxt(new_titles.get_title(diff))
					message.send_to_telegram(bot)

				except:
					fallback_msg = message_hj()
					fallback_msg.fallback_without_title()
					fallback_msg.send_to_telegram(bot)



if __name__ == "__main__":
#	daemon = MyDaemon('/tmp/daemon-example.pid')
	daemon = Not_Really_Daemon()
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'foreground' == sys.argv[1]:
			print("Debug mode: running on front ground")
			daemon.run()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print("Unknown command")
			sys.exit(2)
		sys.exit(0)
	else:
		print("usage: %s start|stop|restart|foreground") % sys.argv[0]
		sys.exit(2)


