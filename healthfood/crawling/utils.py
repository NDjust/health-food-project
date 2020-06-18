from selenium import webdriver
from multiprocessing import Pool
import pymysql
import os


def apply_multiprocessing(func, data: list, **kwargs) -> list:
    """ 파라미터로 입력받은 함수와 데이터를 병렬처리하는 함수

    :param func: 병렬처리할 함수
    :param data: 병렬처리할 데이터
    :return: 병렬처리 결과 값
    """
    pool = Pool(processes=os.cpu_count())
    result = pool.map(func, data)
    pool.close()

    return result


def preprocess_materials_info(info: str) -> str:
    """ 긁어온 원재료 정보 데이터에 대한 전처리 함수.

    :param info: 원래료 정보.
    :return: 전처리된 워재료 정보 "|"으로 구분되서 문자열 생성함.
    """
    split_materials = info.split("\n")
    materials = ""
    for i in range(1, len(split_materials)):
        materials += " ".join(split_materials[i].split(" ")[1:]) + "|"

    return materials


def set_chrome_browser(PATH):
    """ chrome 브라우저 최적화 시켜서 세팅해주는 함수.
    본 함수로 불러온 브라우저로 실행시 속도가 올라감.

    :return: Chrome browser Object.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument('headless')  # headless 모드 설정
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    # 속도 향상을 위한 옵션 해제
    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2,
                                                        'geolocation': 2, 'notifications': 2,
                                                        'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2,
                                                        'mixed_script': 2, 'media_stream': 2, 'media_stream_mic': 2,
                                                        'media_stream_camera': 2, 'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                                                        'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}
    options.add_experimental_option('prefs', prefs)

    browser = webdriver.Chrome(PATH, options=options)

    return browser


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


def db_config():
    """ config.json 파일에 저장된 DB 설정값을 불러와 처리.

    :return: 설정된 데이터 베이스 연결된 pysql connector와 Cursor 그리고 insert sql 쿼리문.
    """
    import json
    with open("config.json") as js:
        json_data = json.load(js)
        host = json_data["host"]
        user = json_data["user"]
        password = json_data["password"]
        db = json_data["db"]
        port = json_data["port"]
        cols = json_data["columns"][1:-1].split(",")
        table_name = json_data["table_name"]
        conn, cursor = connect_db(host=host, user=user, password=password, db=db, port=port)
        # cols = ['company_name', 'product_name', 'report_num', 'register_date',
        #         'expiry_date', 'properties', 'daily_dose', 'package_type',
        #         'storage_caution', 'warning_info', 'function_content',
        #         'standard_info', 'materials_info']
        values = ("(" + ("%s," * len(cols))[:-1] + ")")
        columns = "(" + ",".join(cols) + ")"
        print(columns)
        sql = f"insert ignore into {table_name}{columns} values {values}"
        print(sql)
        return conn, cursor, sql
