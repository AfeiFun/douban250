import pymysql
import json


def connect_movie_database():
    # 读取配置信息,连接数据库,返回一个connection对象
    with open('config.json') as conf_json:
        config=json.load(conf_json)
    connection=pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        db=config['db'],
        port=config['port']
    )
    return connection

def insert_movie_in_database(movie,connection):
    '''
    movie:一个电影的dict数据
    connection:一个数据库的连接
    '''
    try:
        with connection.cursor() as cursor:
            #.values()传回的不是一个典型的list，而是dict_list
            movie_tuple=tuple(movie.values())

            print('正在写入电影',movie_tuple)

            # 这里所有的占位符都用 %s ，别用 %d ，即使后面的tuple里有int 数据
            sql="INSERT INTO `movie250`.`movies_list` (`rank`, `movie_title`, `movie_pic`, `movie_director`, `movie_stars`, `movie_year`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"%movie_tuple

            cursor.execute(sql)
            connection.commit()
    except pymysql.err.DataError as reason:
        print(movie_tuple,reason)
        # 单个项目出错后，不影响后续的导入
        pass

def get_movie_from_database(connection,rank):
    try:
        with connection.cursor() as cursor:
            sql="select * from `movie250`.`movies_list` where  `rank`=%s"%rank
            cursor.execute(sql)
            movie_list=cursor.fetchone()
            print(movie_list)
            return movie_list
    except pymysql.err.DataError as reason:
        print(movie_list,reason)
        pass


