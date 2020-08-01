from selenium import webdriver
import time
import csv
import re

def search_product(key):
    driver.find_element_by_id('q').send_keys(key)
    driver.find_element_by_class_name('btn-search').click()
    driver.maximize_window()
    time.sleep(15)

    page = driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[1]').text    #找到最大页数
    page = re.findall('(\d+)',page)[0]

    return page

def get_product():
    '''解析想要的数据'''
    divs = driver.find_elements_by_xpath('//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')
    for div in divs:
        info = div.find_element_by_xpath('.//div[@class="row row-2 title"]/a').text    #商品的名称
        price = div.find_element_by_xpath('.//strong').text + '元'   #商品的价格
        deal = div.find_element_by_xpath('.//div[@class="deal-cnt"]').text    # 商品的付款人数
        name = div.find_element_by_xpath('.//div[@class="shop"]/a').text  # 商品的店铺名称
        print(info,price,deal,name,sep='|')
        with open ('data.csv',mode='a',newline='') as filecsv:
            csvwriter = csv.writer(filecsv,delimiter=',')
            csvwriter.writerow([info,price,deal,name])

def main():
    print('正在爬取第1页数据')
    page = search_product(keyword)
    get_product()

    page_num = 1
    while page_num != page:
        print('*' * 100)
        print('正在爬取第{}页的数据'.format(page_num + 1))
        print('*' * 100)
        driver.get('https://s.taobao.com/search?q={}&s={}'.format(keyword,page_num*44))
        driver.implicitly_wait(10)  #隐式等待时间
        get_product()
        page_num += 1
        time.sleep(1)

if __name__ == '__main__':
    keyword = input('请输入你要搜索的关键字：')
    driver = webdriver.Chrome()
    driver.get('https://www.taobao.com/')
    main()