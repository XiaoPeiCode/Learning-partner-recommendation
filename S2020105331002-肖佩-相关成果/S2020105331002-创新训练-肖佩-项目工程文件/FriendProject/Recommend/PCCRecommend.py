# -*- coding = utf-8 -*-
# @Time : 2020/11/28 22:55
# @Author : sonder
# @file : PCCRecommend.py
# @Software: PyCharm
# -*- coding:utf-8 -*-

"""
      加载数据集与测试集，随机选取1000个用户进行计算；
      先计算用户相似度，推荐学习伙伴；
      然后进一步实现了对课程的推荐；

"""
import os
import json
import random
import math

'''该类作业：从文件中加载数据，获取所有用户，并随即选取1000个'''
class FirstRec:
    """
        初始化函数
            filePath: 原始文件路径
            seed：产生随机数的种子
            k：选取的近邻用户个数
            nitems：为每个用户推荐的课程数
            users_1000:随机选取的1000个用户
            train,test:训练集，测试集
    """
    def __init__(self,file_path,seed,k,n_items):
        self.file_path = file_path
        self.seed = seed
        self.k = k
        self.n_items = n_items

        self.users_1000 = self.__select_1000_users()

        self.train,self.test = self._load_and_split_data()

    # 获取所有用户并随机选取1000个
    def __select_1000_users(self):
        print("随机选取1000个用户！")
        if os.path.exists("data/train.json") and os.path.exists("data/test.json"):#如果存在文件

            return list()
        else:
            print("--------debug------")
            print("else")
            print("--------debug------")
            users = set()
            # 获取所有用户
            for file in os.listdir(self.file_path):
                one_path = "{}/{}".format(self.file_path, file)
                print("{}".format(one_path))
                with open(one_path, "r") as fp:
                    for line in fp.readlines():
                        if line.strip().endswith(":"):
                            continue
                        userID, _ , _ = line.split(",")
                        users.add(userID)
            # 随机选取1000个
            users_1000 = random.sample(list(users),1000)
            print(users_1000)
            return users_1000

    # 加载数据，并拆分为训练集和测试集
    def _load_and_split_data(self):
        train = dict()
        test = dict()
        if os.path.exists("data/train.json") and os.path.exists("data/test.json"):
            print("从文件中加载训练集和测试集")
            train = json.load(open("data/train.json"))
            test = json.load(open("data/test.json"))
            print("从文件中加载数据完成")
        else:
            # 设置产生随机数的种子，保证每次实验产生的随机结果一致
            random.seed(self.seed)
            for file in os.listdir(self.file_path):
                one_path = "{}/{}".format(self.file_path, file)
                print("{}".format(one_path))
                with open(one_path,"r") as fp:
                    courseID = fp.readline().split(":")[0]
                    for line in fp.readlines():
                        if line.endswith(":"):
                            continue
                        userID, rate, _ = line.split(",")
                        # 判断用户是否在所选择的1000个用户中
                        if userID in self.users_1000:
                            if random.randint(1,50) == 1:
                                test.setdefault(userID, {})[courseID] = int(rate)
                            else:
                                train.setdefault(userID, {})[courseID] = int(rate)
            print("加载数据到 data/train.json 和 data/test.json")
            json.dump(train,open("data/train.json","w"))
            json.dump(test,open("data/test.json","w"))
            print("加载数据完成")
        return train,test

    """
        计算皮尔逊相关系数
            rating1：用户1的评分记录，形式如{"courseid1":rate1,"courseid2":rate2,...}
            rating2：用户1的评分记录，形式如{"courseid1":rate1,"courseid2":rate2,...}                              
    """
    def pearson(self,rating1,rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        num = 0  #总个数
        for key in rating1.keys():
            if key in rating2.keys():  #只对两用户之间都有评分记录的课程进行计算
                num += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += math.pow(x,2)
                sum_y2 += math.pow(y,2)
        if num == 0:
            return  0
        # 皮尔逊相关系数分母
        denominator = math.sqrt( sum_x2 - math.pow(sum_x,2) / num) * math.sqrt( sum_y2 - math.pow(sum_y,2) / num )
        if denominator == 0:
            return  0
        else:
            return ( sum_xy - ( sum_x * sum_y ) / num ) / denominator

    """
            用户userID进行TopN学习伙伴推荐
                userID：用户ID
    """
    def recommend_friend(self, userID,n):
        '''召回'''
        ## 计算相关系数
        neighborUser = dict()
        for user in self.train.keys():
            if userID != user:
                distance = self.pearson(self.train[userID], self.train[user])
                neighborUser[user] = distance
        '''排序'''
        # 字典排序  根据相关度
        newNU = sorted(neighborUser.items(), key=lambda k: k[1], reverse=True)

        # 返回前n个最可能的学习伙伴
        return newNU[:n]


    """
        用户userID进行课程推荐
            userID：用户ID
    """
    def recommend_course(self,userID):
        '''召回'''
        ## 计算相关系数
        neighborUser = dict()
        for user in self.train.keys():
            if userID != user:
                distance = self.pearson(self.train[userID],self.train[user])
                neighborUser[user]=distance


        '''排序'''
        # 字典排序  根据相关度
        newNU = sorted(neighborUser.items(),key = lambda k:k[1] ,reverse=True)

        '''调整'''
        courses = dict()
        for (sim_user,sim) in newNU[:self.k]: #选取前k个相关系数最大的用户
            for coursesID in self.train[sim_user].keys():
                courses.setdefault(coursesID,0) #
                courses[coursesID] += sim * self.train[sim_user][coursesID]
                #sim是相似度，加个权；相似度 * 相似的人对该课程的评分

        '''对最后结果再排序'''
        newCourses = sorted(courses.items(), key = lambda  k:k[1], reverse=True)
        return newCourses

    """
        推荐系统效果评估函数
            num: 随机抽取 num 个用户计算准确率
        这里是借助对课程的推荐近似计算准确率      
    """
    def evaluate(self,num=30):
        print("开始计算准确率")
        precisions = list()
        random.seed(10)
        for userID in random.sample(self.test.keys(),num):
            hit = 0
            result = self.recommend_course(userID)[:self.n_items] #推荐结果
            for (item,rate) in result:
                if item in self.test[userID]:  # 如果推荐结果再测试集中 hit加1
                    hit += 1
            precisions.append(hit/self.n_items) # 一个用户的推荐的课程的正确数/总数
        return  sum(precisions) / precisions.__len__() #求样本期望

# main函数，程序的入口
if __name__ == "__main__":
    file_path = "../DataCapturing/netflix/training_set"
    seed = 30
    k = 15
    n_items =10
    f_rec = FirstRec(file_path,seed,k,n_items)

    # 计算用户 195100 和 1547579的皮尔逊相关系数
    # r = f_rec.pearson(f_rec.train["195100"],f_rec.train["1547579"])
    # print("195100 和 1547579的皮尔逊相关系数为：{}".format(r))
    # # 为用户195100进行课程推荐
    # result = f_rec.recommend("195100")
    # print("为用户ID为：195100的用户推荐的课程为：{}".format(result))

    print()
    print("--------------用户相关系数计算模块---------------")
    # 计算用户 2497991 和 845136的皮尔逊相关系数
    r = f_rec.pearson(f_rec.train["2497991"],f_rec.train["845136"])
    print("2497991 和 845136的皮尔逊相关系数为：{}".format(r))
    # r = f_rec.pearson(f_rec.train["2497991"], f_rec.train["283932"])
    # print("2497991 和 283932的皮尔逊相关系数为：{}".format(r))
    r = f_rec.pearson(f_rec.train["2497991"], f_rec.train["2088993"])
    print("2497991 和 2088993的皮尔逊相关系数为：{}".format(r))
    r = f_rec.pearson(f_rec.train["2497991"], f_rec.train["2497991"])
    print("2497991 和 2497991的皮尔逊相关系数为：{}".format(r))


    print()
    print("--------------学习伙伴推荐模块---------------")
    # 为用户2497991推荐学习伙伴
    friends = f_rec.recommend_friend("845136",10)
    print("为用户ID为：845136的用户推荐的10个学习伙伴为：")
    for friend in friends:
        print(friend)


    print()
    print("--------------课程推荐模块---------------")
    # 为用户2497991进行课程推荐
    courses = f_rec.recommend_course("2497991")
    print("为用户ID为：2497991的用户推荐的课程为：")
    for course in courses[:n_items]:
        print(course)


    print()
    print("--------------评估模块---------------")
    print("算法的推荐准确率为: {}".format(f_rec.evaluate()))

