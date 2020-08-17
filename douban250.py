import get_moives


def main():
    # 抓取数据并保存到json文件中
    get_moives.get_all_page()

    # 将json数据导出到数据库中

if __name__ == "__main__":    
    main()



