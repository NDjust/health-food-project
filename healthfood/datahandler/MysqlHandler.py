from pymysql.err import Error

import pymysql
import pandas as pd


class MysqlHandler:

    def __init__(self, host, user, password, port, db) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db = db
        self.session = None

    def __enter__(self) -> object:
        """ Special Method로 with 구문으로 감싸면 자동으로 실행되는 코드.

        생성된 객체를 데이터베이스에 연결해주는 해줌.
        """
        try:
            conn = pymysql.connect(host=self.host, user=self.user,
                                   password=self.password, db=self.db,
                                   port=self.port, charset="utf8")
            print(conn.get_server_info() + "\n")

            print(f"Connected DB = {self.host}")
            self.session = conn

        except Error as e:
            print(f"Error ={e}")

        return self

    def mysql_to_df(self, sql: str, save=False, file_path=None) -> pd.DataFrame:
        """

        :param sql: dataframe으로 만들 sql 쿼리문
        :param save: 저장 여부
        :param file_path: 저장할 파일 경로
        :return: sql 불러온 데이터를 dataframe으로 변환한 결과.
        """
        if self.session is not None:
            conn = self.session

            df = pd.read_sql(sql, conn)
            df = df.dropna()

            if save:
                df.to_csv(file_path, encoding='utf-8-sig', header=True, \
                          doublequote=True, sep=',', index=False)
                print('File, {}, has been created successfully'.format(file_path))

            return df
        else:
            print("DB is Not Connected")

    def get_data(self, sql: str) -> list:
        """ database에 저장된 데이터를 가져오는 코드.

        :param sql: 데이터베이스 sql 쿼리문
        :return: sql문 결과값.
        """
        if self.session is not None:
            conn = self.session

            cursor = conn.cursor()
            cursor.execute(sql)

            record = cursor.fetchall()
            return record

        else:
            print("DB is not Connected")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ __enter__ 함수와 마찬가지로 special method로 with indent 종료시 자동 실행 코드.

        데이터베이스 connect session 종료시킴.
        """
        self.session.close()