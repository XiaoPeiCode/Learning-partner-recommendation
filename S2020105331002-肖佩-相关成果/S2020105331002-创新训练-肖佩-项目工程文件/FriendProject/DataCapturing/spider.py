# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from selenium import webdriver
import re
from bs4 import BeautifulSoup


# 1.爬取网页
def askURL(url):
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    return html

# 2.得到数据
def getData():
    #获取网址
    for i in range(0,50):
        url = "https://www.icourse163.org/home.htm?userId="+ str(1401276559 + i * 5) + "#/home/course"
        html = askURL(url)
        bs = BeautifulSoup(html, "html.parser")
        mooc_list = bs.find_all(class_="f-thide")
        #未取出用户或者未取出时间则跳过
        if len(mooc_list[1].get_text()) == 0 or len(mooc_list[2].get_text()) == 0:
            continue
        else:
            #将学习时间里的数字取出来成为一个数组
            time = re.findall(r'\d', mooc_list[2].get_text())
            t = ""
            for item in time:
                t += item
            # print(mooc_list[1])
            # print(t)
            # 如果该用户学习时间少于10分钟则跳过
            if int(t) < 10:
                continue
        text = ""
        if len(mooc_list) > 2:
            for i in range(1, len(mooc_list) - 1):
                text += mooc_list[i].get_text() + " "
            text += "\n"
            print(text)
            saveData(text)



#3.保存数据
def saveData(text):
    with open('mooc.txt', 'a',encoding='utf-8') as f:  # 在当前路径下，以写的方式打开一个名为'url.txt'，如果不存在则创建
     f.write(text)  # 将text里的数据写入到文本中
     f.close()




if __name__ == '__main__':
    getData()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
