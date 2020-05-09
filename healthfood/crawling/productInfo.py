from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from utils import preprocess_materials_info
import time
import pickle

REPORT_NUMS = pickle.load(open("./report_num.pickle", "rb"))
print(REPORT_NUMS)

PATH = "../chromedriver"
SITE_URL = "http://www.foodsafetykorea.go.kr/portal/healthyfoodlife/searchHomeHF.do?menu_grp=MENU_NEW04&menu_no=2823"

BROWSER = webdriver.Chrome(PATH)
BROWSER.get(SITE_URL)
BROWSER.implicitly_wait(2)


def search_product(prod_report_num: int):
    try:
        # click 신고 번호
        BROWSER.find_element_by_xpath('//*[@id="search_code"]/option[3]').click()
        BROWSER.find_element_by_xpath('//*[@id="search_word"]').send_keys(prod_report_num)
        time.sleep(2)
        BROWSER.find_element_by_xpath('//*[@id="wrap"]/main/div[3]/div[1]/div/fieldset/ul/li[3]/a').click()
        time.sleep(2)
        BROWSER.find_element_by_xpath('//*[@id="wrap"]/main/div[3]/table/tbody/tr/td[2]').click()
        return BROWSER
    except WebDriverException as e:
        print(e)
        return None


def get_product_page(prod_report_num: int):
    product_page = None
    try:
        while True:
            product_page = search_product(prod_report_num)

            if product_page is not None:
                break
        return product_page
    except TimeoutError as e:
        print(e)
        return None


def get_product_info(prod_report_num: int):
    product_page = get_product_page(prod_report_num)

    if product_page is None:
        product_page = get_product_info(prod_report_num)

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

    return product_info


def save_in_db(product_info):
    pass


def main():
    for num in REPORT_NUMS:
        product_info = get_product_info(num)
        save_in_db(product_info)
