import requests
import argparse
from bs4 import BeautifulSoup

class ArticleParser(object):
    """This class provides getting article text, formatting and saving in file."""
    def __init__(self):
        """Constructor"""
        self.url = ''  # goal url
        self.title = ''  # title of article
        self.paragraphs = []  # list of paragraphs of arcticle
        self.formatted_text = ''  # the formatted text
        self.line_len = 0  # len of the current line formatted text
        self.line_len_limit = 80  # the max len of the line

    def get_url(self):
        """Gets a URL from terminal command"""

        parser = argparse.ArgumentParser(description='URL parser')
        parser.add_argument('--url', default='https://habr.com/ru/post/674798/', type=str,
                            help='a URL to parse')

        args = parser.parse_args()
        print('URL: ', args.url)
        self.url = args.url

    def getter(self):
        """Gets the text of article from the URL"""
        rs = requests.get(self.url)
        rs.raise_for_status()

        root = BeautifulSoup(rs.content.decode('utf-8','ignore'), 'html.parser')
        # print(root)
        body = root.find(attrs={'itemprop': 'articleBody'})
        # print(body)
        try:
            self.paragraphs = body.find_all("p")
        except AttributeError:
            self.paragraphs = root.find_all("p")
        # print(self.paragraphs)

        self.title = root.head.title.get_text()
        print('Title:', self.title)
        self.add_word(self.url)
        self.add_word('\n\n   ')
        self.add_strip(self.title)
        self.add_word('\n\n   ')

    def add_word(self, word):
        """Instrument to add a word in formatted text"""
        if self.line_len + len(word) > self.line_len_limit:
            self.formatted_text += '\n'
            self.line_len = 0
        self.formatted_text += word + ' '
        self.line_len += len(word) + 1


    def add_strip(self, strip):
        """Instrument to add a few words in formatted text"""
        for word in strip.split():
            self.add_word(word)
        # print( '==>', strip)


    def formatter(self):
        """Formats the raw text in the goal format"""
        for paragraph in self.paragraphs:
            print(paragraph)
            # find all links in paragraph
            links = {}
            for link in paragraph.find_all('a'):

                #  make link absolute if it is not
                if not link.get("href").startswith('https'):
                    abs_link = self.url[:self.url.index('/', 8)] + link.get("href")
                else:
                    abs_link = link.get("href")
                links[link.text.strip()] = abs_link
            print(links)

            print('STRIP', strip)
            if links != {}:
                for strip in paragraph.stripped_strings:
                    # print('LINK', link)
                    self.add_strip(strip)
                    #  add link in text
                    if strip in links:
                        self.add_word('[' + links[strip] + ']')
            else:
                # add whole paragraph
                self.add_strip(paragraph.text.strip())
            self.add_word('\n\n   ')
            self.line_len = 0

    def writter(self):
        """Writes formatted text in file"""
        with open('output.txt', 'w') as f:
            # print(self.formatted_text)
            f.writelines(self.formatted_text)

# create object ArticleParser
AP = ArticleParser()
# get url from command
AP.get_url()
# get html page from url
AP.getter()
# format text
AP.formatter()
# output formatted text in file
AP.writter()

