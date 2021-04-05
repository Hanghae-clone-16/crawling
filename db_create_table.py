import pymysql

## db 접속
db = pymysql.connect(host='{ip}', port=3306, user='', passwd='', db='{database name}')
cursor = db.cursor()

## 테이블 생성
sql = ''' 
CREATE TABLE card (
    id INT NOT NULL PRIMARY KEY ,
    title VARCHAR(200) NOT NULL,
    contents VARCHAR(200) NOT NULL,
    img VARCHAR(200),
    created_At varchar(100) NOT NULL,
    nickname varchar(100) NOT NULL,
    like_cnt varchar(100)
);
'''

## 생성은 execute로 한다.
cursor.execute(sql)

db.commit()
db.close()
