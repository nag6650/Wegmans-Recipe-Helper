import requests
import re
from bs4 import BeautifulSoup


def scrape(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    arr = []
    arr.append("")
    regex = re.compile('.*ingredients.*')
    for EachPart in soup.find_all("div", {"class" : regex}):
        arr[0] += EachPart.get_text()

    arr.append("")
    regex = re.compile('.*Ingredients.*')
    for EachPart in soup.find_all("div", {"class" : regex}):
        arr[1] += EachPart.get_text()

    arr.append("")
    regex = re.compile('.*Recipe.*')
    for EachPart in soup.find_all("div", {"class" : regex}):
        arr[2] += EachPart.get_text()

    arr.append("")
    regex = re.compile('.*recipe.*')
    for EachPart in soup.find_all("div", {"class" : regex}):
        arr[3] += EachPart.get_text()

    arr.append("")
    regex = re.compile('.*ingredient.*')
    for EachPart in soup.find_all("ul", {"id" : regex}):
        arr[4] += EachPart.get_text()

    arr.append("")
    regex = re.compile('.*recipe-ingredients.*')
    for EachPart in soup.find_all("div", {"class": regex}):
        arr[5] += EachPart.get_text()

    '''
    for i in arr:
        print i
    '''
    best_string = ""
    best_length = -1;
    for str in arr:
        if(len(str) > 0):
            if(best_length < 1):
                for c in str:
                    if c.isalpha():
                        for c in str:
                            if c.isdigit():
                                best_length = len(str)
                                best_string = str
                                break
            elif (len(str) < best_length):
                for c in str:
                    if c.isalpha():
                        for c in str:
                            if c.isdigit():
                                best_length = len(str)
                                best_string = str
                                break
    return best_string


def parse(string):
    pat = re.compile(r"([0-9])")
    string = (pat.sub(" \\1 ", string))

    return string


def main():
    return parse(scrape("https://www.tasteofhome.com/recipes/easy-pepper-steak/"))

#print main()