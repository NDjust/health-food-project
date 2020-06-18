import json
from pprint import pprint
from urllib import request

import pymysql
import xmltodict


# TODO api 데이터 받아오는 거 마무리 및 인코딩 문제 확인.
def get_api_data(conn, cursor, sql):
    api_key = "#"
    start_row = 1
    end_row = 512
    url = f"http://openapi.foodsafetykorea.go.kr/api/{api_key}/I-0040/xml/{str(start_row)}/{str(end_row)}"
    req = request.Request(url)
    res = request.urlopen(url)
    res_code = res.getcode()

    try:
        if res_code == 200:
            res_data = res.read()
            rd = xmltodict.parse(res_data)

            rdj = json.dumps(rd)
            output = json.loads(rdj)
            print("===output===")
            print(output)
            for row_data in output["I-0040"]["row"]:
                company_address = row_data["ADDR"]  # 주소
                material_name = row_data["APLC_RAWMTRL_NM"]  # 신청원료명
                company_name = row_data["BSSH_NM"]  # 업체명
                daily_dose = row_data["DAY_INTK_CN"]  # 1일 섭취량
                function_content = row_data["FNCLTY_CN"]  # 기능성 내용
                confirm_num = row_data["HF_FNCLTY_MTRAL_RCOGN_NO"]  # 인정번호
                warning_info = row_data["IFTKN_ATNT_MATR_CN"]  # 섭취시 주의사항
                company_type = row_data["INDUTY_NM"]  # 업종
                confirm_date = row_data["PRMS_DT"]
                data = [confirm_num, confirm_date, company_name, company_type, company_address,
                        material_name, function_content, daily_dose, warning_info]
                insert_in_db(data, conn=conn, cursor=cursor, sql=sql)
                pprint(data)
    except pymysql.Error as e:
        print(e)


def insert_in_db(data: list, conn, cursor, sql):
    """ 데이터를 디비에 삽입하는 함수.

    :param data: 삽입할 데이터
    :param conn: 디비 conn
    :param cursor: 디비 cursor
    :param sql: sql 쿼리
    :return: None
    """
    print("==========SAVE data==============\n")
    print(data)
    cursor.execute(sql, tuple([d for d in data]))
    conn.commit()

    # values = ("(" + ("%s," * len(cols))[:-1] + ")")
    # columns = "(" + ",".join(cols) + ")"


def connect_db(host, user, password, db, port):
    """ 데이터베이스 연결하는 함수

    """
    conn = pymysql.connect(host=host,
                           user=user,
                           password=password,
                           charset="utf8",
                           db=db,
                           port=port)
    print(conn.get_server_info())
    cursor = conn.cursor()

    return conn, cursor


if __name__ == '__main__':
    conn, cursor = connect_db("114.71.219.75", "nathan", "asd62351", db='health_food_pjt', port=10003)
    columns = "(confirm_num, confirm_date,company_name, company_type, company_address, " \
              "material_name, function_content, daily_dose, warning_info)"
    values = ("(" + ("%s," * len(columns.split(",")))[:-1] + ")")
    print(values)
    table_name = "material_info"
    sql = f"insert into {table_name}{columns} values {values}"
    print(sql)
    get_api_data(conn, cursor, sql)
