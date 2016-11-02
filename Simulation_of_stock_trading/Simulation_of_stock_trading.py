# -*- coding:utf-8 -*-  
"""
@Version: ??
@Author: Dyson
@Contact: Weaver1990@163.com
@File: Simulation_of_stock_trading.py
@Time: 2016/10/25 22:41
@Instruction：不考虑除权等大幅度高低开的因素，暂时只支持一个股票买卖
"""
import set_log #log_obj.debug(文本)  "\x1B[1;32;41m (文本)\x1B[0m"
import sys
import random
import numpy as np
import matplotlib.dates
import matplotlib.finance
import matplotlib.pyplot
import time
log_obj = set_log.Logger('Simulation_of_stock_trading.log', set_log.logging.WARNING, set_log.logging.DEBUG)
log_obj.cleanup('Simulation_of_stock_trading.log', if_cleanup = True) # 是否需要在每次运行程序前清空Log文件
file_path1 = 'D:\Git_Clone\Single_Files\SZ#002549.csv'
file_path2 = 'D:\Git_Clone\Single_Files\SZ#300137.csv'

def initialization(stock_num):
    """
    初始化程序，准备数据
    :return: 股票历史数据
    """
    if_right_input = '1' <= stock_num <= '2'
    log_obj.debug(if_right_input)
    if not if_right_input:  # 没有正确输入则报错
        print "Don't have data No.%s" % stock_num
        sys.exit()
    file_name = ''.join(['stock', stock_num, '.csv'])
    start_day = int(random.uniform(80, 300))  # 随机获取开始炒股的起始日期
    o, h, l, c = np.loadtxt(file_name, delimiter = ',', skiprows = 2,
                            usecols = (1, 2, 3, 4), unpack = True)
    date = np.loadtxt(file_name, dtype = str, delimiter = ',', skiprows = 2,
                            usecols = (0,), unpack = True)
    # 为了使每次游戏都不重复
    o = o[-start_day:]
    h = h[-start_day:]
    l = l[-start_day:]
    c = c[-start_day:]
    date = date[-start_day:]
    
    f = open(file_name, 'r')
    name = f.readline()
    f.close()
    # # 初始化持仓表
    # stock_book[stock_num] = 0

    # name = name.decode('gbk', 'replace').encode('utf8')
    
    return o, h, l, c, date, stock_num

def data_contrl():
    # 防止多次数据初始化
    stock_num = raw_input("Choose a stock data(1-2):\n")
    if stock_num not in stocks.keys():
        stocks[stock_num] = initialization(stock_num)
        return stocks[stock_num]
    else:
        return stocks[stock_num]

def show_k_bar(stock_data, title = None, bar_num = 30):
    print 'Showing stock No.%s' % str(stock_data[5])
    time.sleep(2)
    # 规定第一天的数据为K线图里的第31根
    stock_data = [arr[30 + day - bar_num - 1: 30 + day] for arr in
                  stock_data if type(arr) == np.ndarray]
    log_obj.debug2('stock_data', stock_data)
    
    #  主要刻度
    mondays = matplotlib.dates.WeekdayLocator(matplotlib.dates.MONDAY)
    # 次要刻度
    alldays = matplotlib.dates.DayLocator()
    mondayFormatter = matplotlib.dates.DateFormatter('%Y/%m/%d') # 2011/10/10

    fig, ax = matplotlib.pyplot.subplots() # subplot(numRows, numCols,
    # plotNum)
    fig.set_size_inches(6.4 * 2, 4.8 * 2)
    log_obj.debug2('fig', fig)
    log_obj.debug2('ax', ax)
    fig.subplots_adjust(bottom=0.2)
    
    
    # xaxis横坐标
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(mondayFormatter)
    # ax = matplotlib.pyplot.subplot2grid((6, 4), (1, 0), rowspan = 4, colspan = 4,
    #                        axisbg = 'w')

    log_obj.debug2('type(ax)', type(ax))
    matplotlib.finance.candlestick2_ohlc(ax, stock_data[0], stock_data[1],
                                         stock_data[2], stock_data[3],
                                         width=0.6)
    ax.xaxis_date()
    ax.autoscale_view()

    matplotlib.pyplot.setp(matplotlib.pyplot.gca().get_xticklabels(),
                           rotation = 45, horizontalalignment = 'right')
    matplotlib.pyplot.title(title.decode('utf8'))
    # matplotlib.pyplot.xticks(xrange(len(stock_data[0])), date)
    matplotlib.pyplot.show()
    return

    
