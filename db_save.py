import requests
from bs4 import BeautifulSoup


# db 접속
import pymysql
db = pymysql.connect(host='{ip}', port=3306, user='', passwd='', db='{database name}')
db.set_charset('utf8mb4')
cursor = db.cursor()

## 크롤링
# 브라우저에서 엔터친 것 처럼
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# source
data = requests.get('https://velog.io',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
cards = soup.select('#root > div.sc-iRbamj.blSEcj > div.sc-fjdhpX.rMlhG > div.sc-jlyJG.lpgbkm > main > div > div')

#
img=[]
title=[]
contents=[]
created_At=[]
comments_cnt=[]
nickname=[]
like_cnt=[]

for card in cards:
    all_img = card.select_one('a > div > img')
    if all_img is not None:
        all_img = all_img.get("src")
        img.append(all_img)
    img.append(all_img)

    all_title = card.select_one('div.sc-jhAzac.hvSHGq > a > h4')
    if all_title is not None:
        all_title = all_title.text
        title.append(all_title)
    elif all_title is None:
        all_title = ""
        title.append(all_title)

    all_contents = card.select_one('div.sc-jhAzac.hvSHGq > a > div > p')
    if all_contents is not None:
        all_contents = all_contents.text
        contents.append(all_contents)
    elif all_contents is None:
        all_contents = ""
        contents.append(all_contents)

    all_created_At = card.select_one('div.sc-jhAzac.hvSHGq > div > span:nth-child(1)')
    if all_created_At is not None:
        all_created_At = all_created_At.text
        created_At.append(all_created_At)
    elif all_created_At is None:
        all_created_At = ""
        created_At.append(all_created_At)

    all_comments_cnt = card.select_one('div.sc-jhAzac.hvSHGq > div > span:nth-child(3)')
    if all_comments_cnt is not None:
        all_comments_cnt = all_comments_cnt.text
        comments_cnt.append(all_comments_cnt)
    elif all_comments_cnt is None:
        all_comments_cnt = ""
        comments_cnt.append(all_comments_cnt)

    all_nickname = card.select_one('div.sc-fBuWsC.wKjEm > a > span > b')
    if all_nickname is not None:
        all_nickname = all_nickname.text
        nickname.append(all_nickname)

    all_like_cnt = card.select_one('div.sc-fBuWsC.wKjEm > div')
    if all_like_cnt is not None:
        all_like_cnt = all_like_cnt.text
        like_cnt.append(all_like_cnt)

items = [item for item in zip(title,contents,img,created_At,comments_cnt,nickname,like_cnt)]
# items = [item for item in zip(title,contents,created_At,comments_cnt,nickname,like_cnt)]

# 실행할 때마다 다른값이 나오지 않게 테이블 제거
cursor.execute("drop table if exists board")

## 테이블 생성
sql = '''
CREATE TABLE board (
    id INT NOT NULL PRIMARY KEY ,
    title VARCHAR(200) NOT NULL,
    contents VARCHAR(200) NOT NULL,
    img VARCHAR(200),
    createdAt VARCHAR(200) NOT NULL,
    comments_cnt varchar(100) NOT NULL,
    nickname varchar(100) NOT NULL,
    like_cnt varchar(100)
    )
    ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
;
'''
# ## 테이블 생성
# sql = '''
# CREATE TABLE card (
#     id INT NOT NULL PRIMARY KEY ,
#     title VARCHAR(200) NOT NULL,
#     contents VARCHAR(200) NOT NULL,
#     created_At varchar(100) NOT NULL,
#     comments_cnt varchar(100) NOT NULL,
#     nickname varchar(100) NOT NULL,
#     like_cnt varchar(100)
#     )
#     ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
# ;
# '''

## 생성은 execute로 한다.
cursor.execute(sql)

i = 1
# 데이터 저장하기
for item in items:
    cursor.execute(
        f"INSERT INTO board VALUES({i}, \"{item[0]}\",\"{item[1]}\",\"{item[2]}\",\"{item[3]}\",\"{item[4]}\",\"{item[5]}\", \"{item[6]}\")")
    i += 1


# 커밋
db.commit()
# 종료
db.close()
