import requests
import uuid
import logging
from pydash import last, head

import urllib2
import re 
from bs4 import BeautifulSoup 
import json

from time import sleep
from datetime import datetime


logger = logging.getLogger()
logger.setLevel(logging.INFO)

js_regex = re.compile("var FB_PUB*")


def find_ending_square_bracket(text):
    bracket_stack = []
    indexes_of_brackets = {}
    
    for index, char in enumerate(text):
        if char == '[':
            bracket_stack.append(index)
        if char == ']':
            try: 
                indexes_of_brackets[bracket_stack.pop()] = index
            except IndexError: 
                # There are an uneven number of 
                # braces, dont care about the rest
                break 
            
    
    if not indexes_of_brackets:
        raise ValueError("Could not find matching bracket in - {}".format(text))
    
    return indexes_of_brackets

def get_answers_to_javascript_field(field_id, soup):
    script_text = head(soup.find_all(name="script", text=js_regex))
    script_text = str(script_text).decode('utf-8')
    
    script_text = script_text.split(" = ")[1]
    
    start = len(field_id) + script_text.find(field_id) + 1
    
    js_answers = script_text[start:]
    js_answers = js_answers.replace("\n", "")[:-10]
    
    # Find out where the answers are in the script
    bracket_indexes = find_ending_square_bracket(js_answers)
    
    
    
    answers = js_answers[start+1:end+1] # this is hackey, think of better
    answers = json.loads(answers)
    answer = answers[0]
    

def build_get_request(elements):
    """
    Build GET request params with random strings
    :param list html_fields: beautiful soup parsed html form elements
    """
    request_fields = ''
    rand_string = uuid.uuid4().hex

    for field in elements:
        
        field_name = field.attrs['name']
        field_id = last(field_name.split('.'))
        
        is_drop_down_question = field.findParent().attrs.get('role') == 'listitem'
        
        if is_drop_down_question:
            # Drop down has to be one of the listed answers, not random
            rand_string = get_answers_to_javascript_field(field_id, soup)
            
        request_fields += field_name + "=" + rand_string + '&'

    return request_fields[:-1]  # Remove extra '&' at end


if __name__ == "__main__":

    #url = 'https://docs.google.com/forms/d/e/1FAIpQLSfuCdfkfq31Xsz6hsGFLviEna4_em2VVzCoJZIALduQs_NEeg/viewform?usp=sf_link'
    url = 'https://docs.google.com/forms/d/e/1FAIpQLScTS37wZTmUPWTcdkEbtF5sHQIR-mRiRfR_u5KSxf2VucMeVQ/viewform?'
    logging.basicConfig()
    
    for i in xrange(20000):
        
        if i % 10 == 0:
            # Refresh the page every 5 times
            page = urllib2.urlopen(url)
            soup =  BeautifulSoup(page, 'html.parser')

        elements = soup.find_all(attrs={"name": re.compile("entry.*")})
        request_fields = build_get_request(elements)

        send_url = '/'.join(url.split("/")[:-1]) + "/formResponse?{}".format(request_fields)
        response = requests.get(send_url)
        
        keep_going = "U of L Confessions: Submissions" in response.content
        logger.info(" {} - {} - {}".format(i, datetime.now(), keep_going))
        
        if not keep_going:
            break
        
        sleep(7)

