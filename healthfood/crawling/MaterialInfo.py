from pprint import pprint

from bs4 import BeautifulSoup
from utils import db_config, insert_in_db, apply_multiprocessing
import requests
import pymysql

REGISTER_URL = 'https://www.foodsafetykorea.go.kr/portal/board/boardList.do'
DETAIL_URL = "http://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHFDetail.do"
# config DB
CONN, CURSOR, SQL = db_config()

# Json으로 데이터를 처리하는 request를 처리하는 Parameter
material_param = {
    "menu_no": 2660,
    "menu_grp": "MENU_NEW01",
    "copyUrl": "https://www.foodsafetykorea.go.kr:443/portal/board/board.do?menu_no=2660&menu_grp=MENU_NEW01",
    "bbs_no": "bbs987",
    # "search_word": None,
    "start_idx": 1,
    # "show_cnt": 10
}


def preprocess_data(data: list):
    info_data = [info.split(":")[1].strip() if info in ":" else info for info in data]
    join_str = " ".join([info.split(":")[0].strip() if info in ":" else info for info in data])
    result = [None] * 6
    if len(info_data) != 6:
        if "원료" not in join_str:
            result[1:] = info_data
            return result
        elif "인정번호" not in join_str:
            result[1] = info_data[1]
            result[2:] = info_data[1:]
            return result
        elif "업체" not in join_str:
            result[:2] = info_data[:2]
            result[3:] = info_data[2:]
            print(result)
            return result
        elif "기능성내용" not in join_str:
            result[:3] = info_data[:3]
            result[4:] = info_data[3:]
            return result
        elif "주의사항" not in join_str:
            result[:4] = info_data[:4]
            result[5:] = info_data[4:]
            return result
        elif "일일섭취량" not in join_str:
            result[:5] = info_data
            return result
    return info_data


def save_material_data(start_idx: int) -> list:
    """ 제품 등록 데이터 수집 후 저장.

    :param start_idx: 등록정보 페이지 번호
    :return: 제품 등록정보
    """
    print(f"Start Idx = {start_idx}\n")

    try:
        material_param["start_idx"] = start_idx
        req = requests.post(REGISTER_URL, data=material_param)
        # req.encoding = "utf8"
        print(req.json())
        total_data = []
        for js in req.json()["list"]:
            material_no = js["ntctxt_no"]
            print(material_no)
            material_url = "https://www.foodsafetykorea.go.kr/portal/board/boardDetail.do"
            material_params = {
                "menu_no": 2660,
                "menu_grp": "MENU_NEW01",
                "copyUrl": "https://www.foodsafetykorea.go.kr:443/portal/board/board.do?menu_no=2660&menu_grp=MENU_NEW01",
                "bbs_no": "bbs987",
                "ntctxt_no": material_no,
            }
            material_req = requests.post(material_url, material_params)
            req.encoding = "utf8"
            soup = BeautifulSoup(material_req.text, "html.parser")
            material_info = soup.find("p", {"id": "bdt_pre"}).text
            material_info = material_info.split("○")[1:]
            print(f"Before Preprocess Data = {material_info}\n")

            material_info = preprocess_data(material_info)

            print(f"material_info len = {len(material_info)}")
            pprint(material_info)

            insert_in_db(data=material_info, conn=CONN, cursor=CURSOR, sql=SQL)

        # return total_data
    except pymysql.Error as e:
        print(e)


def main():
    """ 식품안전나라에 등록된 건강기능식품 데이터 가져와 저장하는 main 함수.

    """
    start_indexes = [i for i in range(33, 46)]
    for i in range(33, 46):
        save_material_data(i)
    # result = apply_multiprocessing(save_material_data, start_indexes)
    CONN.close()
    # print(result)


if __name__ == '__main__':
    main()
