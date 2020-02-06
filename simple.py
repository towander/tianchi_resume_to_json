# -*- coding:utf-8 -*-

import sys
import importlib
importlib.reload(sys)
import os
import re
from tqdm import tqdm
import pdfplumber  # 为了操作PDF
import pandas as pd

def file_batch_process():
    path = "../result"
    s = []  # 存入这个list中
    files = os.listdir(path)
    for file in tqdm(files):
        if not os.path.isdir(file):
            f = open((str(path)+'/'+str(file)).strip(), 'r+', encoding='utf-8')
            resumestr = ""
            for line in f:
                str_line = str(line)
                resumestr = resumestr + str_line
            s.append(resumestr)
            f.close()
    return s        

'''
args:
    s：打开的txt
'''
def find_experience(s):
    count = 0
    resumes_work_experiences = []
    for resume in s:
        resume_work_experiences = []
        position1 = 0
        position2 = 0
        position1 = resume.find('工作经历', position2)
        if position1 == -1:
            count += 0
        else:
            count += 1
    return count

def find_time(resume_list):
    for resume in resume_list:
        date_all = re.findall(r"(\d{4}\.\d{1,2})",resume)
        date_all += re.findall(r"(\d{4}\/\d{1,2})",resume)
        date_all += re.findall(r"(\d{4}.年\d{1,2}.月)",resume)
        date_all += re.findall(r"(\d{4}年\d{1,2}月)",resume)
        for item in date_all:
            print (item)
            f = open("date_result.txt", 'a+', encoding='utf-8')
            f.write(str(item)+"\n")
            f.close()

def find_title(resume_list):
    i = 0
    title_dict = {}
    for resume in resume_list:
        title_all = re.findall(r"\n\n.+?\n\n",resume)
        for item in title_all:
            if len(item.rstrip()) < 10: #移除空格后判断长度
                # print (item)
                f = open("../test_title/" + str(i)+ ".txt", 'a+', encoding='utf-8')
                f.write(str(item).replace(" ","").replace("\n","")+"\n")
                f.close()
                if str(item).replace(" ","").replace("\n","") in title_dict:
                    title_dict[str(item).replace(" ","").replace("\n","")] += 1 #存在该候选title则加1
                else:
                    title_dict[str(item).replace(" ","").replace("\n","")] = 1 #初始化为1
        i += 1
    sort_dict = sorted(title_dict.items(), key=lambda item:item[1], reverse = True)
    for title in sort_dict:
        f = open("../test_title/total_title.txt", 'a+', encoding='utf-8')
        f.write(str(title)+"\n")
        f.close()
    return sort_dict[:64]

if __name__ == '__main__':
    path = "../result_test"
    resume_list = []  # 将所有文件内容存入这个list中
    file_name_list = [] # 存放文件名
    files_read = os.listdir(path)
    for file_read in tqdm(files_read):
        if not os.path.isdir(file_read):
            f_read = open((str(path)+'/'+str(file)).strip(), 'r+', encoding='utf-8')
            file_name_list.append(f_read)
            resumestr = ""
            for line in f_read:
                resumestr += str_line
            resume_list.append(resumestr)
            f_read.close()
    
    # 寻找候选title，并再候选title前插入$$符号
    temp = find_title(resume_list)
    keywords = []
    for item in temp:
        pattern = re.compile("'(.+?)'")
        str_re1= pattern.findall(str(item))
        keywords.append(str_re1[0])
    split_str = ''
    
    # 文本替换、删除、摘取等处理部分
    i = 0 #用于遍历
    for resume in resume_list:
        paras = resume

        # 时间格式标准化 变成年月格式
        date_all = re.findall(r"(\d{4}/\d{1,2})",paras)
        for date in date_all:
            paras = paras.replace(date, date + "&%$")
            paras = paras.replace(date, date.replace('/', '年'))
            paras = paras.replace('&%$', '月')
        date_all = re.findall(r"(\d{4}\.\d{1,2})",paras)
        for date in date_all:
            paras = paras.replace(date, date + "&%$")
            paras = paras.replace(date, date.replace('.', '年'))
            paras = paras.replace('&%$', '月')
        
        #根据统计得到的高频title切分文本
        for keyword in keywords:
            if len(keyword) > 3:
                paras = paras.replace("\n"+keyword, '\n$$'+keyword)

        #根据工作经历、姓名、籍贯、性别、工作经验、项目经验、项目经历等切分文本

        #保存处理过的文本
        f = open("../split_test/"+file_name_list[i].split('.')[0]+".txt", "a+", encoding="utf-8")
        i+=1 # 加1，用于遍历file_name_list
        f.write(paras)
        f.close()