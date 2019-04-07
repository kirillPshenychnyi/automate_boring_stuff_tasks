#! /usr/bin/python3

"""example of Selenium module usage for images downloading from flickr"""

import logging
import os
import argparse
import requests

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s- %(message)s')


def next_image(count_images, firefox_driver):
    firefox_driver.find_element_by_tag_name('html').send_keys(Keys.ARROW_RIGHT)
    download_images(count_images, firefox_driver)


def download_images(count_images, firefox_driver):
    logging.info('Images %s' % count_images)
    if count_images == 0:
        return

    try:
        first_photo = \
            WebDriverWait(firefox_driver, 6, poll_frequency=2).until(
                EC.presence_of_element_located((By.XPATH, "//img[@class='main-photo']")))

        img_url = first_photo.get_attribute('src')

        img = requests.get(img_url)
        img.raise_for_status()

        img_file = open(os.path.join('images', str(count_images) + '.jpg'), mode='wb')

        for chunk in img.iter_content(1000):
            img_file.write(chunk)

        img_file.close()
        count_images = count_images - 1
        next_image(count_images, firefox_driver)
    except TimeoutException:
        logging.debug('TimeoutException')
        next_image(count_images, firefox_driver)
    except StaleElementReferenceException:
        logging.debug('StaleElementReferenceException')
        next_image(count_images, firefox_driver)


def search_images(keyword, images_number):
    firefox_driver = webdriver.Firefox()
    firefox_driver.get('https://www.flickr.com/search/?text=' + keyword)

    main_search_results_element = \
        WebDriverWait(firefox_driver, 4).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='photo-list-photo-interaction']")))

    main_search_results_element.click()

    os.makedirs('images', exist_ok=True)

    download_images(images_number, firefox_driver)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('keyword', type=str, help='Keyword for image search')
    parser.add_argument('images', type=int, help='Number of images for download')

    args = parser.parse_args()

    search_images(args.keyword, args.images)
