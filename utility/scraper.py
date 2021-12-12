# import dependencies

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import os


# scraping out the headings

def scrapeheadings():
    page = requests.get(
        'https://economictimes.indiatimes.com/news/economy/agriculture')
    page.encoding = 'utf-8'
    page = page.text
    textlist = []
    soup = BeautifulSoup(page, 'html.parser')
    for content in soup.find_all("div", class_="eachStory"):
        textlist.append(content.get_text())

    headinglist = []
    contentlist = []

    for index in range(len(textlist)):

        dummy = textlist[index].split('IST')

        heading = dummy[0]
        content = dummy[1]

        headinglist.append(heading[:len(heading)-23])
        contentlist.append(content)

    return headinglist, contentlist

# scraping out the href's


def scrapehref():
    page = requests.get(
        'https://economictimes.indiatimes.com/news/economy/agriculture')
    page.encoding = 'utf-8'
    page = page.text
    contentlist = []
    soup = BeautifulSoup(page, 'html.parser')
    for content in soup.find_all("div", class_="eachStory"):
        contentlist.append(content)

    # converting the soup object result to string

    finalstring = ' '.join([str(i) for i in contentlist])

    soup1 = BeautifulSoup(finalstring, 'html.parser')
    links_with_text = []
    for a in soup1.find_all('a', href=True):
        if a.text:
            links_with_text.append(a['href'])

    links_with_text_final = [
        'https://economictimes.indiatimes.com/'+i for i in links_with_text]

    return links_with_text_final


# scraping out images

def scrapeimage():

    page = requests.get(
        'https://economictimes.indiatimes.com/news/economy/agriculture')
    page.encoding = 'utf-8'
    page = page.text
    soup = BeautifulSoup(page, 'html.parser')
    images = []
    for img in soup.find_all("div", class_="eachStory"):
        images.append(img)

    image_urls = []
    for index in range(len(images)):
        a = str(images[index]).split(
            'data-original')[1].split(".jpg")[0]+'.jpg'
        image_urls.append(a[2:])

    return image_urls


# fetching the main content


def fetchcontent():

    links_with_text_final = scrapehref()
    finalcontent = []
    for index in range(len(links_with_text_final)):

        page = requests.get(links_with_text_final[index])
        page.encoding = 'utf-8'
        page = page.text
        contentlist = []
        index = 0
        soup = BeautifulSoup(page, 'html.parser')
        for content in soup.find_all("div"):

            #         print(str(index)+'  '+content.get_text())
            #         print('='*100)

            contentlist.append(content.get_text())
            index += 1

        stringlist = contentlist[122].split('\n')[:-3]
        finalcontent.append(' '.join(stringlist))

    return finalcontent


heading_list, content_list = scrapeheadings()

image_urls = scrapeimage()

final_content = fetchcontent()
