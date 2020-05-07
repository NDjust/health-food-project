from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, WebDriverException
import pymysql
import re
import time

PATH = "../chromedriver"
SITE_URL = "http://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHF.do?menu_grp=MENU_NEW04&menu_no=2823"


def set_chrome_browser():
    """ Load chrome browser function.
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


BROWSER = set_chrome_browser()
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
    save_all_data("register_info")
