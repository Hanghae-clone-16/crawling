import requests
from bs4 import BeautifulSoup

# 브라우저에서 엔터친 것 처럼
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# source
data = requests.get('https://velog.io',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# # 하나만 가져오기
# # print(soup)
# img = soup.select_one('#root > div.sc-iRbamj.blSEcj > div.sc-fjdhpX.rMlhG > div.sc-jlyJG.lpgbkm > main > div > div:nth-child(1) > a > div > img').text
# title = soup.select_one('#root > div.sc-iRbamj.blSEcj > div.sc-fjdhpX.rMlhG > div.sc-jlyJG.lpgbkm > main > div > div:nth-child(1) > div.sc-jhAzac.hvSHGq > a > h4').text
# contents = soup.select_one('#root > div.sc-iRbamj.blSEcj > div.sc-fjdhpX.rMlhG > div.sc-jlyJG.lpgbkm > main > div > div:nth-child(1) > div.sc-jhAzac.hvSHGq > a > div > p').text
# created_At = soup.select_one('#root > div.sc-iRbamj.blSEcj > div.sc-fjdhpX.rMlhG > div.sc-jlyJG.lpgbkm > main > div > div:nth-child(1) > div.sc-jhAzac.hvSHGq > div > span:nth-child(1)').text
# comment_cnt = soup.select_one('#root > div.sc-iRbamj.blSEcj > div.sc-fjdhpX.rMlhG > div.sc-jlyJG.lpgbkm > main > div > div:nth-child(1) > div.sc-jhAzac.hvSHGq > div > span:nth-child(3)').text
# nickname = soup.select_one('#root > div.sc-iRbamj.blSEcj > div.sc-fjdhpX.rMlhG > div.sc-jlyJG.lpgbkm > main > div > div:nth-child(1) > div.sc-fBuWsC.wKjEm > a > span > b').text
# like_cnt = soup.select_one('#root > div.sc-iRbamj.blSEcj > div.sc-fjdhpX.rMlhG > div.sc-jlyJG.lpgbkm > main > div > div:nth-child(1) > div.sc-fBuWsC.wKjEm > div').text
#
# print(img, title, contents, created_At, comment_cnt, nickname, like_cnt)

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
        all_created_At = all_created_At.text.split("년")[0]+all_created_At.text.split("년")[1].split("월")[0]+all_created_At.text.split("월")[1].split("일")[0]
        created_At.append(all_created_At.replace(" ","-"))
    elif all_created_At is None:
        all_created_At = "2021-01-01"
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

print(len(img))
print(img)
print(len(title))
print(title)
print(len(contents))
print(contents)
print(len(created_At))
print(created_At)
print(len(comments_cnt))
print(comments_cnt)
print(len(nickname))
print(nickname)
print(len(like_cnt))
print(like_cnt)
