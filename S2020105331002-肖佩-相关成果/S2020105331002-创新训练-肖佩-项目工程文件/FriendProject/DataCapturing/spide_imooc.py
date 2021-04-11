# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# -*- coding: utf-8 -*-
import requests
import re
import json
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content.decode("utf-8")
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<div class="box">.*?lecturer-info.*?<span>(.*?)</span>.*?shizhan-intro-box.*?title=".*?">'
                         '(.*?)</p>.*?class="grade">(.*?)</span>.*?imv2-set-sns.*?</i>'
                         '(.*?)</span>.*?class="big-text">(.*?)</p>.*?shizan-desc.*?>'
                         '(.*?)</p>.*?</div>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'teacher': item[0],
            'title': item[1],
            'grade': item[2],
            'people':item[3],
            'score': item[4],
            'describe': item[5]
        }

def write_to_file(content):
    with open('imooctest.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()



def main():
    url = 'https://coding.imooc.com/?page=1'
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    main()
