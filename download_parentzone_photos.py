#!/usr/bin/env python3
import click
import os
import requests
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from urllib.parse import urlparse, parse_qs


class PhotoRetriever:
    """This class collects the image details and downloads them"""

    def __init__(self):
        self.numbers = []
        self.last_key = ""
        self.last_datetime = ""

    def add_image(self, image_src):
        """Adds an image to the list to be downloaded from an image src

        Expects an image url in the format:
        https://api.parentzone.me/v1/media/1234567/thumbnail?key=000a0000-0aaa-0a00-a000-a0aa00a0a00a&u=2021-05-18T06:26:58
        Extracts the image number, adds it to the number list if it is not
        already there and updates the latest key and datetime"""

        photo_added = False

        parsed_src = urlparse(image_src)
        number = parsed_src.path[len('/v1/media/'):].split("/")[0]
        if number not in self.numbers:
            self.numbers.append(number)
            photo_added = True

        query_dict = parse_qs(parsed_src.query)
        self.last_key = query_dict["key"][0]
        self.last_datetime = query_dict["u"][0]
        return photo_added

    def download_pictures(self, output_folder):
        """Downloads full quality pictures in the numbers list to output_folder"""
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        # For each image that we've found
        for number in self.numbers:
            # Parentzone looks to retrieve the images using the following API:
            # https://api.iconnectdaily.net/api/v1/media/1234567?key=000a0000-0aaa-0a00-a000-a0aa00a0a00a&size=thumbnail&u=2021-05-18T06:26:58
            # Valid options for size are "thumbnail" (128x128), "medium" (512x512), "web"/"small"/"large" (1024x768) and "full" (e.g. 2448x1836)

            image_url = f"https://api.iconnectdaily.net/api/v1/media/{number}?key={self.last_key}&size=full&u={self.last_datetime}"

            image_output_path = os.path.join(output_folder,
                                             f'{number}.jpg')

            # Only download and save the file if it doesn't already exist
            if not os.path.exists(image_output_path):
                r = requests.get(image_url, allow_redirects=True)
                open(image_output_path, 'wb').write(r.content)


@click.command()
@click.option('--email', help='Email address used to log in to ParentZone',
              prompt='Email address used to log in to ParentZone')
@click.option('--password', help='Password used to log in to ParentZone',
              prompt='Password used to log in to ParentZone')
@click.option('--output_folder', help='Output folder',
              default='./output')
def get_parentzone_photos(email, password, output_folder):
    """Downloads all photos from a ParentZone account"""
    driver = webdriver.Chrome()
    photo_collection = PhotoRetriever()

    driver.get("https://www.parentzone.me/")
    driver.implicitly_wait(10)

    # Fill in email and password
    email_field = driver.find_element_by_xpath('//*[@id="email"]')
    email_field.clear()
    email_field.send_keys(email)

    passwd_field = driver.find_element_by_xpath('//*[@id="password"]')
    passwd_field.clear()
    passwd_field.send_keys(password)
    time.sleep(2)
    login_button = driver.find_element_by_xpath("//button[@data-test-id='login_btn']")
    login_button.click()

    # Give it time to finish logging in
    time.sleep(2)

    # Go to Gallery view
    driver.get('https://www.parentzone.me/gallery')

    added_pictures = 1

    while added_pictures > 0:
        # Adds visible pictures and scrolls down
        added_pictures = 0

        # Add visible photos to collection. ToDo: Deal with videos -- I don't have any to test
        visible_pictures = driver.find_elements_by_xpath("//img[starts-with(@src, 'https://api.parentzone.me/v1/media/')]")
        for picture in visible_pictures:
            if photo_collection.add_image(picture.get_attribute("src")):
                # True only if the picture was not in the list already
                added_pictures += 1

        # Scroll down by just less than a page after waiting a pause
        # (Selenium seems to crash if too quick)
        time.sleep(1)
        thumbnails_pane = driver.find_element_by_xpath('//div[@tabindex="0"]')
        time.sleep(1)
        thumbnails_pane.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        thumbnails_pane.send_keys(Keys.ARROW_UP)
        thumbnails_pane.send_keys(Keys.ARROW_UP)
        thumbnails_pane.send_keys(Keys.ARROW_UP)
        time.sleep(1)

    photo_collection.download_pictures(output_folder)


if __name__ == '__main__':
    get_parentzone_photos()
