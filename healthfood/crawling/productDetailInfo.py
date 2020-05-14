from bs4 import BeautifulSoup
from utils import insert_in_db, db_config, apply_multiprocessing
import requests
import pickle
import pymysql

MATERIALS_URL = "http://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHfPrdlstRawmtrl.do"
DETAIL_URL = "http://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHFDetail.do"

CONN, CURSOR, SQL = db_config()


def get_materials_data(product_report_no: int):
    materials_param = {"prdlst_report_no": product_report_no}
    res_json = requests.post(MATERIALS_URL, data=materials_param).json()
    materials = ""
    print("======Material_Json_Data===========")
    print(res_json)
    if res_json is None:
        return ""

    for js in res_json:
        if "rawmtrl_nm" not in js.keys():
            continue
        material_name = js["rawmtrl_nm"]
        materials += material_name + "|"
    print(materials)
    return materials


def save_product_detail_data(detail_keywords: tuple):
    try:
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
    except pymysql.Error as e:
        print(e)


def main():
    search_data = []
    with open("./search_data.pickle", "rb") as f:
        search_data = pickle.load(f)

    apply_multiprocessing(save_product_detail_data, data=search_data)
    CONN.close()


if __name__ == '__main__':
    main()


