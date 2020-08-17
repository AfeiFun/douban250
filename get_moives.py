import requests
from bs4 import BeautifulSoup
import json


def get_one_page(url):
    '''
    获取一页的数据并将数据加入到douban250.json文件中
    '''
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59'
    }
    cookies={'bid':'-iv9ZmYXAFM'}

    r=requests.request('GET',url,headers=headers,cookies=cookies)
    soup=BeautifulSoup(r.text,'html.parser')

    movies=soup.find_all('div',class_='item')
    movies_list=[]
    for movie in movies:
        
        try:
            #获取编号
            movie_NO=movie.div.em.string
            # #获取电影名字
            movie_title=movie.find_next('span',class_='title').string
            
            # 获取图片下载地址
            movie_pic_url=movie.find_next('img').attrs['src']
            # 保存图片到文件夹
            pic=requests.request('GET',movie_pic_url,headers=headers,cookies=cookies)
            with open(r'pics/%s.webp'%movie_NO,'wb') as webp:
                webp.write(pic.content)
            # 获取图片路径
            movie_pic=r'pics/%s.webp'%movie_NO

            #获取详情字符串
            movie_info=movie.p.text.strip()
            #截取导演字符串
            start=4
            end=movie_info.find(' ',start)
            movie_director=movie_info[start:end]
            #截取主演字符串
            start=movie_info.index('主')+4
            end=movie_info.find(' ',start)
            movie_stars=movie_info[start:end]
            #截取年份
            movie_info=movie_info.replace(' ','')
            start=movie_info.index('\n')+1
            end=movie_info.find('/',start)-1
            movie_year=movie_info[start:end]
        except ValueError as reason:
            movie_stars=''
            print(movie_title,'抓取演员失败',reason)
            pass
        movie_dict={
            'rank':movie_NO,
            'movie_title':movie_title,
            'movie_pic':movie_pic,
            'movie_director':movie_director,
            'movie_stars':movie_stars,
            'movie_year':movie_year
        }
        movies_list.append(movie_dict)
        
    # 保存数据到json文件
    

    file_name='douban250.json'

    with open(file_name,'a') as file:
        file=file.write(json.dumps(movies_list,ensure_ascii=False, indent=4, separators=(',', ':')))


def get_all_page():
    '''
    获取所有的页面
    '''
    for i in range(10):
        url='https://movie.douban.com/top250'
        url=url+'?start=%d&filter='%(i*25)
        print('正在下载第%d页'%(i+1))
        get_one_page(url)
    