def trade(b_or_s):
    """
    股票交易
    """
    stock_data = data_contrl()
    stock_num = stock_data[5]
    max_bar_num = day + 30 -1
    bar_num = int(raw_input("How many bars do you like in the chart (<=%d)\n"
                         % max_bar_num))
    log_obj.debug2('type(bar_num)', type(bar_num))
    while int(bar_num) <= int(max_bar_num):
        show_k_bar(stock_data, title = 'Day ' + str(day), bar_num = bar_num)
        print "What's the price"
        price = float(raw_input("Enter here:\n"))
        print "How many would you like to %s(100 integer times)" % b_or_s
        num = int(raw_input("Enter here:\n"))
        if num % 100 == 0:
            # 检查是否持有此类股票
            if stock_num not in stock_book.keys():
                stock_book[stock_num] = 0
            shareholding = stock_book[stock_num]
            # 检查是否能成交
            tradable = if_tradable(price, shareholding, stock_data, num,
                                   b_or_s)
            log_obj.debug2('tradable', tradable)
            if tradable:
                if b_or_s == 'buy':
                    trade_history.append([price, num, 'stock No.%s' % stock_num])
                    cash[day-1] -= price * num
                    stock_book[stock_num] += num
                elif b_or_s == 'sell':
                    trade_history.append([price, -num, 'stock No.%s' % stock_num])
                    cash[day - 1] += price * num
                    stock_book[stock_num] -= num
            else:
                trade_history.append([price, "Fail to %s" % b_or_s])
        else:
            print "Wrong !"
        is_that_all = raw_input("Is that all you need(YES/NO)\n")
        if is_that_all.upper() == 'YES':
            break
    return

def buy():
    trade('buy')
    return
def sell():
    trade('sell')
    return

def if_tradable(price, shareholding, stock_data, num, b_or_s):
    # stock_data ----> o, h, l, c, date, name
    # 不能成交的情况：
    # 1.可用资金不足
    # 2.持有股票不足（卖的时候）
    # 3.报价不在第二天的价格波动范围内
    log_obj.debug2('price * num > cash[day-1]', price * num > cash[day-1])
    log_obj.debug2('cash[day-1]',cash[day - 1])
    if price * num > cash[day-1]:
        print "Don't have enough money !!!!"
        return False
    h = stock_data[1][30 + day]
    l = stock_data[2][30 + day]
    log_obj.debug2('day %d high price:' % day, h)
    log_obj.debug2('day %d low price:' % day, l)

    if b_or_s == 'sell' and shareholding < num:
        print "Don't have enough share!"
        return False
    
    if l <= price <= h:
        return True
    else:
        return False
    
def check():
    print "Showing daily bar chart"
    show_k_bar(data_contrl(), title = 'Day ' + str(day))
    return
    
if __name__ == '__main__':
    global day
    day = 1
    
    # 初始化资金
    global cash
    cash = np.zeros(1000)
    cash[0] = 1000000
    # print "And you now have ONE million dollars !!!"
    # time.sleep(2)
    # print "Come on ! Make it one billion ! \n\n"
    # time.sleep(2)
    # print "Attention !"
    # time.sleep(2)
    # print "You are not a pro stock trader \n You have a steady job \n" \
    #       "You work hard and you dont have the time to check the " \
    #       "stock market \n You have to tell me what to do on the next " \
    #       "trading day."
    # time.sleep(10)
    # while 1:
    #     if_known = raw_input("Do you understand what\'s going on here ??("
    #                          "YES/NO)\n")
    #     if if_known.upper() == 'YES':
    #         print "OK, here we go !"
    #         break
    #     else:
    #         print "WTF ??"
    # 用来记录持有哪些股票
    global trade_history
    global stock_book
    global stocks
    trade_history = []
    stock_book ={}
    stocks = {}
    
    while 1:
        print "\n\n\n"
        print "It's day %d \n" % day
        if trade_history:
            # 如果有交易记录
            print "Your trade history:\n", trade_history
            print "Your balance: ",cash[day-2]
            print "Your stock book", stock_book
            # 更新期初资金
            if day > 1:
                cash[day - 1] = cash[day - 2]
        while 1:
            what_to_do = raw_input("What do you want to do next (buy/sell/check/pass)\n")
            if what_to_do == 'buy':
                buy()
            if what_to_do == 'sell':
                sell()
            if what_to_do == 'check':
                check()
            if what_to_do == 'pass':
                break
            if what_to_do not in ['buy', 'sell', 'check', 'pass']:
                print "WTF ??"
        day += 1
                

        
    
    
        
