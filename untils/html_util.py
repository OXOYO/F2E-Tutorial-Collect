#coding=utf-8

import os
from HTMLParser import HTMLParser

import file_utils


class MyHTMLParser(HTMLParser):
    is_a = False
    is_h3 = False
    links = []
    cur_tag_key = ''
    cur_tag_value = ''

    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        # print "Encountered the beginning of a %s tag" % tag
        if tag == 'a':
            self.is_a = True
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.cur_tag_value = value
        else:
            self.is_h3 = True

    def handle_data(self, data):
        if self.is_a:
            self.cur_tag_key = data
        elif self.is_h3:
            self.cur_tag_key = data
            self.cur_tag_value = 'h3'

    def handle_endtag(self, tag):
        if tag == 'a' or tag == 'h3':
            self.is_a = False
            self.is_h3 = False
            if self.cur_tag_key == '' and self.cur_tag_value == '':
                pass
            else:
                self.links.append([self.cur_tag_key, self.cur_tag_value])
                self.cur_tag_key = ''
                self.cur_tag_value = ''


def get_links():
    html_code = file_utils.read2mem('bookmarks.html')
    hp = MyHTMLParser()
    hp.feed(html_code)
    hp.close()
    try:
        os.remove('star.md')
    except FileNotFoundError:
        pass
    file_utils.append2file('star.md', '# F2E资料整理')
    for word in hp.links:
        if word[1] == 'h3':
            file_utils.append2file('star.md', '##' + word[0] + '\n\n')
            print(word[0] + '\n')
        else:
            file_utils.append2file('star.md', '- [' + word[0] + '](' + word[1] + ')\n\n')
            print('- [' + word[0] + '](' + word[1] + ')\n')


get_links()
