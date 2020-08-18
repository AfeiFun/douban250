import requests
from bs4 import BeautifulSoup
import json
import datebase


def get_one_page(url):
    '''
    获取一页的数据
    '''

    # 组装header和cookie
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59'
    }
    cookies={'bid':'-iv9ZmYXAFM'}

    # 发起request请求，得到网页内容
    r=requests.request('GET',url,headers=headers,cookies=cookies)

    # 组装soup
    soup=BeautifulSoup(r.text,'html.parser')

    # 找到所有电影的tag
    movies=soup.find_all('div',class_='item')
    movies_list=[]
    for movie in movies:      
        try:
            #获取编号
            movie_NO=movie.div.em.string
            # #获取电影名字
            movie_title=movie.find_next('span',class_='title').string
            
            # 获取图片下载地址,并下载到pics文件夹
            # movie_pic_url=movie.find_next('img').attrs['src']
            # pic=requests.request('GET',movie_pic_url,headers=headers,cookies=cookies)
            # with open(r'pics/%s.webp'%movie_NO,'wb') as webp:
            #     webp.write(pic.content)
            
            # 获取图片路径
            movie_pic=r'pics+%s.webp'%movie_NO

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

        # 保存这电影数据到dict
        movie_dict={
            'rank':movie_NO,
            'movie_title':movie_title,
            'movie_pic':movie_pic,
            'movie_director':movie_director,
            'movie_stars':movie_stars,
            'movie_year':movie_year[:4]
        }
        movies_list.append(movie_dict)
    return movies_list 
def get_all_page():
    '''
    获取所有的页面
    '''
    movies_list=[]
    for i in range(10):
        url='https://movie.douban.com/top250'
        url=url+'?start=%d&filter='%(i*25)
        print('正在下载第%d页'%(i+1))

        # 将所有movies_list的值接在一起
        movies_list.extend(get_one_page(url))
    
    return movies_list
def save_movies_into_database(movies_list):
    '''保存数据到database'''
    # 打开数据库连接
    connection=datebase.connect_movie_database()

    # 将movies_list中所有数据写入到数据库
    for movie_dict in movies_list:
        # print('获取到的单个电影的字典数据：',movie_dict)
        datebase.insert_movie_in_database(movie_dict,connection)
    
    # 关闭数据库连接
    connection.close()

def save_movies_into_json(movies_list):
    '''保存数据到json'''
    file_name='douban250.json'
    with open(file_name,'a') as file:
        file.write(json.dumps(movies_list,ensure_ascii=False, indent=4, separators=(',', ':')))


    