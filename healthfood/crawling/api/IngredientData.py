import json
from pprint import pprint
from urllib import request

import pymysql
import xmltodict

개별_인정 = "http://openapi.foodsafetykorea.go.kr/api/sample/I-0050/xml/1/5"
API_KEY = "1a191c4700ee46cf8e49"


# TODO api 데이터 받아오는 거 마무리 및 인코딩 문제 확인.
def get_function_ingre_data(conn, cursor, sql):
    start_row = 1
    end_row = 512
    url = f"http://openapi.foodsafetykorea.go.kr/api/{API_KEY}/I-0040/xml/{str(start_row)}/{str(end_row)}"
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
            count = 1
            for row_data in output["I-0040"]["row"]:
                print(f"===Count : {count}=====")
                count += 1
                company_address = row_data["ADDR"]  # 주소
                material_name = row_data["APLC_RAWMTRL_NM"]  # 신청원료명
                company_name = row_data["BSSH_NM"]  # 업체명
                daily_dose = row_data["DAY_INTK_CN"]  # 1일 섭취량
                function_content = row_data["FNCLTY_CN"]  # 기능성 내용
                confirm_num = row_data["HF_FNCLTY_MTRAL_RCOGN_NO"]  # 인정번호
                warning_info = row_data["IFTKN_ATNT_MATR_CN"]  # 섭취시 주의사항
                company_type = row_data["INDUTY_NM"]  # 업종
                confirm_date = row_data["PRMS_DT"]
                confirm_num_date = f"{confirm_num}({confirm_date})"
                data = [confirm_num_date, company_name,
                        material_name, function_content, daily_dose, warning_info]
                insert_in_db(data, conn=conn, cursor=cursor, sql=sql)
                pprint(data)
    except pymysql.Error as e:
        print(e)


# TODO api 데이터 받아오는 거 마무리 및 인코딩 문제 확인.
def get_each_ingre_data(conn, cursor, sql):
    start_row = 1
    end_row = 315
    url = f"http://openapi.foodsafetykorea.go.kr/api/{API_KEY}/I-0050/xml/{str(start_row)}/{str(end_row)}"
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
            count = 1
            for row_data in output["I-0050"]["row"]:
                print(f"===Count : {count}=====")
                count += 1
                confirm_num = row_data["HF_FNCLTY_MTRAL_RCOGN_NO"]  # 주소
                daily_high = row_data["DAY_INTK_HIGHLIMIT"]  # 신청원료명
                daily_low = row_data["DAY_INTK_LOWLIMIT"]  # 업체명
                daily_dose = row_data["WT_UNIT"]  # 1일 섭취량
                material_name = row_data["RAWMTRL_NM"]  # 기능성 내용
                warning_info = row_data["IFTKN_ATNT_MATR_CN"]  # 인정번호
                function_content = row_data["PRIMARY_FNCLTY"]  # 섭취시 주의사항
                data = [confirm_num, daily_high, daily_low,
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
    conn, cursor = connect_db("#", "#", "#", db='#', port=10003)
    columns = "(confirm_num_date, company_name, " \
              "material_name, function_content, daily_dose, warning_info)"
    values = ("(" + ("%s," * len(columns.split(",")))[:-1] + ")")
    print(values)
    columns2 = "(confirm_num, daily_high, daily_low, material_name, function_content, daily_dose, warning_info)"
    values2 = ("(" + ("%s," * len(columns2.split(",")))[:-1] + ")")
    table_name = "material_info"
    table_name2 = "each_material_info"
    sql = f"insert ignore into {table_name}{columns} values {values}"
    sql2 = f"insert ignore into {table_name2}{columns2} values {values2}"
    print(sql)
    get_function_ingre_data(conn, cursor, sql)
    # get_each_ingre_data(conn, cursor, sql2)
