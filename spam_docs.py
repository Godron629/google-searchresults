import logging
import urllib
import re
from bs4 import BeautifulSoup
from pyjsparser import PyJsParser

logger = logging.getLogger()
logger.setLevel(logging.INFO)


if __name__ == "__main__":

    url = 'https://docs.google.com/forms/d/e/1FAIpQLSfuCdfkfq31Xsz6hsGFLviEna4_em2VVzCoJZIALduQs_NEeg/viewform?usp=sf_link'

    page = urllib.urlopen(url).read()
    soup = BeautifulSoup(page, 'html.parser')

    js_answers = soup.find_all('script', text=re.compile(r'FB_PUBLIC_LOAD_DATA'))[0].text

    p = PyJsParser()
    js_answers = p.parse(js_answers)

    list_of_answers = js_answers['body'][0]['declarations'][0]['init']['elements'][1]['elements'][1]['elements']
    # figure out a way of identifying answers after parser, write some recursive filter maybe (or look one up)
