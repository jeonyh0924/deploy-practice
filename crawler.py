import imghdr
from django.core.files.uploadedfile import SimpleUploadedFile
from selenium import webdriver
import time
import re
import requests
from datetime import datetime
from config.settings.base import CHROME_DRIVER
from mappings.models import Cast
from mappings.models import Movie, Stillcut
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Chrome(CHROME_DRIVER)
time.sleep(5)
driver.get('https://www.cgv.co.kr/movies/')
driver.find_element_by_css_selector('div.nowshow input').click()
time.sleep(1)
driver.find_element_by_class_name('btn-more-fontbold').click()
time.sleep(20)
url_list = driver.find_elements_by_xpath("//ol/li/div[@class='box-image']/a")
detail_urls = [url.get_attribute("href") for url in url_list]
time.sleep(2)
for url in detail_urls:
    driver.get(url)
    time.sleep(4)
    try:
        driver.find_element_by_class_name('sect-error')
    except NoSuchElementException:
        driver.get(url)
        time.sleep(4)
        try:
            title = driver.find_element_by_css_selector('div.title strong').text
            spec = driver.find_elements_by_css_selector('div.spec dd')
            clean_spec = [dd.text for dd in spec]
            director = clean_spec[0]
            actor_list = re.split(',', clean_spec[2])
            genre = re.split(':', driver.find_elements_by_css_selector('div.spec dt')[2].text)[1]
            running_time = int(re.search(r'[0-9]+', clean_spec[4].split(',')[1]).group())
            opening_date = clean_spec[5]
            story = driver.find_element_by_css_selector('div.sect-story-movie div').text.strip().replace('\n', '<br>')
            image_url = driver.find_element_by_css_selector('div.box-image a').get_attribute("href")
            img_response = requests.get(image_url)
            img_data = img_response.content
            ext = imghdr.what('', h=img_data)
            main_image = SimpleUploadedFile(f'{title}.{ext}', img_data)
            instance = Movie.objects.create(
                title=title,
                director=director,
                duration_min=running_time,
                opening_date=datetime.strptime(opening_date, '%Y.%m.%d').date(),
                description=story,
                genre=genre,
                main_img=main_image,
            )
            for actor in actor_list:
                Cast.objects.create(movie=instance, actor=actor)
            time.sleep(1)
            driver.find_elements_by_css_selector('ul.tab-menu li a')[2].click()
            time.sleep(2)
            stillcuts = driver.find_elements_by_css_selector('div#stillcut_list img')
            stillcut_urls = [img.get_attribute("src") for img in stillcuts][:5]
            index = 1
            for stillcut_url in stillcut_urls:
                stillcut_response = requests.get(stillcut_url)
                stillcut_data = stillcut_response.content
                ext = imghdr.what('', h=stillcut_data)
                stillcut_image = SimpleUploadedFile(f'{title}_{index}.{ext}', stillcut_data)
                Stillcut.objects.create(movie=instance, image=stillcut_image)
                index += 1
            time.sleep(1)
        except NoSuchElementException:
            pass
            time.sleep(1)