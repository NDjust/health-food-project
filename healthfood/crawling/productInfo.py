from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils import preprocess_materials_info, connect_db, insert_in_db, set_chrome_browser, db_config
import pymysql
import time
import pickle

REPORT_NUMS = pickle.load(open("./report_num.pickle", "rb"))
print(REPORT_NUMS)

PATH = "/Users/hongnadan/PycharmProjects/DataArchitecture/health-food-project/chromedriver"
SITE_URL = "http://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHF.do?menu_grp=MENU_NEW04&menu_no=2823"


def search_product(prod_report_num: int, browser: webdriver.chrome) -> webdriver.Chrome:
    """ 신고번호로 해당 제품의 상세 정보 검색.

    자바스크립트 이벤트 에러를 방지하기 위해 예외처리.
    :param browser: chrome web browser
    :param prod_report_num: 제품 신고번호
    :return: Chrome Browser or None
    """
    try:

        # click 신고 번호
        browser.implicitly_wait(10)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search_code"]/option[3]'))).click()

        # 신고번호 입
        browser.find_element_by_xpath('//*[@id="search_word"]').send_keys(prod_report_num)

        # 제품 검색
        time.sleep(5)
        wait = WebDriverWait(browser, 10)
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="wrap"]/main/div[3]/div[1]/div/fieldset/ul/li[3]/a'))).click()

        # 제품 클릭
        time.sleep(5)
        wait = WebDriverWait(browser, 10)
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="wrap"]/main/div[3]/table/tbody/tr/td[2]/a'))).click()

        return browser
    except WebDriverException as e:
        print(e)


def get_product_page(prod_report_num: int, browser) -> webdriver.Chrome:
    """ 제품 상세 페이지 로딩.

    검색한 제품의 상세 페이지를 가져옴.
    검색 실패시 다시 검색을 진행할 수 있도록 search_product 함수에서 None 리턴하지 않을때까지 반복.
    추가로 TimeOutError 예외처리.

    :param browser: chrome web browser
    :param prod_report_num: 제품 신고 번호
    :return: Browser or None
    """
    try:
        print("=====get_product_page======")
        product_page = search_product(prod_report_num, browser)
        # while True:
        #     if product_page is not None:
        #         break
        #     product_page = search_product(prod_report_num, browser)

        return product_page
    except TimeoutError as e:
        print(e)


def get_product_info(prod_report_num: int, product_page: webdriver.Chrome) -> list:
    """ 제품의 상세 정보를 가져오는 함수.

    제품 상세 페이지의 데이터를 긁어오고, 페이지 못가져올시 다시 브라우저 실행.

    :param product_page: product page browser
    :param prod_report_num: 제품 신고번호
    :return: 제품 상세정보가 담긴 리스트
    """
    print("=====get_product_info======")
    print(product_page)
    # if product_page is None:
    #     product_page = get_product_page(prod_report_num)

    product_info = []
    for i in range(1, 13):
        text = product_page.find_element_by_xpath(f'//*[@id="wrap"]/main/div[3]/article/table/tbody/tr[{i}]/td').text
        product_info.append(text)

    total_materials = ""
    func_materials_info = product_page.find_element_by_xpath('//*[@id="wrap"]/main/div[3]/article/div[1]/table').text
    etc_materials_info = product_page.find_element_by_xpath('//*[@id="wrap"]/main/div[3]/article/div[2]/table').text
    capsule_materials_info = product_page.find_element_by_xpath('//*[@id="wrap"]/main/div[3]/article/div[3]/table').text
    total_materials += preprocess_materials_info(func_materials_info)
    total_materials += preprocess_materials_info(etc_materials_info)
    total_materials += preprocess_materials_info(capsule_materials_info)
    product_info.append(total_materials)

    return product_info


def save_in_db(conn, cursor, sql: str):
    try:
        for num in REPORT_NUMS:
            BROWSER = webdriver.Chrome(PATH)
            BROWSER.get(SITE_URL)

            page = get_product_page(num, BROWSER)
            product_info = get_product_info(num, page)
            print(product_info)
            insert_in_db(data=product_info, conn=conn, cursor=cursor, sql=sql)
            BROWSER.close()
        conn.close()
    except pymysql.Error as e:
        print(e)
    except Exception as e:
        print(e)


def main():
    print(REPORT_NUMS)
    conn, cursor, sql = db_config()
    save_in_db(conn=conn, cursor=cursor, sql=sql)


if __name__ == '__main__':
    main()
