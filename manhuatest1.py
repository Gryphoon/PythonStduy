# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os

class Spider:
    def __init__(self):
        self.siteURL = 'http://m.chuiyao.com/manhua/3670/'

    #获取目录页面
    def getPage(self):
        url = self.siteURL
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read()

    def getPages(self,url):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read()


    #获取目录网址
    def getContents(self):
        page = self.getPage()
        Pattern =re.compile('<div class="chapter-list" id="chapterList">(.*?)</div>',re.S)
        s1 = re.findall(Pattern,page)
        pattern = re.compile('href=\"(.*?)\" ',re.S)
        contents= re.findall(pattern, str(s1))
        return contents

    #获取目录名字
    def getURLs(self):
        page = self.getPage().decode('utf-8')
        pattern = re.compile('html\" title=\"(.*?)\" target=\"\">',re.S)
        urls = re.findall(pattern,page)
        #str_s = str(urls).replace('u\'','\'')
        #name = str_s.decode("unicode-escape")
        return urls

    #文件夹
    def mkdir(self,path):
        path = path.strip()
        isExists=os.path.exists(path)
        if not isExists:
            print u"新建了名字叫做",path,u'的文件夹'
            os.makedirs(path)
            return True
        else:
            print u"名为",path,'的文件夹已经创建成功'
            return False

    #提取下载图片的网址
    def saveImageUrls(self,url):
        page = self.getPages(url)
        pattern = re.compile('.*?parseJSON\(\'\[(.*?)\]\'\)', re.S)
        items = re.findall(pattern, page)
        a = str(items).replace( '\\', '')
        pattern = re.compile('\"(.*?)\"', re.S)
        item = re.findall(pattern, a)
        return item

    #下载图片
    def saveImg(self,imageURL, fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        print  fileName
        f.close()

    #运行
    def start(self):
        contents = self.getContents()
        names = self.getURLs()
        for name in range(len(names)):
            self.mkdir(names[name])
            url = contents[name]
            imageUrls = self.saveImageUrls(url)
            for x in range(len(imageUrls)):
                path = 'F:\\Python\\Crawler\\manhua\\'+names[name]+'\\'+str(x)+'.jpg'
                isExists = os.path.exists(path)
                if not isExists:
                    self.saveImg(imageUrls[x], path)
                else:
                    print u"名为", path, '已经存在'


spider=Spider()
spider.start()


