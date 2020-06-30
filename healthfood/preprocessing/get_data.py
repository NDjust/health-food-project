import pymysql
import pandas as pd
from sqlalchemy import create_engine

import pymysql

pymysql.install_as_MySQLdb()


def db_to_csv(table_name: str, file_name: str) -> None:
    try:
        conn = pymysql.connect(host="#",
                               user="#",
                               password="#",
                               db="#",
                               port=0,
                               charset='utf8')
        print(conn.get_server_info() + "\n")
        cursor = conn.cursor()
        cursor.execute(f"select * from {table_name}")
        data = cursor.fetchall()
        field_names = [i[0] for i in cursor.description]
        df = pd.DataFrame(data, columns=field_names)
        df.to_csv(f"./{file_name}.csv")

    except pymysql.DatabaseError as e:
        print(e)


def csv_to_db(df: pd.DataFrame) -> None:
    engine = create_engine("mysql+mysqldb://#:" + "#" + "#", encoding='utf-8')
    conn = engine.connect()

    # if_exists = "append": 기존 데이터에 추가로 넣음.
    df.to_sql(name='functional_product', con=engine, index=False, if_exists="append")


if __name__ == '__main__':
    info = "product_info"
    db_to_csv(info, info)
    # info = "each_material_info"
    # db_to_csv(info, info)
    # df = pd.read_csv("./category_function_data.csv")
    # csv_to_db(df)

