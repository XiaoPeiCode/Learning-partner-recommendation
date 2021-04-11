# -*- coding = utf-8 -*-
# @Time : 2020/11/27 21:46
# @Author : sonder
# @file : __init__.py.py
# @Software: PyCharm
import mysql.connector
import numpy as np


def creat_MysqlDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="imooc_project",
        charset= "utf8"

    )
    return mydb


def learn_hour():
    mydb = creat_MysqlDB()
    mycursor = mydb.cursor()
    for i in range(50):
        sql = 'select count(*) from student_list where user_time between %s and %s;'
        mycursor.execute(sql, (i + 0.001, i + 1))
        res = mycursor.fetchall()
        print((i + 0.001, i + 1), res[0])


def recommand():
    hit = 0
    for i in range(len(train)):
        train_ele = train[i].copy()
        test_ele = test[i]
        predict = []

        train_ele.reverse()
        j = 0
        for c in train_ele[:3]:
            t = g[c].copy()
            t = t.argsort().tolist()
            t.reverse()
            k = 0
            for e in t:
                max_course = [5, 3, 2]
                if e not in train_ele and e not in predict:
                    predict.append(e)
                    k += 1
                    if k == max_course[j]:
                        break
            j += 1
        for p in predict:
            if p in test_ele:
                hit += 1
                break
    print(hit / len(test))


def recommand_hot():
    hit = 0
    for i in range(len(train)):
        train_ele = train[i].copy()
        test_ele = test[i]
        predict = []

        train_ele.reverse()
        j = 0

        all_candidate = None
        user_count = g.sum(axis=0)
        idx = user_count.argsort()
        for k in range(30):
            p = idx[-k - 1]
            if p not in predict and p not in train_ele:
                predict.append(p)
            if len(predict) == 10:
                break
        for p in predict:
            if p in test_ele:
                hit += 1
    print(hit / len(train) / 2)


def recommand_random():
    # 随机N个项目
    import random
    hit = 0
    for i in range(len(train)):
        train_ele = train[i].copy()
        test_ele = test[i]
        predict = []

        train_ele.reverse()
        j = 0

        for k in range(30):
            p = int(random.random() * 1200)
            if p not in predict and p not in train_ele:
                predict.append(p)
            if len(predict) == 10:
                break
        for p in predict:
            if p in test_ele:
                hit += 1
                break
    print(hit / len(train))


def frequency():
    # 统计课程的关联规则

    from apyori import apriori
    result = list(apriori(transactions=records, min_support=0.005, min_confidence=0.1))
    supports = []
    items = []
    confidence_result = []
    for r in result:
        if len(r.items) >= 2:
            supports.append(r.support)
            items.append(r)
            for e in r.ordered_statistics:
                confidence_result.append((e.items_base, e.items_add, e.confidence))

    print(len(items))
    confidence_result.sort(key=lambda x: x[2])
    print(confidence_result[-100:-50])


if __name__ == '__main__':

    mydb = creat_MysqlDB()
    mycursor = mydb.cursor()
    sql = 'select user_id,GROUP_CONCAT(a.course_id),GROUP_CONCAT(course_name) from student_learn a ,courses_list b where user_id in ( select user_id from student_learn group by user_id having count(course_id)>1) and a.course_id = b.course_id group by user_id;'
    print("136")
    mycursor.execute(sql)
    print("138")
    res = mycursor.fetchall()  # 获取每个用户的学习路径为一个返回
    stu_seq = 0
    train_index = []
    records = []

    matrix = np.zeros((len(res), 1200))  # 填充0的矩阵
    train_matrix = np.zeros((len(res), 1200))
    train = []
    test = []
    g = np.zeros((1200, 1200))
    lstm_X = []
    lstm_Y = []
    lstm_test_X = []
    lstm_test_Y = []

    for r in res:

        courses = r[1].split(',')  # 获取每个用户学习的课程编号
        records.append(r[2].split(','))
        courses = list(map(int, courses))  #
        #         matrix[stu_seq][np.array(courses)] = 1
        courses.reverse()
        train_ele = []
        test_ele = []
        last = courses[0]
        test_num = 2
        for i in range(1, len(courses)):
            c = courses[i]

            train_number = 3
            if len(courses) > train_number:
                for j in range(len(courses) - train_number):
                    if len(courses) > train_number + 2 and j > len(courses) - train_number - 2:
                        lstm_test_X.append(courses[j:j + train_number])
                        lstm_test_Y.append(courses[j + train_number])
                    else:
                        lstm_X.append(courses[j:j + train_number])
                        lstm_Y.append(courses[j + train_number])

            if len(courses) > test_num + 3:
                if i < len(courses) - test_num:
                    train_ele.append(c)
                    train_index.append(stu_seq)
                    #                     train_matrix[stu_seq][c] = 1
                    g[last][c] += 1
                    last = c
                else:
                    test_ele.append(c)
            else:
                #                 train_matrix[stu_seq][c] = 1
                g[last][c] += 1
                last = c

        if len(test_ele) > 0:
            train.append(train_ele)
            test.append(test_ele)
        stu_seq += 1

    print(np.count_nonzero(g))
