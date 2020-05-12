from selenium.common.exceptions import WebDriverException
from utils import set_chrome_browser, insert_in_db, connect_db, db_config
import pymysql
import time


PATH = "/Users/hongnadan/PycharmProjects/DataArchitecture/health-food-project/chromedriver"
SITE_URL = "http://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHF.do?menu_grp=MENU_NEW04&menu_no=2823"

BROWSER = set_chrome_browser(PATH)
BROWSER.get(SITE_URL)


def click_next_button(page_len: int) -> None:
    """ 건강기능식품 등록 다음 페이로 넘어가는 함수.
    본 사이트의 페이지네이션은 모두 자바스크립트로 동작하기 때문에 url 로직이 변하지 않아서
    직접 해당 이벤트 클릭으로 페이지를 넘어가야함.

    추가로 해당 페이지 바 길이에 따라 동적으로 변하기 때문에 그에 맞춰서 인자값을 받아서 처리.

    :param page_len: 해당 페이지의 페이지 바 길이.
    """
    try:
        time.sleep(2)
        BROWSER.find_element_by_xpath(f'//*[@id="wrap"]/main/div[3]/div[2]/div/ul/li[{page_len}]/a').click()
    except WebDriverException as e:
        print(e)


def get_current_page_data():
    """건강기능식품 등록 페이지의 데이터를 가져옴.
    만약 데이터를 못 긁어오면 None 리턴.
    셀레니움으로 진행되기 때문에 웹 브라우저 반응 속도에 따라 Exception 이 터져서 try-except 으로 예외처리.

    :return: page_data or None
    """
    try:
        data = []
        time.sleep(2)
        page_length = len(BROWSER.find_element_by_xpath('//*[@id="wrap"]/main/div[3]/div[2]/div/ul').text.split('\n'))
        click_next_button(page_length)
        text = BROWSER.find_element_by_xpath('//*[@id="wrap"]/main/div[3]/table/tbody').text
        page_text_list = text.split("\n")
        print("==========Current Page Test List==============\n")
        if page_text_list is None:
            return None

        for i in range(1, len(page_text_list) + 1):
            print("==========Current Page Data==============\n")
            row = [BROWSER.find_element_by_xpath(
                f'//*[@id="wrap"]/main/div[3]/table/tbody/tr[{i}]/td[{j}]').text for j in range(1, 6)]
            data.append(row)
        print(data)
        return data
    except WebDriverException as e:
        print(e)


def save_all_data(sql: str, conn, cursor) -> list:
    """ 자바스크립트 이벤트로 페이지네이션 한 후 모든 데이터를 디비에 저장.

    :param cursor: db 커서
    :param conn: db 연결 세션
    :param sql: sql 쿼리문
    :return: all_data or None
    """
    try:
        all_data = []

        while True:
            page_data = get_current_page_data()
            print("==========Get Current Page data==============\n")
            if page_data is None:
                continue
            all_data.append(page_data)
            for data in page_data:
                insert_in_db(data=data, conn=conn, cursor=cursor, sql=sql)

            if page_data[0][0] == "1":
                break
        conn.close()

        return all_data
    except Exception as e:
        print(e)
    except pymysql.Error as e:
        print(e)


def main():
    conn, cursor, sql = db_config()
    save_all_data(sql, conn, cursor)


if __name__ == '__main__':
    main()
