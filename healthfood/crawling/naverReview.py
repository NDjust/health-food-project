from bs4 import BeautifulSoup
import requests
import pymysql

URL = 'https://search.shopping.naver.com/detail/detail.nhn?nvMid=13016571849&query=%EC%9C%A0%EC%82%B0%EA%B7%A0&NaPm=ct%3Dkbzzsmls%7Cci%3D9c1ec43d3c277fa8c66fd0458cb37d750cf4e464%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3Dd9060854c9e485db62280a568e0d04b9816a4ee5'

req = requests.get(URL)
soup = BeautifulSoup(req.text, "html.parser")
print(soup.text)
