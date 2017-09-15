# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @time: 2017/9/13 10:04
--------------------------------
"""
import sys
import os
import selenium.webdriver
import datetime
import time
import re
import matplotlib.pyplot as plt
import json

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')
import set_log # MyWheels中的自定义类
log_obj = set_log.Logger(u'数据流.log', set_log.logging.WARNING,
                         set_log.logging.DEBUG)
log_obj.cleanup(u'数据流.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件

headers = {'Accept': '*/*',
           'Accept-Language': 'en-US,en;q=0.8',
           'Cache-Control': 'max-age=0',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive'
           }

def initialization():
    # 初始化浏览器
    desired_capabilities = selenium.webdriver.DesiredCapabilities.PHANTOMJS.copy()

    for key, value in headers.iteritems():
        desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
    desired_capabilities['phantomjs.page.customHeaders.User-Agent'] ='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

    return selenium.webdriver.PhantomJS(desired_capabilities=desired_capabilities)


if __name__ == '__main__':
    fig_width = 200 # 图表宽度
    fig_height = 100 # 图表高度
    check_width = 100 # 检查重复数据的范围
    delay = 3 # 获取数据间隔，单位秒
    test_width = 40 # 刷新一次网页后，再读取多少次，才开始判断重复数据（此时会更新每小时的波峰波谷）
    
    x = []
    y = []
    y0 = []
    d = {}
    # 由于min（None，int）永远是None，所以没有用None作为初始值
    max_diff = float('-inf') # 最大价差初始化为负无穷
    min_diff = float('inf') # 最小价差初始化为正无穷
    
    plt.figure(figsize=(fig_width,fig_height))  # 创建绘图对象
    plt.ion() # 实时图像更新
    driver1 = initialization()
    driver2 = initialization()

    i = 0 # 防止头几次数据相同，重复刷新网页
    while True:
        # 由于刚开始运行的时候，数据重复的可能性很大，所以设置一个i，在爬取了一定量的数据时，再进行重复检测
        if i not in range(1,test_width) and len(set(y0)) <= 1 :
            print u'开始读取网页'
            start_time = time.time()
            driver1.get('https://bter.com/trade/BTC_CNY')
            driver2.get('https://www.btctrade.com/')
            print u'读取网页结束，耗时：%s' %(time.time()-start_time)
            i = 0

        price1 = re.search(ur'\d+\.{0,1}\d{0,2}', driver1.title).group()
        price2 = re.search(ur'\d+\.{0,1}\d{0,2}', driver2.title).group()
        price_diff = float(price1) - float(price2) # 实时价差
        
        max_diff = max(max_diff,price_diff)
        min_diff = min(min_diff,price_diff)
        print datetime.datetime.now(), u'=> 报价1：', price1,u'报价2：', price2, u'差价：', price_diff
        print u"本次运行中，最大价差：%s，最小价差：%s" %(max_diff,min_diff)
        #print driver1.title
        #print driver2.title
        
        # 生成日志
        log_obj.info("价差：%s,报价：%s | %s \n" %(price_diff,price1,price2))
        
        # 生成每小时的波峰波谷，json
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        hour = datetime.datetime.now().hour
        if date not in d:
            d[date] = {}
        if hour in d[date]:
            d[date][hour] = [min(min_diff, d[date][hour][0]), max(max_diff,d[date][hour][1])]
        else:
            d[date][hour] = [min_diff, max_diff]
        if i % test_width == 0: # 固定一定次数后刷新json文件
            with open(u'每小时波峰波谷.json','w') as f:
                json.dump(d,f,encoding='utf8')

        # 生成图像
        # X轴，Y轴数据
        y.append(price_diff)
        x.append(datetime.datetime.now())
        
        # 只保留部分数据
        x = x[(fig_width * int(len(x) / fig_width)):]
        y = y[(fig_width * int(len(y) / fig_width)):]
        
        # 用于控制检查重复值的宽度
        y0 = y[(check_width * int(len(y) / check_width)):]
        
        plt.plot(x, y, linewidth=1)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
        plt.pause(0.001)  # 显示图
        time.sleep(delay)
        
        print 
        i = i + 1
