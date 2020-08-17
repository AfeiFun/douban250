import requests
from bs4 import BeautifulSoup


## 获取数据

def get_movies_info_list(url,headers={},cookies={}):
    
    # 发起请求，获得response
    r=requests.request('GET',url,headers=headers,cookies=cookies)

    ## 解析数据
    soup=BeautifulSoup(r.text,'html.parser')
    # 找到所有的电影项目
    movie_items=soup.find_all('div',class_='item')

    #保存每个电影数据
    # movie_lists=[]
    # for movie_item in movie_items:
        # movie_dict={}
        # 查找电影名
        movie_title=movie_items[0].find_next('span',class_='title').string
        # movie_dict['movie_title']=movie_title
        # 查找图片地址
        movie_pic_address=movie_item[0].find_next('image')
        print(movie_pic_address)
        # movie_pic_address=movie_address['src']  
    # return movie_lists

def main():
    url='https://movie.douban.com/top250'
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59'
    }
    cookies={'bid':'-iv9ZmYXAFM'}
    
    movie_lists=get_movies_info_list(url,headers=headers,cookies=cookies)

if __name__ == "__main__":
    
    main()



