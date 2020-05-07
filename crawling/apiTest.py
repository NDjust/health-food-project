import requests
from bs4 import BeautifulSoup
from selenium import webdriver
url = "http://search.11st.co.kr/Search.tmall?kwd=%25EC%259E%2585%25ED%2581%25B0%2520%25EB%25A6%25BD%25EC%258A%25A4%25ED%258B%25B1&fromACK=recent"
req = requests.get(url)
html = req.text
driver = webdriver.Chrome("../chromedriver")
driver.get(url)

html1 = driver.page_source
soup = BeautifulSoup(html1, "html.parser")
data = soup.find(
    "#contsWrap > div > div.result_related > h3"
)
print(data)