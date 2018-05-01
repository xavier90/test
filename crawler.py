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
import threading



class WebPage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self):
        super(WebPage, self).__init__()
        self.loadFinished.connect(self.handleLoadFinished)
        self.cur_product_array = []
        self.flag_download = False
        


    def setHelperPara(self, categoryName, outfile):
        self.categoryName = categoryName
        self.outfile = outfile

    def setCategoryDic(self, search_dic, category_id):
        self.search_dic = search_dic
        self.category_id = category_id

    def start(self, urls, flag_download):
        self._urls = iter(urls)
        self.flag_download = flag_download
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
            QtWidgets.qApp.quit()

            # # after download finished, close file
            # if not self.flag_category_or_detail:
            #     self.outfile.write(']')
            #     self.outfile.close()

    def handleLoadFinished(self):
        self.toHtml(self.processCurrentPage)


    # get product url array
    def getProductUrlArray(self, html):
        soup = bs.BeautifulSoup(html, 'html.parser')
        self.cur_product_array += ["https://www.crateandbarrel.com"+e['href'] for e in soup.select("a.product-miniset-thumbnail")]
        
    

if __name__ == '__main__':
    start_urls = module.get_start_urls()
    
    search_dic, category_id = Util.category()
    outfile = open('result.json', 'a')
    outfile.write('[\n')
    target_url = []

    def cate_worker(search_dic, category_id, cate, outfile, start_urls):
        app = QtWidgets.QApplication(sys.argv)
        webpage = WebPage()
        webpage.setCategoryDic(search_dic, category_id)
        process = psutil.Process(os.getpid())
        webpage.setHelperPara(cate, outfile)

        webpage.start(start_urls[cate], False)
        global target_url
        target_url = list(set(webpage.cur_product_array))
        sys.exit(app.exec_())

    def download_worker(search_dic, category_id, cate, outfile, target_url):
        app = QtWidgets.QApplication(sys.argv)
        webpage = WebPage()
        webpage.setCategoryDic(search_dic, category_id)
        process = psutil.Process(os.getpid())
        webpage.setHelperPara(cate, outfile)
        webpage.start(target_url, True)
        sys.exit(app.exec_())

    for cate in start_urls:

        print "[ DM_info ] " + cate
        worker1 = threading.Thread(target=cate_worker, args=(search_dic, category_id, cate, outfile, start_urls,))
        worker1.start()
        worker1.join()


        print "[ DM_info ] start downloading product for " + cate
        worker2 = threading.Thread(target=download_worker, args=(search_dic, category_id, cate, outfile, target_url,))
        worker2.start()
        worker2.join()



