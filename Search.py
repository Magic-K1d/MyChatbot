from download import request
from bs4 import BeautifulSoup
import re


class Search(object):
    ''''''

    def __init__(self):
        self.search = ''
        self.pageNum = 1
        self.BT_url = 'http://www.btanh.com/search/'
        self.Bdp_url = 'http://www.sosoyunpan.com/'
        self.Bdp_md5 = BeautifulSoup(request.get(self.Bdp_url, 3).text, 'lxml').find_all('input')[1]['value']
        self.Bdp_result_page = 'http://www.sosoyunpan.com/search.asp?wd=' + self.search + '&so_md5key=' + self.Bdp_md5

    # BeautifulSoup(request.get(self.Bdp_url, 3).text, 'lxml').find('input', name='so_md5key').value
    def BT_search(self, search, fn):
        text_list = []
        cl_list = []
        xl_list = []

        self.search = search
        fun = {'fa': '-first-asc-', 'la': '-last-asc-', 'hd': '-hot-desc-', 'sd': '-size-desc-'}
        url = self.BT_url + self.search + fun[fn] + str(self.pageNum)
        try:
            html = request.get(url, 3)
            html.encoding = 'GBK-2312'
            Soup = BeautifulSoup(html.text, 'lxml')
            body = Soup.find('div', id='wall').find_all('div', class_='search-item')
        except:
            return False

        for item in body:
            text = item.find('div', class_='item-list').find('p')
            # 去除email模块script
            try:
                text.a.extract()
                text.script.extract()
            except:
                pass
            # 在文件大小前加上空格以区分
            text.find_all('span')[-1].string.insert_before('  ')

            text = text.get_text()
            link = item.find('div', class_='item-bar').find_all('a')
            cl_link = link[0]['href']
            xl_link = link[1]['href']
            text_list.append(text)
            cl_list.append(cl_link)
            xl_list.append(xl_link)
        return text_list, cl_list, xl_list

    def Bdy_search(self, search):
        href_list = []
        result_text = []

        self.search = search
        self.Bdp_result_page = 'http://www.sosoyunpan.com/search.asp?wd=' + self.search + '&so_md5key=' + self.Bdp_md5
        html = request.get(self.Bdp_result_page)
        html.encoding = 'GBK-2312'
        Soup = BeautifulSoup(html.text, 'lxml')
        result = Soup.find('div', class_='so_list_left flt')
        result_a = result.find_all('div', class_='search_box_list_bt')

        for a in result_a:
            result_text.append(a.get_text())
            html = request.get(a.find('a')['href'])
            a_tmp = BeautifulSoup(html.text, 'lxml').find('div', class_='pan_down').find('a')['href']
            href = request.get(a_tmp, referer=a.find('a')['href'] )
            a_final = BeautifulSoup(href.text, 'lxml').find('div').find('meta')['content'][6:]
            #input(BeautifulSoup(request.get(a_final).text, 'lxml'))
            #if BeautifulSoup(request.get(a_final).text, 'lxml').find('div', id='doc').find('div').id == 'layoutApp':
            #    continue
            href_list.append(a_final)
        return result_text, href_list


Searcha = Search()
if __name__ == '__main__':
    #    x = Searcha.BT_search('ipz', 'hd')  # siro-920
    #    print(x)
    for a in Searcha.Bdy_search('学习资料'):
        print(a)
