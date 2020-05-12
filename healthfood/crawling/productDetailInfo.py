from bs4 import BeautifulSoup
from multiprocessing import Pool
from utils import insert_in_db, db_config
import requests
import os
import pickle

# TODO 네트워크를 활용해서 POST, GET 으로 자바 스크립트 데이터 처리

MATERIALS_URL = "http://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHfPrdlstRawmtrl.do"
DETAIL_URL = "http://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHFDetail.do"

CONN, CURSOR, SQL = db_config()


def apply_multiprocessing(func, data, **kwargs) -> list:
    pool = Pool(processes=os.cpu_count())
    result = pool.map(func, data)
    pool.close()

    return result


def get_materials_data(product_report_no: int):
    materials_param = {"prdlst_report_no": product_report_no}
    res_json = requests.post(MATERIALS_URL, data=materials_param).json()
    materials = ""
    for js in res_json:
        material_name = js["rawmtrl_nm"]
        materials += material_name + "|"
    print(materials)
    return materials


def save_product_detail_data(detail_keywords: tuple):
    search_no, report_no = detail_keywords
    product_detail_param = {
        "prdlstReportLedgNo": search_no,
        "menu_grp": "MENU_NEW01",
        "menu_no": 2823,
        "search_code": "01",
        "start_idx": "1",
    }
    req = requests.post(DETAIL_URL, product_detail_param)
    soup = BeautifulSoup(req.text, "html.parser")
    product_info = soup.find_all("td")

    info = []
    for d in product_info[:12]:
        info.append(d.text)

    # add materials
    info.append(get_materials_data(report_no))
    insert_in_db(data=info, conn=CONN, cursor=CURSOR, sql=SQL)

    return info


def main():
    search_data = []
    with open("./search_data.pickle", "rb") as f:
        search_data = pickle.load(f)

    apply_multiprocessing(save_product_detail_data, data=search_data)


if __name__ == '__main__':
    main()

# get_product_detail_data(detail_url, params2)
# get_registration_data(register_url, params)



