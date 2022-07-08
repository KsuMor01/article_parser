import requests
import argparse
from bs4 import BeautifulSoup
import os


class ArticleParser(object):
    """This class provides getting article text, formatting and saving in file."""
    def __init__(self):
        """Constructor"""
        self.url = ''  # goal url
        self.title = ''  # title of article
        self.paragraphs = []  # list of paragraphs of article
        self.formatted_text = ''  # the formatted text
        self.line_len = 0  # len of the current line formatted text
        self.args = {}  # input settings arguments

    def get_args(self):
        """Gets a URL from terminal command and settings from settings.txt"""

        parser = argparse.ArgumentParser(description='URL parser.This application provides a tool to get '
                                                     'an article text from an URl.')
        parser.add_argument('--url', type=str, help='input URL')

        args = parser.parse_args()
        self.url = args.url

        with open('settings.txt', 'r') as f:
            settings = f.readlines()

        if settings[0][settings[0].index(':')+2:-1] == 'yes':
            self.args['print_urls'] = True
        else:
            self.args['print_urls'] = False

        if settings[1][settings[1].index(':')+2:-1] == 'yes':
            self.args['print_title'] = True
        else:
            self.args['print_title'] = False
        self.args['line_len_limit'] = int(settings[2][settings[2].index(':')+2:-1])

    def getter(self):
        """Gets the text of article from the URL"""
        rs = requests.get(self.url)
        rs.raise_for_status()

        root = BeautifulSoup(rs.content.decode('utf-8', 'ignore'), 'html.parser')
        body = root.find(attrs={'itemprop': 'articleBody'})

        try:
            self.paragraphs = body.find_all("p")
        except AttributeError:
            self.paragraphs = root.find_all("p")
        self.title = root.head.title.get_text()

        empty_line = '\n\n   '

        if self.args['print_urls']:
            self.add_word(self.url)
            self.add_word(empty_line)
        if self.args['print_title']:
            self.add_strip(self.title)
            self.add_word(empty_line)

    def add_word(self, word):
        """Instrument to add a word in formatted text"""
        # if length of the word > line_len_limit
        if len(word) > self.args['line_len_limit']:
            for part_of_word in [word[it:it + self.args['line_len_limit']]
                                 for it in range(0, len(word), self.args['line_len_limit'])]:
                if self.line_len + len(part_of_word) > self.args['line_len_limit']:
                    self.formatted_text += '\n'
                    self.line_len = 0
                self.formatted_text += part_of_word + ' '
                self.line_len += len(part_of_word) + 1

        else:
            if self.line_len + len(word) > self.args['line_len_limit']:
                self.formatted_text += '\n'
                self.line_len = 0
            self.formatted_text += word + ' '
            self.line_len += len(word) + 1

    def add_strip(self, strip):
        """Instrument to add a few words in formatted text"""
        for word in strip.split():
            self.add_word(word)

    def preprocess_link(self, paragraph):
        """Finds all links in paragraph and makes them absolute if not"""
        links = {}
        for link in paragraph.find_all('a'):
            #  make link absolute if it is not
            if not link.get("href").startswith('http'):
                abs_link = self.url[:self.url.index('/', self.url.index('://') + 3)] + link.get("href")
            else:
                abs_link = link.get("href")
            links[link.text.strip()] = abs_link
        return links


    def formatter(self):
        """Formats the raw text in the goal format"""
        for paragraph in self.paragraphs:
            # find all links in paragraph
            if self.args['print_urls']:
                links = self.preprocess_link(paragraph)
                for strip in paragraph.stripped_strings:
                    self.add_strip(strip)
                    #  add link in text
                    if strip in links:
                        self.add_word('[' + links[strip] + ']')
            else:
                # add whole paragraph
                self.add_strip(paragraph.text.strip())
            self.add_word('\n\n   ')
            self.line_len = 0

    def writer(self):
        """Writes formatted text in file"""

        outputdir = os.getcwd().replace('\\', '/') + self.url[(self.url.index('://')+2):]
        ind = self.url[::-1].index('/')
        if ind == 0:
            ind = self.url[::-1].index('/', 1)
        outputdir = outputdir[:-ind]
        filename = self.url[-ind:-1]
        if filename.find('.') != -1:
            filename = filename[:filename.index('.')] + '.txt'
        else:
            filename += '.txt'
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)
        filepath = outputdir + filename
        with open(outputdir + filename, 'w') as f:
            f.writelines(self.formatted_text)
            print('Article is written in ', filepath)


# create object ArticleParser
AP = ArticleParser()
# get url from command
AP.get_args()
# get html page from url
AP.getter()
# format text
AP.formatter()
# output formatted text in file
AP.writer()
