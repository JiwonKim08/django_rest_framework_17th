# CEOS 17기 백엔드 스터디

### 서비스 설명
에브리타임 클론 코딩으로, 앱은 크게 accout, board, timetable로 나누었다.

구현 모델:
- common: CommonInfo
- account: Shcool, User, Friend
- board: Board, Fixed_board, Post, Photo, Scrap, Comment, Message_room, Message
- timetable: Lecture, My_lecture, Lecture_enrollment, Review


### ERD
![ERD1](https://user-images.githubusercontent.com/99666136/229291041-66ce740c-63b7-4070-8ded-20b06452dbef.png)

부가 설명:
- User table에서 role 속성을 뺐다. 장고에서 지원하는 '커스텀 유저 모델'에서 이미 일반회원과 관리자를 구분해주기 때문이다.
- User table과 Post table이 n:n 관계라고 생각해 scrap table을 중간에 두고 1:n, 1:n으로 이었다.
- School table을 따로 작성했다. Lecture의 경우 학교마다 데이터가 다르기때문에 외래키로 참조해야했기 때문이다.
- Message_room table에서는 DM목록을 제공하고, Message는 DM을 제공한다.
- Friend table에서 follower과 followee 모두 user table을 참조한다.
- comment table(댓글 테이블)에서 parent_id를 두어 자기 참조 관계로 구현하면 대댓글 테이블을 만들지 않아도 된다.


### 겪은 오류와 해결 과정
- INSTALLED_APPS에 app 이름을 작성하지 않아 모듈이 없다는 에러를 만났고 해결했다.
- migrate가 안되길래 mySQL에서 테이블 삭제하고 migrations 파일도 다지우고 다시 makemigrations 해서 해결했다.
- CommonInfo에서 이미 models.Model을 상속받고 있는데, 모든 테이블마다 models.Model과 CommonInfo를 같이 상속받아 다중상속 에러가 발생했고 해결했다.
- Board table이 School table을 외래키로 참조하는데, School에 데이터를 넣지 않고 Board에 데이터를 넣어 오류가 났고 해결했다.


### 새롭게 배운 점
1. 앱을 큰 기능별로 분리(account, board, timetable)
2. ForeignKey와 related_name 필드의 사용: orm을 쉽게 사용하기 위해서 related_name을 사용한다.
3. 기본속성은 상속모델을 따로 생성: 
- 수정일자: auto_now=True 사용, auto_now=True 는 django model 이 save 될 때마다 현재날짜(date.today()) 로 갱신된다.
- 생성일자: auto_now_add=True 사용, auto_now_add=True 는 django model 이 최초 저장(insert) 시에만 현재날짜(date.today()) 를 적용한다.
- 삭제 함수 구현: def delete(self, using=None, keep_parents=False) : models.Model이 가지고 있는 delete 기능을 재정의했다.
4. class Meta를 통한 테이블에 대한 기본 속성 변경: CommonInfo에 abstract = True를 두어 상속 허용 및 테이블 이름 재설정
5. AbstractBaseUser를 통해 커스텀 유저 모델 생성: 비밀번호 해시함수 제공 및 현업에서의 사용때문에 AbstractBaseUser를 쓰는 것이 좋다.
6. 에브리타임은 user와 post관계가 1:n이다. '작성'이라는 관계로 묶여있기 때문이다.
7. 속성으로 배열을 넣으면 안된다. 정렬에 문제가 생겨 정보가 누락될 수 있기 때문이다. ex. where문, order by문, join문 => 테이블 분리 by 제1 정규화 법칙
8. n:m 관계는 연결 테이블을 만들어 1:n, 1:n으로 이어 해결한다.(단, 연결테이블을 만들 때는 중복될 수 있는 값을 고려해 기본키를 잘 설정해야한다. + 장고는 n:m 관계 필드를 사용하면 알아서 연결테이블을 만들어준다.) ex. user table - write table - post table
9. 정규화를 통해 잘 쪼개진 테이블은 읽기 기능을 희생시켜 쓰기 기능을 올린 것이다. join연산은 비싸기 때문이다. 그렇다고 정규화가 성능을 떨어뜨린다는 것은 아니다. 따라서, 인덱싱이나 캐시 기법을 쓰고도 데이터베이스의 느림이 인지된다면, 역정규화(테이블 수정)을 거친다.


### 데이터 삽입, 조회, filter()

    python manage.py shell

    from account.models import School
    from board.models import Board

    #데이터 생성
    School1 = School(name='이화여자대학교') 
    School2 = School(name='연세대학교')  
    School1.save()  
    School2.save() 

    Board1 = Board(school_id_id=1,name='자유게시판', category='자유', bookmark='yes')
    Board2 = Board(school_id_id=2,name='비밀게시판', category='기본', bookmark='yes') 
    Board3 = Board(school_id_id=1,name='컴공게시판', category='학과', bookmark='no')  
    Board1.save() 
    Board2.save()  
    Board3.save() 

    #데이터 조회
    Board.objects.all()               
    <QuerySet [<Board: school_id: 이화여자대학교, boardname: 컴공게시판>, <Board: school_id: 연세대학교, boardname: 비밀게시판>, 
    <Board: school_id: 이화여자대학교, boardname: 자유게시판>, <Board: school_id: 이화여자대학교, boardname: 벼룩게시판>]>

    #filter() 사용
    Board.objects.filter(school_id_id=1)  
    <QuerySet [<Board: school_id: 이화여자대학교, boardname: 컴공게시판>, <Board: school_id: 이화여자대학교, boardname: 자유게시판>]>

![school](https://user-images.githubusercontent.com/99666136/229292698-eb899073-bdfe-4569-9518-1437452f29a4.png)
![board](https://user-images.githubusercontent.com/99666136/229292702-be0386be-1a5b-478d-a802-36b3d14a2725.png)


### 궁금한 점
궁금한 점: 이미 튜플(값)을 넣은 후에 속성을 수정한 후, 다시 migrate해도 되는지?
(하다보니 논리적으로 안 맞는 부분이 보이는데 수정하기가 두렵습니다..)


### 회고
백엔드 개발에서 가장 중요한 부분이 ERD를 잘 짜는 것이라고 생각한다. 시간을 많이 들인 만큼, 완벽할 줄 알았으나 
계속해서 '관계(1:1, 1:n, n:m)및 제약조건'에 대해 수정해야만 했다. 또한 mySQL의 Select, Join을 공부하는 계기가 되어 좋았다.
쿼리문법이 어렵다면, [mySQL 정리](https://jwkdevelop.tistory.com/9)를 참고해보길 바란다. 모델링해보는 게 처음이라, 과제를 제출한 뒤 따로 모델링 수업을 들어봤다.
아니나 다를까.. 관계 설정도 잘못했고 속성도 빼먹고 제약조건도 잘못 걸어뒀다.. 수정하려면 하루는 걸릴 것 같다^__^ 
강의를 들은 후 [modeling 정리](https://jwkdevelop.tistory.com/65)에 정리해두었으니, 어렵다면 참고해보길 바란다.