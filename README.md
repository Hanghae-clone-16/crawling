# crawling

클론코딩 프로젝트를 진행하면서 사이트의 데이터를 크롤링 해와야 하는 과제가 생겼습니다.
먼저, 프로젝트에서는 java를 사용하지만 이번에는 Python - bs4로 데이터를 크롤링하고, mysql db에 넣어줄 생각입니다.

## import

크롤링을 위한 beautifulsoup4와 requests / python에서 mysql을 사용하기 위한 pymysql을 import 해줍니다.

## version

* python - 3.8
* mysql - 8.0.23
* pyMysql - 1.0.2
* bs4 - 0.0.1(Beautifulsoup4 - 4.9.3)
* Requests - 2.25.1

## 사전 작업

mysql을 설치하고, 기본 설정을 해줍니다. (mysql_secure_installation)

이번 프로젝트에 사용할 database를 만들고, 크롤링을 해왔습니다.

## 맞닥뜨린 문제
크롤러를 만드는 것이 아니였기 때문에 조금 쉽게 데이터를 긁어올 수 있었습니다.
하지만, mysql 세팅에서 잘못된 부분이 있어 에러를 많이 만났네요

### utf8mb4
긁어온 데이터 안에는 이모티콘이 있었습니다.
이를 utf8로 인코딩 한다면 아래와 같은 멋진 에러가 출력됩니다.
pymysql.err.dataerror: (1366, "incorrect string value: '\\xf0\\x9f\\x91\\xa9\\xf0\\x9f...' for column 'contents' at row 1")

mysql 세팅을 utf8mb4로 바꿔주는 작업이 필요하다고 하여
find 명령어로 my.cnf 파일을 찾았고 아래와 같은 설정을 해주었습니다.(Windows는 my.ini 파일을 찾아야 한다고 합니다.)

```bash
# Default Homebrew MySQL server config
[mysqld]
# Only allow connections from localhost
bind-address = 127.0.0.1
collation-server = utf8mb4_unicode_ci
#init-connect='SET NAMES utf8mb4'
character-set-server = utf8mb4


[client]
default-character-set=utf8mb4

[mysql]
default-character-set=utf8mb4

[mysqldump]
default-character-set=utf8mb4
```
그리고 python code 안에서, 테이블을 만드는 쿼리를 짤 때도 아래와 같은 세팅을 명시해 주었습니다.

```python
CREATE TABLE card (
    id INT NOT NULL PRIMARY KEY ,
    title VARCHAR(200) NOT NULL,
    contents VARCHAR(200) NOT NULL,
    created_At varchar(100) NOT NULL,
    comments_cnt varchar(100) NOT NULL,
    nickname varchar(100) NOT NULL,
    like_cnt varchar(100)
    )
    ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

이로서 이모티콘 관련 이슈는 해결되었네요

### img 경로 이슈
이미지 경로를 크롤링 해올 때, html 태그인 ``` <img src>``` 형태를 긁어온 걸 모르고 있었습니다.
.get("src")를 사용해 src에 해당하는 부분만 긁어오고, None인 경우 그냥 긁어오는 방식을 사용했습니다.

### createdAt 이슈
이번 크롤링의 목적은 테스트 데이터의 양질화를 위한 것이었기 때문에 쿼리에서 VARCHAR로 문자열로 받아온 것을 알고 있었음에도 넘어가려 했으나
본 코드에서 생성일자는 timestamped 클래스를 상속하여 자동으로 갖고 오게 되는데, 올바르지 않은 값이 들어가게 되면 PUSH, PUT을 할 수 없었습니다.

ex) 2021년 3월 10일

위의 형식을 '2021-3-10'의 형식으로 바꿔줄 필요가 있다고 판단하여 split()과 replace()를 적절히 이용해 해결했고,
```python
        all_created_At = all_created_At.text.split("년")[0]+all_created_At.text.split("년")[1].split("월")[0]+all_created_At.text.split("월")[1].split("일")[0]
        created_At.append(all_created_At.replace(" ", "-"))
```
create문에서는 해당 created_at column의 자료형을 VARCHAR가 아닌 date로 선언해주었습니다

### ' 과 "
날짜가 바뀌어 게시물이 바뀌었는데, 내용에 작은따옴표가 들어가는 게시물이 생겼습니다.
긁어온 내용을 item에 담고, zip()을 이용하여 처리해주고,
Insert 문에서는 \"{item[0]}\"의 형식으로 사용했었으나
```python
items = [item for item in zip(title,contents,img,created_At,comments_cnt,nickname,like_cnt)]
```
작은따옴표를 코드에서 인식하여 어제까진 볼 수 없었던 에러가 나왔습니다.
내용을 긁어오는 부분에서 replace()를 사용하여 처리해주었습니다.
```python
 contents.append(all_contents.replace("\"","\'"))
```

## 결과
db에는 이런식으로 들어가게 됩니다
![image](https://user-images.githubusercontent.com/53491653/113588073-a8f10680-966a-11eb-9693-e5e25886c69d.png)
