import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import bs4 as bs
import json
import re
import Util
import _CB as module
import gc

import os
import psutil


class WebPage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self):
        super(WebPage, self).__init__()
        self.loadFinished.connect(self.handleLoadFinished)
        self.product_dic = {}
        self.outfile = open('result.json', 'w')
        self.outfile.write('[\n')


    def start_crawler(self, start_url_dic):
        for cate, urls in start_url_dic.items():
            self.flag_download = False
            self.categoryName = cate

            self.start(urls)

    def start(self, urls):
        self.load_cnt += len(urls)
        self._urls = iter(urls)
        self.fetchNext()

    def fetchNext(self):
        try:
            url = next(self._urls)
        except StopIteration:

            return False
        else:
            self.load(QtCore.QUrl(url))
        return True

    def processCurrentPage(self, html):
        url = self.url().toString()
        # do stuff with html...
        if self.flag_download:
            module.downloadProduct(html, url, self.outfile, self.categoryName, self.search_dic, self.category_id) 
            print "[ DM_info ] before collect " + str(process.memory_info()[0])
            gc.collect()
            print "[ DM_info ] after collect " + str(process.memory_info()[0])
        else:
            self.getProductUrlArray(html)

        if not self.fetchNext():

            if not self.flag_download:
                self.flag_download = True
                download_list = list(set(self.cur_product_array))
                # self._urls = iter(download_list)
                self.start(download_list)


            # # after download finished, close file
            # if not self.flag_category_or_detail:
            #     self.outfile.write(']')
            #     self.outfile.close()

    def handleLoadFinished(self):
        self.toHtml(self.processCurrentPage)


    # get product url array
    def getProductUrlArray(self, html):
        soup = bs.BeautifulSoup(html, 'html.parser')
        self.product_dic.setdefault(self.cate, [])
        self.cur_product_array[self.cate] += ["https://www.crateandbarrel.com"+e['href'] for e in soup.select("a.product-miniset-thumbnail")]
        
    


if __name__ == '__main__':
    start_urls = module.get_start_urls()

    app = QtWidgets.QApplication(sys.argv)
    
    webpage = WebPage()

    # process = psutil.Process(os.getpid())

    webpage.start_crawler(start_urls)

    sys.exit(app.exec_())

    
    # for cate in start_urls:
    #     print "[ DM_info ] " + cate

        
    #     print "[ DM_info ] start downloading product for " + cate
    #     target_url = list(set(webpage.cur_product_array))
    #     webpage.start(target_url, True)


    

