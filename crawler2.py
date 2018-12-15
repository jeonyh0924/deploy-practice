import imghdr

# from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from selenium import webdriver
import time
import re
import requests
from datetime import datetime
# from config.settings.base import CHROME_DRIVER
from mappings.models import Movie, Stillcut, Cast, Director, Directing, Casting
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Chrome(CHROME_DRIVER)
driver = webdriver.Chrome('/home/hanoul/chromedriver')

time.sleep(5)
driver.get('https://www.cgv.co.kr/movies/')
time.sleep(5)
driver.find_element_by_css_selector('div.submenu > ul > li:nth-child(2) > a').click()
time.sleep(5)
url_list = []
for i in range(9, 18):
    url_list += driver.find_elements_by_css_selector(f"div.sect-movie-chart ol:nth-child({i}) > li > div.box-image > a")
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
            try:
                eng_title = driver.find_element_by_css_selector('div.title p').text
            except IndexError:
                eng_title = ""
            spec = driver.find_elements_by_css_selector('div.spec dd')
            clean_spec = [dd.text for dd in spec]

            genre = re.split(':', driver.find_elements_by_css_selector('div.spec dt')[2].text)[1]
            age = clean_spec[4].split(',')[0]
            running_time = int(re.search(r'[0-9]+', clean_spec[4].split(',')[1]).group())
            opening_date = clean_spec[5]
            story = driver.find_element_by_css_selector('div.sect-story-movie div').text.strip().replace('\n', '<br>')

            image_url = driver.find_element_by_css_selector('div.box-image a').get_attribute("href")
            img_response = requests.get(image_url)
            img_data = img_response.content
            ext = imghdr.what('', h=img_data)
            main_image = SimpleUploadedFile(f'{title}.{ext}', img_data)
            # thumbnail = Image.open(main_image)
            # image_generator = Thumbnail(source=thumbnail)
            # thumbnail_image = image_generator.generate()

            movie_instance = Movie.objects.create(
                title=title,
                eng_title=eng_title,
                genre=genre,
                age=age,
                duration_min=running_time,
                opening_date=datetime.strptime(opening_date, '%Y.%m.%d').date(),
                description=story,
                main_img=main_image,
                # thumbnail_img=thumbnail_image,
            )

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
                Stillcut.objects.create(movie=movie_instance, image=stillcut_image)
                index += 1
            time.sleep(1)

            driver.find_elements_by_css_selector('ul.tab-menu li a')[1].click()
            # 감독 선택
            director_namespace = driver.find_element_by_css_selector(
                'div.sect-staff-director ul li.clear > div.box-contents dl dd a').text
            director = re.split('\n', director_namespace)[0]
            try:
                eng_director = re.split('\n', director_namespace)[1]
            except IndexError:
                eng_director = ""
            d_image_url = driver.find_element_by_css_selector(
                'div.sect-staff-director ul li.clear > div.box-image a span img').get_attribute("src")
            d_img_response = requests.get(d_image_url)
            d_img_data = d_img_response.content
            ext = imghdr.what('', h=d_img_data)
            director_image = SimpleUploadedFile(f'{title}.{ext}', d_img_data)

            director_instance = Director.objects.create(
                director=director,
                eng_director=eng_director,
                profile_img=director_image
            )

            directing_instance = Directing.objects.create(
                movie=movie_instance,
                director=director_instance
            )

            # 배우 선택
            cast_namespace_list = driver.find_elements_by_css_selector(
                'div.sect-staff-actor ul li > div.box-contents dl dd a')
            c_image_url_list = driver.find_elements_by_css_selector(
                'div.sect-staff-actor ul li > div.box-image a span img')
            cast_list = driver.find_elements_by_css_selector(
                'div.sect-staff-actor ul li > div.box-contents dl dt')
            cast_image_list = []
            for c_image_url in c_image_url_list:
                c_img_response = requests.get(c_image_url.get_attribute("src"))
                c_img_data = c_img_response.content
                ext = imghdr.what('', h=c_img_data)
                cast_image = SimpleUploadedFile(f'{title}.{ext}', c_img_data)
                cast_image_list.append(cast_image)
            index = 0
            for cast_namespace in cast_namespace_list:
                actor = re.split('\n', cast_namespace.text)[0]
                try:
                    eng_actor = re.split('\n', cast_namespace.text)[1]
                except IndexError:
                    eng_actor = ""
                cast_instance = Cast.objects.create(
                    actor=actor,
                    eng_actor=eng_actor,
                    profile_img=cast_image_list[index]
                )
                casting_instance = Casting.objects.create(
                    movie=movie_instance,
                    actor=cast_instance,
                    cast=cast_list[index].text
                )
                index += 1

        except NoSuchElementException:
            pass
            time.sleep(1)