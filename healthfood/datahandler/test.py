import pandas as pd
import pymysql
import numpy as np

pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)


def insert_in_db(data: list, conn, cursor, sql):
    """ 데이터를 디비에 삽입하는 함수.

    :param data: 삽입할 데이터
    :param conn: 디비 conn
    :param cursor: 디비 cursor
    :param sql: sql 쿼리
    :return: None
    """
    try:
        print("==========SAVE data==============\n")
        print(data)
        data = [None if d is np.nan else d for d in data]
        data = [int(d) if type(d) is np.int64 else d for d in data]
        cursor.execute(sql, tuple([d for d in data]))
        conn.commit()
    except Exception as e:
        print(e)


def connect_db(host, user, password, db, port):
    """ 데이터베이스 연결하는 함수

    """
    conn = pymysql.connect(host=host,
                           user=user,
                           password=password,
                           charset="utf8mb4",
                           db=db,
                           port=port)
    print(conn.get_server_info())
    cursor = conn.cursor()

    return conn, cursor


def main():
    try:
        conn, cursor = connect_db(host="114.71.219.75", user="nathan",
                          password="asd62351", db="health_food_pjt",
                          port=10003)

        product_info = pd.read_csv("../preprocessing/product_info_final_06_23.csv")
        columns = list(product_info.columns)
        cols = "(" + ",".join(columns) + ")"
        values = ("(" + ("%s," * len(columns))[:-1] + ")")
        table_name = "product_total_info"
        print(columns)
        sql = f"insert into {table_name}{cols} values {values}"

        for i in range(len(product_info)):
            data = list(product_info.iloc[i])
            insert_in_db(data, conn, cursor, sql)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()