import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import requests

import click

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

    driver.get("https://www.parentzone.me/")
    driver.implicitly_wait(10)

    # Fill in email and password
    email_field = driver.find_element_by_xpath('//*[@id="login"]/fieldset/div[1]/input')
    email_field.clear()
    email_field.send_keys(email)

    passwd_field = driver.find_element_by_xpath('//*[@id="login"]/fieldset/div[2]/input')
    passwd_field.clear()
    passwd_field.send_keys(password)
    passwd_field.send_keys(Keys.RETURN)

    # Go to timeline
    driver.get('https://www.parentzone.me/#/timeline')

    # Choose 'Observation' from the dropdown
    dropdown = Select(driver.find_element_by_xpath('//*[@id="filter"]/div[2]/div[4]/div/div[1]/select'))
    dropdown.select_by_value('7')

    # Submit form
    submit_button = driver.find_element_by_id('submit-filter')
    submit_button.click()


    # The page has infinite scrolling, and scrolling by the JS scroll function
    # doesn't seem to work
    # So intead, set up a loop to scroll infinitely, and stop when we
    # stop getting any more photos displaying
    html = driver.find_element_by_tag_name('html')
    old_n_photos = 0
    while True:
        # Scroll
        html.send_keys(Keys.END)
        time.sleep(3)
        # Get all photos
        media_elements = driver.find_elements_by_class_name('img-responsive')
        n_photos = len(media_elements)
        
        if n_photos > old_n_photos:
            old_n_photos = n_photos
        else:
            break

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # For each image that we've found
    for element in media_elements:
        image_url = element.get_attribute('src')
        image_id = image_url.split("&d=")[-1]

        # Deal with file extension based on tag used to display the media
        if element.tag_name == 'img':
            extension = 'jpg'
        elif element.tag_name == 'video':
            extension = 'mp4'
        image_output_url = os.path.join(output_folder, f'{image_id}.{extension}')

        # Only download and save the files 
        if not os.path.exists(image_output_url):
            r = requests.get(image_url, allow_redirects=True)
            open(image_output_url, 'wb').write(r.content)

if __name__ == '__main__':
    get_parentzone_photos()