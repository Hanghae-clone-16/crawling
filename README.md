# crawling

클론코딩 프로젝트를 진행하면서 사이트의 데이터를 크롤링 해와야 하는 과제가 생겼습니다.
먼저, 프로젝트에서는 java를 사용하지만 이번에는 Python - bs4로 데이터를 크롤링하고, mysql db에 넣어줄 생각입니다.

## 맞닥뜨린 문제
크롤러를 만드는 것이 아니였기 때문에 조금 쉽게 데이터를 긁어올 수 있었습니다.
하지만, mysql 세팅에서 잘못된 부분이 있어 에러를 많이 만났네요,

### utf8mb4
긁어온 데이터 안에는 이모티콘이 있었습니다.
이를 utf8로 인코딩 한다면 아래와 같은 멋진 에러가 출력됩니다.
pymysql.err.dataerror: (1366, "incorrect string value: '\\xf0\\x9f\\x91\\xa9\\xf0\\x9f...' for column 'contents' at row 1")

mysql 세팅을 utf8mb4로 바꿔주는 작업이 필요하다고 하여
find 명령어로 my.cnf 파일을 찾았고 아래와 같은 설정을 해주었습니다.

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
이미지 경로를 크롤링 해올 때, html 태그인 <img src> 형태를 긁어온 걸 모르고 있었습니다.
.get("src")를 사용해 src에 해당하는 부분만 긁어오고, None인 경우 그냥 긁어오는 방식을 사용했습니다.

## 결과
내용이 길어 이쁘진 않지만 긁어오기에 성공했네요!
![image](https://user-images.githubusercontent.com/53491653/113515822-b5fdef00-95b1-11eb-8959-4f455d0c43a7.png)



