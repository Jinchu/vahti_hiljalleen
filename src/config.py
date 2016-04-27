# This file is written by Peter Kronstrom
# -*- coding: UTF-8 -*-

# How long the website is queried in seconds before the connection times out
REQUEST_TIMEOUT = 3

if False:
	# I have saved my sensitive data in environment variables
	# change the conditional to False and modify the details below else
	import os
	GMAIL_USER = os.environ.get('GMAIL_USER')
	GMAIL_PWD = os.environ.get('GMAIL_PWD')
	RECIPIENT = os.environ.get('VAHTI_RECIPIENT')
	BOT_ID = os.environ.get('BOT_ID')
	TARGET_CHAN_ID = os.environ.get('TARGET_TELEGRAM_CHAN')
	DEV_PERSONAL_ID = os.environ.get('DEV_PERSONAL_TELEGRAM')
else:
	GMAIL_USER = "sender.name@gmail.com"
	GMAIL_PWD = "password44"
	RECIPIENT = "reseiver.name@gmail.com"
	BOT_ID = "999999199:EEEeeeEeEEE6EExxXXxxxxXxxxXXXXXxXxx"
	TARGET_CHAN_ID = "199009900"
	DEV_PERSONAL_ID = "99009900"

INTERVAL = 19
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like GeckoMozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
MAIL_SUBJECT = u"Server notification"

# In Jinja2 format
MAIL_TEMPLATE = """
	Generic server notification.
"""
