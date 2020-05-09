from MysqlHandler import MysqlHandler
import pandas as pd


def save_db_data(sql):
    handler = MysqlHandler(host="localhost",
                                   user="root",
                                   password="",
                                   db="health_food_pjt",
                                   port=None)
    with handler:
        handler.mysql_to_df("select * from register_info", save=True, file_path="./data.csv")


if __name__ == '__main__':
    df = pd.read_csv("./data.csv")
