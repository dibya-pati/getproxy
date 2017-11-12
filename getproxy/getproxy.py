# coding=utf-8 -*-
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import numpy as np
import os

class getproxy:
    def __init__(self):
        pass
        # print 'getting proxy'

    def getProxy(self,source = r'https://free-proxy-list.net/'):
        url_about = source

        chromedriver = "chromedriver"  # Needed?
        os.environ["webdriver.chrome.driver"] = chromedriver  # Needed?
        options = webdriver.ChromeOptions()
        ##chrome options to test
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1200,1100')

        browser = webdriver.Chrome(chrome_options=options)
        browser.get(url_about)
        src_updated = browser.page_source
        columns = ['ip', 'port', 'code', 'Country', 'Anonymity', 'google', 'https', 'lastChecked']
        iptableDF = pd.DataFrame(columns=columns)

        i = 0
        for next in range(4):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight/8);")
            browser.find_element_by_xpath('''//*[@id="proxylisttable_length"]/label/select/option[3]''').click()
            time.sleep(1)
            src_updated = browser.page_source
            soup = BeautifulSoup(src_updated, 'html5lib')
            # soup = BeautifulSoup(test, 'html5lib')
            for proxytable in soup.find_all('table'):
            #print proxytable
            #print cl_text
                bodyFragment = proxytable.findNext('tbody').findNext('tr')
                if proxytable is not None and 'proxylisttable' in proxytable.get('id'):
                    while bodyFragment:
                        # print map(lambda tags:tags.text,filter(lambda x:not None,bodyFragment.find_all('td')))
                        # print pd.DataFrame(map(lambda tags:tags.text,filter(lambda x:not None,bodyFragment.find_all('td'))),columns = columns)
                        df = map(lambda tags:tags.text,filter(lambda x:not None,bodyFragment.find_all('td')))
                        # print iptableDF.columns
                        if len(df) != 0:
                            iptableDF.loc[i] = df
                            i += 1
                        bodyFragment = bodyFragment.findNext('tr')
                        # print iptableDF.shape

            if next < 3:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
                time.sleep(0.5)
                browser.find_element_by_xpath('''//*[@id="proxylisttable_next"]/a''').click()

        browser.quit()
        # print iptableDF
        # iptableDF.to_csv('iptable.csv',index=False)
        return iptableDF

    def getGoodIP(self,IPTableDf,lastChecked='seconds',countryCode = ' ',https=' '):
        # print IPTableDf.shape
        # print IPTableDfh
        newIP= IPTableDf.loc[IPTableDf['lastChecked'].str.contains(lastChecked),:]

        if countryCode != ' ':
            newIP = newIP.loc[IPTableDf['code'].str.contains(countryCode),:]
        if https.lower() == 'yes':
            newIP = newIP.loc[IPTableDf['https'].str.contains(https),:]

        shape = newIP.sort_values('lastChecked').shape[0]
        # print shape
        if shape != 0:
            return newIP.reset_index().loc[np.random.randint(shape),['ip','port']]
        else:
            return IPTableDf.loc[IPTableDf['lastChecked'].str.contains('minutes'),:]\
                .reset_index().loc[np.random.randint(8),['ip','port']]