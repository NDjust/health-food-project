from utils import db_config, insert_in_db, apply_multiprocessing
import requests
import pymysql

# TODO 네트워크를 활용해서 POST, GET 으로 자바 스크립트 데이터 처리

REGISTER_URL = 'http://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHFProc.do'
DETAIL_URL = "http://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHFDetail.do"
# config DB
CONN, CURSOR, SQL = db_config()

# Json으로 데이터를 처리하는 request를 처리하는 Parameter
registration_param = {
    "menu_no": 2823,
    "menu_grp": "MENU_NEW04",
    "copyUrl": "http://www.foodsafetykorea.go.kr:80/portal/healthyfoodlife/searchHomeHF.do?menu_grp=MENU_NEW04&menu_no=2823",
    "search_code": "01",
    "search_word": None,
    "start_idx": 1,
    "show_cnt": 10
}


def save_registration_data(start_idx: int) -> list:
    """ 제품 등록 데이터 수집 후 저장.

    :param start_idx: 등록정보 페이지 번호
    :return: 제품 등록정보
    """
    try:
        registration_param["start_idx"] = start_idx
        req = requests.post(REGISTER_URL, data=registration_param)
        req.encoding = "utf-8"

        total_data = []
        for js in req.json():
            register_no = js["no"]
            product_report_search_no = js["prdlst_report_ledg_no"]
            report_num = js["prdlst_report_no"]
            product_name = js["prdlst_nm"]
            company_name = js["bssh_nm"]
            register_date = js["prms_dt"]
            data = [register_no, product_report_search_no, report_num, product_name, company_name, register_date]
            total_data.append(data)
            insert_in_db(data=data, conn=CONN, cursor=CURSOR, sql=SQL)

        return total_data
    except pymysql.Error as e:
        print(e)


def main():
    """ 식품안전나라에 등록된 건강기능식품 데이터 가져와 저장하는 main 함수.

    """
    # 각 페이지의 인덱스 값.
    start_indexes = [i for i in range(1, 2859)]
    result = apply_multiprocessing(save_registration_data, start_indexes)
    CONN.close()
    print(result)


if __name__ == '__main__':
    main()
