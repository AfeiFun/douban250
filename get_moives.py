import requests
import re
from bs4 import BeautifulSoup


url='https://movie.douban.com/top250'
headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59'
    }
cookies={'bid':'-iv9ZmYXAFM'}

r=requests.request('GET',url,headers=headers,cookies=cookies)
soup=BeautifulSoup(r.text,'html.parser')

movies=soup.find_all('div',class_='item')
movie_title=movies[0].find_next('span',class_='title').string
movie_pic=movies[0].find_next('img').attrs['src']
movie_info=movies[0].p.text
start=movie_info.index(':')
end=movie_info.find('主')
print(movie_info[start+1:end-3])
# print(movie_info.find(':'))
# movie_director=movie_info[4:movie_info.find(' ',4)]

# print(r.status_code,movie_title,movie_pic,movie_director)