import get_moives


def main():
    # 抓取数据
    movies=get_moives.get_all_page()

    # 保存到数据库
    get_moives.save_movies_into_database(movies)

    # 保存到json文件
    get_moives.save_movies_into_json(movies)

if __name__ == "__main__":    
    main()



