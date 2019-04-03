#! /usr/bin/python3

"""example of Selenium module usage for gmail sending"""

import logging
import os
import argparse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')


def loginToMail(browser_instance, username, password):
    try:
        browser_instance.get('https://accounts.google.com/signin')

        login = browser_instance.find_element_by_name('identifier')
        login.send_keys(username)
        login.send_keys(Keys.ENTER)

        password_field = WebDriverWait(browser_instance, 4).until(EC.presence_of_element_located((By.NAME, 'password')))

        browser_instance.find_element_by_tag_name('html').click()
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
    except:
        browser_instance.close()


def sendLetter(browser_instance, recepient, body, theme=''):
    WebDriverWait(browser_instance, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'gb_xc')))

    browser_instance.get('https://mail.google.com/mail/u/0/#inbox?compose=new')

    new_letter_button = browser_instance.find_element_by_xpath("//div[@class = 'aic']//div[@role='button']")
    new_letter_button.click()

    recipient_field = WebDriverWait(browser_instance, 10).until(EC.presence_of_element_located((By.NAME, 'to')))
    recipient_field.send_keys(recepient)
    body_field = browser_instance.find_element_by_id(':nv')
    body_field.send_keys(body)

    body_field.send_keys(Keys.CONTROL + Keys.ENTER)


def sendMail(login, password, recipient, text):
    browser_instance = webdriver.Firefox()
    loginToMail(browser_instance, login, password)
    sendLetter(browser_instance, recipient, text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m', '--message', help='mail message')
    group.add_argument('-f', '--file', help='path to file with message')

    parser.add_argument('login', type=str, help='google mail login')
    parser.add_argument('password', type=str, help='google mail password')
    parser.add_argument('recipient', type=str)

    args = parser.parse_args()

    logging.debug(args.login)
    logging.debug(args.password)
    logging.debug(args.recipient)
    logging.debug(args.message)

    if args.message:
        sendMail(args.login, args.password, args.recipient, args.message)
    else:
        if os.path.isfile(args.file):
            file = open(args.file, 'r')
            sendMail(args.login, args.password, args.recipient, file.read())
        else:
            raise Exception("File doesn't exist")
