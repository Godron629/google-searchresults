import requests
import uuid
import logging

import urllib2
import re 
from bs4 import BeautifulSoup 

from time import sleep
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

url = 'www.test.com/'
INTERVAL = 1 
TIMES = 500


def parse_html_page(url):
    """
    Get raw HTML of url and create BeautifulSoup object
    :param string url: website url
    """
    page = urllib2.urlopen(url)
    return BeautifulSoup(page, 'html.parser')
    
def build_get_request(elements):
    """
    Build GET request params with random strings
    :param list html_fields: beautiful soup parsed html form elements
    """
    request_fields = ''
    
    for field in elements:
        rand_string = uuid.uuid4().hex
        field_name = field.attrs['name']
        request_fields += field_name + "=" + rand_string + '&'
        
    return request_fields[:-1]  # Remove extra '&' at end

def send_request(url, second_interval, limit_times=None):
    """
    Send get request to url 
    :param string url: url to send get request to
    :param int second_interval: seconds to wait to send another request
    :param limit_times None|int: number of times to send request - None is inf
    """
    
    log = "{} - {} - {}"
    send_request.counter = 0
    
    def _send():
        response = requests.get(url)        
        send_request.counter += 1
        
        logging.info(log.format(send_request.counter, datetime.now(), response.ok))
        sleep(second_interval)
        
    if limit_times is None:
        while True:
            _send()
    else:
        for i in xrange(limit_times):
            _send()
    
            
if __name__ == "__main__":
        
    soup = parse_html_page(URL)
    
    # Find all form entry fields
    elements = soup.find_all(attrs={"name": re.compile("entry.*")})
    
    request_fields = build_get_request(elements)
        
    # Combine url and request
    send_url = '/'.join(URL.split("/")[:-1]) + "/formResponse?{}".format(request_fields)
    
    send_request(send_url, second_interval=INTERVAL, limit_times=TIMES)    
    