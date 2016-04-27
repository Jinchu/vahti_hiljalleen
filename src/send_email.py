# -*- coding: utf-8 -*-

from optparse import OptionParser
import smtplib
import argparse
parser = argparse.ArgumentParser()

from config import RECIPIENT, GMAIL_USER, GMAIL_PWD, RECIPIENT, MAIL_SUBJECT, MAIL_TEMPLATE


def send_email(topic, msg):
        """
                Parses the mail and sends it to the address specified in the config.py file
        """

        # Parse the mail headers
        headers = [
                                "From: " + GMAIL_USER,
                                "Subject: " + topic,
                                "To: " + RECIPIENT,
                                "MIME-Version: 1.0",
                                "Content-Type: text/html; charset=UTF-8"
                                ]

        headers = "\r\n".join(headers)
        headers += "\r\n\r\n"
        headers += msg

        # Connect to the mailserver and send the message
        try:
                mailServer = smtplib.SMTP("smtp.gmail.com", 587)
                #mailServer.set_debuglevel(1)
                mailServer.ehlo()
                mailServer.starttls()
                mailServer.ehlo()
                mailServer.login(GMAIL_USER, GMAIL_PWD)
                mailServer.sendmail(GMAIL_USER, RECIPIENT, headers.encode('utf-8'))
                mailServer.close()
                print("[vahti.py] Mail sent to " + RECIPIENT)

        except smtplib.SMTPAuthenticationError:
                print("Incorrect Gmail login. - Mail was not sent.")



def main():
        parser.add_argument("-msg", type=str, help="Use this as the email body", default=MAIL_TEMPLATE)
        parser.add_argument("-s", type=str, help="Use this as the topic of the email", default=MAIL_SUBJECT)
        
        args = parser.parse_args()

        send_email(args.s, args.msg)

if __name__ == "__main__":
        main()
