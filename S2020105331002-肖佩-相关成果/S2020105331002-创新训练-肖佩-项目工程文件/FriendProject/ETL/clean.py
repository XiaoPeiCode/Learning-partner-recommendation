
import pymysql
import numpy as np
import re

# 连接数据库
def creat_MysqlDB():
    mydb = pymysql.connect(
        host="localhost",
        user="root",
        passwd="12345678",
        database="mooc_project"
    )
    return mydb

if __name__ == '__main__':

    mydb = creat_MysqlDB()
    #创建游标对象
    mycursor = mydb.cursor()
    sql = 'select course_score from courses_list'
    mycursor.execute(sql)

    res = mycursor.fetchall()  # 获取每个用户的学习路径为一个返回
    score = np.array(res)
    # print(res)

    sql = 'select course_id from courses_list'
    mycursor.execute(sql)

    res = mycursor.fetchall()
    id = np.array(res)

    sql = 'select course_duration from courses_list'
    mycursor.execute(sql)

    res = mycursor.fetchall()
    duration = np.array(res)


    def normalization(data):
        _range = np.max(data) - np.min(data)
        return (data - np.min(data)) / _range


    def standardization(data):
        mu = np.mean(data, axis=0)
        sigma = np.std(data, axis=0)
        return (data - mu) / sigma

    def updatedata(id, score):
        x = 0
        for i in id:
            x1 = int(id[x])
            x2 = float(score[x])
            sql = 'update courses_list set course_score = {value1} where course_id = {value2}'.format(value1 = x2, value2 = x1)
            mycursor.execute(sql)
            mydb.commit()
            x = x + 1

    def updatedata_time(id,duration):
        x = 0
        for i in id:
            x1 = int(id[x])
            x2 = str(duration[x])


    n_score = normalization(score)    #归一化
    print(n_score)

    # updatedata(id, n_score)
    mycursor.close()
    mydb.close()

    x=0
    for i in duration:
        time = str(duration[x])
        time = re.sub(r'\s+',"",time)
        time = re.sub(r'\'\]',"",time)
        time = re.sub(r'\[\'',"",time)
        hour = re.sub(r'小.*$',"",time)
        hour = re.sub(r'..分',"",hour)
        hour = re.sub(r'.分',"",hour)
        minute = re.sub(r'.小时',"",time)
        minute = re.sub(r'分',"",minute)
        if hour!="":
            hour = int(hour)
        else:
            hour = 0
        minute = hour*60+int(minute)
        x=x+1
        print(minute)