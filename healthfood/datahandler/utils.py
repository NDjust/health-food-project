from MysqlHandler import MysqlHandler
import pandas as pd


def save_db_to_csv(sql: str, file_path: str) -> None:
    """ db에 있는 데이터를 csv 파일로 변환.

    :param sql: db sql 쿼리문
    :param file_path: 저장할 파일 위치.
    :return: None
    """
    handler = MysqlHandler(host="localhost",
                                   user="root",
                                   password="",
                                   db="health_food_pjt",
                                   port=None)
    with handler:
        handler.mysql_to_df(sql, save=True, file_path=file_path)



if __name__ == '__main__':
    df = pd.read_csv("./data.csv")
