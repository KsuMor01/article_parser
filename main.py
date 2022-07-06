import os
import requests
import argparse
from html.parser import HTMLParser
from bs4 import BeautifulSoup

class ArticleParser(object):
    """This class provides getting article text, formatting and saving in file."""
    def __init__(self):
        """Constructor"""
        self.url = ''
        self.title = ''
        self.paragraphs = []
        self.formatted_text = ''
        self.text = ''

    def get_url(self):
        parser = argparse.ArgumentParser(description='URL parser')
        parser.add_argument('--url', default='https://lenta.ru/news/2022/07/06/sbp/', type=str,
                            help='a URL to parse')

        args = parser.parse_args()
        print('URL: ', args.url)
        self.url = args.url

    def getter(self):
        rs = requests.get(self.url)
        rs.raise_for_status()

        root = BeautifulSoup(rs.content, 'html.parser')
        self.paragraphs = root.find_all("p")
        self.title = root.find("h1").text.strip()
        print('Title: ', self.title)

    def formatter(self):
        for paragraph in self.paragraphs:
            links = paragraph.find_all('a')

            # if there are links in line
            if links != []:
                for link in links:
                    for strip in paragraph.stripped_strings:
                        self.formatted_text += strip

                        #  add link in text
                        if strip == link.text.strip():
                            #  add head of link if not absolute
                            if not link.get('href').startswith('https'):
                                abs_link = self.url[:self.url.index('/', 8)] + link.get('href')
                            else:
                                abs_link = link.get('href')
                            self.formatted_text += '[' + abs_link + ']'
                        else:
                            self.formatted_text += ' '
            else:
                self.formatted_text += paragraph.text.strip() + '\n'
    def writter(self):
        with open('output.txt', 'w') as f:
            print(self.formatted_text)
            f.writelines(self.formatted_text)


AP = ArticleParser()
AP.get_url()
AP.getter()
AP.formatter()
AP.writter()

