from pprint import pprint

import pandas
import requests
from bs4 import BeautifulSoup
import urllib.request


def download_image():
    for i in range(1, 34):
        if i < 10:
            urllib.request.urlretrieve(f"https://www.foodsafetykorea.go.kr/img/healthyfoodlife/im0{i}.png",
                                       f"./image/{i}.png")
        else:
            urllib.request.urlretrieve(f"https://www.foodsafetykorea.go.kr/img/healthyfoodlife/im{i}.png",
                                       f"./image/{i}.png")


def get_function_ingredients():
        try:
            data = []
            for i in range(1, 34):
                URL = ""
                if i < 10:
                    URL = f"https://www.foodsafetykorea.go.kr/portal/healthyfoodlife/functionalityView0{i}.do?menu_grp=MENU_NEW01&menu_no=2657"
                else:
                    URL = f"https://www.foodsafetykorea.go.kr/portal/healthyfoodlife/functionalityView{i}.do?menu_grp=MENU_NEW01&menu_no=2657"
                print(URL)
                req = requests.get(URL)
                soup = BeautifulSoup(req.text, "html.parser")
                ingredients_tag = soup.find_all("ul", {"class": "health"})
                function_data = []
                for ingre in ingredients_tag:
                    function_data += ingre.text.split("\n")[1:-1]

                join = "|".join(function_data)
                data.append([i, join])
                pprint(data)
            df = pandas.DataFrame(data, columns=["category", "ingredients"])
            df.to_csv("./category_function_data.csv")
            return data
        except AttributeError as e:
            print(e)


if __name__ == '__main__':
    # urllib.request.urlretrieve("https://www.foodsafetykorea.go.kr/img/healthyfoodlife/im33_2019.png", './image/33.png')
    # download_image()
    ingredients = get_function_ingredients()
    print(ingredients)
