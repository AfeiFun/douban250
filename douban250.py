import get_moives
import datebase
def main():
    # # 抓取数据
    # movies=get_moives.get_all_page()

    # # 保存到数据库
    # get_moives.save_movies_into_database(movies)

    # # 保存到json文件
    # get_moives.save_movies_into_json(movies)

    # 从数据库中读电影，按照排名
    connection=datebase.connect_movie_database()
    datebase.get_movie_from_database(connection,2)

if __name__ == "__main__":    
    main()



