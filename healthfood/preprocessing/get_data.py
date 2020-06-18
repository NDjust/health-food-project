import pymysql
import pandas as pd

try:
    conn = pymysql.connect(host="114.71.219.75",
                          user = "nathan",
                          password = "asd62351",
                          db="health_food_pjt",
                          port=10003,
                          charset='utf8')
    print(conn.get_server_info() + "\n")
    cursor = conn.cursor()
    cursor.execute("select * from product_info")
    data = cursor.fetchall()
    field_names = [i[0] for i in cursor.description]
    df = pd.DataFrame(data, columns=field_names)
    df.to_csv("./product_info.csv")
except pymysql.DatabaseError as e:
    print(e)