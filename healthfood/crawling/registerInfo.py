from selenium.common.exceptions import WebDriverException
from utils import set_chrome_browser
import pymysql
import time
import pickle

PATH = "/Users/hongnadan/PycharmProjects/DataArchitecture/health-food-project/chromedriver"
SITE_URL = "http://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHF.do?menu_grp=MENU_NEW04&menu_no=2823"

BROWSER = set_chrome_browser(PATH)
BROWSER.get(SITE_URL)


def click_next_button(page_len):
    try:
        time.sleep(2)
        BROWSER.find_element_by_xpath(f'//*[@id="wrap"]/main/div[3]/div[2]/div/ul/li[{page_len}]/a').click()
    except WebDriverException as e:
        print(e)


def get_current_page_data():
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

        for i in range(1, len(page_text_list)+1):
            print("==========Current Page Data==============\n")
            row = [BROWSER.find_element_by_xpath(
                    f'//*[@id="wrap"]/main/div[3]/table/tbody/tr[{i}]/td[{j}]').text for j in range(1, 6)]
            data.append(row)
        print(data)
        return data
    except WebDriverException as e:
        print(e)


def save_all_data(table_name=None):
    try:
        conn = pymysql.connect(host="localhost",
                               user="root",
                               password="",
                               charset="utf8",
                               db="health_food_pjt",
                               port=None)
        print(conn.get_server_info())
        cursor = conn.cursor()

        all_data = []
        while True:
            data = get_current_page_data()
            print("==========Get Current Page data==============\n")
            if data is None:
                continue

            for d in data:
                print("==========SAVE Current Page data==============\n")
                sql = f"insert into {table_name} " \
                      f"(register_num, product_name, company_name, report_num, register_date) " \
                      "values(%s, %s, %s, %s, %s)"
                print(d)
                cursor.execute(sql, (d[0], d[1], d[2], d[3], d[4]))
                conn.commit()

            if data[0][0] == "1":
                break
        conn.close()
    except Exception as e:
        print(e)
    except pymysql.Error as e:
        print(e)
    return all_data


if __name__ == '__main__':
    # get_current_page_data()
    save_all_data("register_info")
