# coding:utf-8

import sys
import importlib
importlib.reload(sys)
import os

from pdfminer.pdfparser import PDFParser, PDFDocument
# from pdfminer.pdfparser import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import  PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

'''
 解析pdf 文本，保存到txt文件中
'''

# path = "../pdf" #文件夹目录
# files= os.listdir(path) #得到文件夹下的所有文件名称
# s = []
# for file in files: #遍历文件夹
#      if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
#           f = open(path+"/"+file); #打开文件
#           iter_f = iter(f); #创建迭代器
#           str = ""
#           for line in iter_f: #遍历文件，一行行遍历，读取文本
#               str = str + line
#           s.append(str) #每个文件的文本存到list中



def parse():

    print("test")
    path = r'..\\pdf'
    files= os.listdir(path) #得到文件夹下的所有文件名称
    i = 0 #计数，test态，i为10则停止。
    for file in files: #遍历文件夹
        print("file: ", file)
        if os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
            # f = open(path+"/"+file) #打开文件
            continue
        # subfile = r'..\\pdf\\0a2df74bbc31.pdf'
        fp = open('..\\pdf\\'+str(file), 'rb') # 以二进制读模式打开
        #用文件对象来创建一个pdf文档分析器
        praser = PDFParser(fp)
        # 创建一个PDF文档
        doc = PDFDocument()
        # 连接分析器 与文档对象
        praser.set_document(doc)
        doc.set_parser(praser)
        # 提供初始化密码
        # 如果没有密码 就创建一个空的字符串
        doc.initialize()
        # 检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
        # print("test1")
            raise PDFTextExtractionNotAllowed
        else:
            # 创建PDf 资源管理器 来管理共享资源
            rsrcmgr = PDFResourceManager()
            # 创建一个PDF设备对象
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            # 创建一个PDF解释器对象
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            # 循环遍历列表，每次处理一个page的内容
            for page in doc.get_pages(): # doc.get_pages() 获取page列表
                interpreter.process_page(page)
                # 接受该页面的LTPage对象
                layout = device.get_result()
                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
                for x in layout:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        with open(r'..\\result\\'+ str(i) +'.txt', 'a', encoding="utf-8") as f:
                            results = x.get_text()
                            # print("result:" + results)
                            f.write(str(results) + '\n')
        i += 1;
        if i >= 20030:
            break;    

if __name__ == '__main__':
    parse()


