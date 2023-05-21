# CEOS 17기 백엔드 스터디

### 서비스 설명
에브리타임 클론 코딩으로, 앱은 크게 accout, board, timetable로 나누었다.!

구현 모델:
- common: CommonInfo
- account: Shcool, User, Friend
- board: Board, Fixed_board, Post, Photo, Scrap, Comment, Message_room, Message
- timetable: Lecture, My_lecture, Lecture_enrollment, Review


# ERD
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


# 데이터 삽입, 조회, filter()
    
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

### URL: board/6
### Method:post
### Body: {"name": 사진게시판, "category": 취미, "school_id": 서강대학교}
    [
       {
        "id": 7,
        "created_at": "2023-04-04T23:25:47.053128+09:00",
        "updated_at": "2023-04-04T23:25:47.053128+09:00",
        "deleted_at": null,
        "name": "사진게시판",
        "category": "취미",
        "school_id": 7
       }
    ]
 
# filter
![filter](https://user-images.githubusercontent.com/99666136/230626896-a6528897-2fe1-430f-9904-c3274a789a0c.png)

### 회고
filter 기능을 이해하는데 시간이 오래걸렸던 것 같다. 구현하면서, 프로젝트 데이터 검색 기능에 활용해야겠다는 생각을 했다.
router를 활용해 mapping하고자 하는 view를 등록해주어 쉽게 관리할 수 있었다. 전체적으로 재밌게 구현한 것 같다.👍


# JWT token
- 전체적인 흐름
![image](https://user-images.githubusercontent.com/99666136/236412232-e004efa7-ccfb-4fcd-9ece-414e12602950.png)

1. LoginSerializer에서 access token 과 refresh token을 발급해준 후, LoginView에서는 이미 발급된 토큰을 가져오기만 하는 방식으로 코드를 짰다.
2. 이때 토큰 발행은, rest_framework_simplejwt.tokens 라이브러리를 사용해 .for_user로 토큰을 발행해준다.
3. serializer에서 발행해둔 토큰을 가져와 response의 cookie에 담아 프론트로 보내준다.
4. 쿠키는 다른 데이터와 함께 브라우저에 저장되기 때문에 보안 취약점이 될 수 있다.
5. 따라서 JWT 토큰을 쿠키에 저장할 때에는 보안 강화를 위해, http-only, secure, 토큰 유효시간을 설정해준다.
6. 프론트가 헤더에 access token을 넣어 api를 request에 담아 전송한다.
7. 백엔드에서 request에서 access token을 꺼내 일치하는 user_id를 찾는다.(decode)
8. user_id에 해당하는 내용을 데이터베이스에서 가져온 후, response에 담아 프론트로 전송한다.
9. access token이 없다면, 프론트에서 access token 재발급을 위한 refresh token을 헤더에 담아 백엔드로 전송한다.
10. refresh token에서 찾은 user_id를 기반으로 새로운 access token 발행 후 프론트로 전송한다.
11. refresh token이 없다면, 로그인 페이지로 리다이렉트 시킨다.

- (위 흐름은 코드내 주석처리를 따라가시면 편하게 이해하실 수 있습니다.)



### 회원가입
![image](https://user-images.githubusercontent.com/99666136/236413895-34410842-6c3d-48ae-8db2-5e8964f9995e.png)



### 로그인
![image](https://user-images.githubusercontent.com/99666136/236418543-c6ec656a-a1de-458c-8e55-fa9fa0605a33.png)



### api요청(토큰을 통한 회원정보 반환)
![image](https://user-images.githubusercontent.com/99666136/236414374-a27b9f67-056e-4017-a4b6-27cf7fd48f6a.png)


프론트는 아래와 같은 코드로 get요청을 보낸다.
```
axios.get('/api/user', {
  headers: {
    'Authorization': `Bearer ${cookie}`
  }
})
```

### 겪은 오류와 해결과정
1. 
```
class AuthView(APIView):
    def get(self, request):
        #access token을 프론트가 보낸 request에서 추출
        print(request)
        access_token = request.META['HTTP_AUTHORIZATION'].split()[1]
        print(access_token)
        #access token이 없다면 에러 발생
        if not access_token:
            return Response({"message": "access token 없음"}, status=status.HTTP_401_UNAUTHORIZED)

        #access token이 있다면
        #토큰 디코딩(유저 식별)
        try:
            #payload에서 user_id(고유한 식별자)를 추출
            #payload={'user_id:1'}

            payload = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256']) #accesstoken 번호
            user_id = payload.get('user_id') #1로 넣었는데 5가 나옴
            print(user_id) #5
            #해당 유저 아이디를 가지는 객체 user을 가져와
            user = get_object_or_404(User, id=user_id) #id=5인 애를 가져와야 됨
```
에서 
``` access_token = request.META['HTTP_AUTHORIZATION'].split()[1]```
를 짜지 못했다. 프론트가 request의 헤더에 토큰을 넣어서 보내는데, 그 토큰이 어떤 이름으로 오는지 몰랐기 때문이다. 또한
'~~ 토큰'으로 오길래 splite[1]로 뒤 토큰만 가져왔다.(현우오빠가 도와줌)

2. 
```user_id = payload.get('user_id') #1로 넣었는데 5가 나옴```에서 계속 에러가 났다.
![image](https://user-images.githubusercontent.com/99666136/236416796-da6f77f9-47ea-4457-9d94-ce3723f3ebc4.png)
그 이유는 내가 'id'와 'user_id'를 구분하지 못했기 때문이다. 프린트 문을 찍어보고 나서야 알게되었다.
   (앞으로 id라는 변수명은 잘 안 쓸 생각이다^^)


3. 
```
class User(AbstractBaseUser):
    # DB에 저장할 데이터를 선언!
    school_id = models.ForeignKey(School, on_delete=models.CASCADE, related_name='schoolId', null=True) # 외래키 자동생성
    user_id = models.CharField("사용자 계정", max_length=20, unique=True)
```
에서 school_id가 null이면 안된다길래, 외래키니까 null 허용해줬다.

### 후기
프론트할 때 jwt토큰을 구현해봤어서 전체적으로 쉽게 이해하며 코드를 짯다!
다만, cors에러 해결 코드에서 에러가 나는 상황인데 고쳐보겠다.
챗지피티씨한테 많이 물어보면서 했는데, 그래도 아직은 내가 더 잘하는 것 같다.✨
자세한 정리는 [JWT token 정리](https://jwkdevelop.tistory.com/72)에서 보면 된다!!


# AWS : EC2, RDS & Docker & Github Action

![image](https://github.com/Bakery-EFUB/Bakery-Back/assets/99666136/18c639e3-ba83-4763-8c4d-821572fd2f80)

### Docker
Docker란 가상 컨테이너 기술로, 어떤 OS에서도 같은 환경을 만들어줍니다.
그럼 이 Docker를 어떻게 배포할 수 있을까요?
Github Action은 docker-compose.prod.yaml 파일을 실행시켜, 
``` sh /home/ubuntu/srv/ubuntu/config/scripts/deploy.sh```로 들어가고, 
``` sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d```를
실행시킵니다. 그러면 이제 EC2서버가 build되고 실행됩니다.

- 여기서 EC2랑 어떻게 연결되는 건가요? docker-compose.prod.yaml을 보면
``` echo "${{ secrets.ENV_VARS }}" >> .env```
   라는 코드가 있습니다. 여기서 EC2와 연결됩니다.
- 그럼 Gihub Action이 배포하는 코드는 어디에 있나요? 
``` Gihub Action는 sudo docker-compose -f /home/ubuntu/srv/ubuntu/docker-compose.prod.yml up --build -d```를 실행한다고 했죠.
  여기서 nginx와 gunicorn을 통해 배포합니다. 
- docker-compose.yml파일과 docker-compose.prod.yml파일의 차이점은 무엇인가요? docker-compose.yml 파일은 로컬 개발 및 테스트 환경에서 사용되는 Docker Compose 설정 파일이고, docker-compose.prod.yml 파일은 프로덕션(운영) 환경에서 사용되는 Docker Compose 설정 파일입니다.


### EC2 
EC2는 AWS에서 제공하는 성능,용량 등을 유동적으로 사용할 수 있는 가상 서버입니다. 저희는 이 서버에 Django를 배포하는 것이죠.
그렇다면 EC2를 왜 사용하는 걸까요?
외부에서 본인이 만든 서비스에 접근하려면 24시간 작동하는 서버가 필요하겠죠. 하지만 저희는 집 pc를 24시간동안 구동시킬 수 없으니 서버를 빌리는 것입니다.
- 보안 그룹 생성
![image](https://github.com/Bakery-EFUB/Bakery-Back/assets/99666136/33b4259a-830d-4579-bddc-737921bb3513)

EC2에서 보안그룹 생성이 정말 중요합니다. 위 사진처럼 인바운드에 서버에 접근 가능한 서버,포트,ip를 설정해줍니다.
여기서 ssh란 리눅스 프로토콜로 나만 볼 수 있어야 합니다. 다른 사람이 내 도커에 접근하면 안 되니까.. (그래서 저렇게 소스를 0.0.0.0/0으로 하면 안되고,,, 본인 집 ip로 쓰길 바란다.)
클라이언트는 Http 프로토콜로 들어올 것이니 0.0.0.0/0으로 할당해줍니다.

- pem키(비밀키)는 매칭되는 공개키를 가지고 있습니다. 그 공개키를 EC2 인스턴스가 가지고 있기때문에, pem키가 유출되는 순간 서버에서 가상화폐가 채굴되는 것을 볼 수 있습니다.
- 탄력적 ip란 AWS의 고정 ip를 말합니다. 요금을 아끼기 위해 잠깐 인스턴스를 중지하고 다시 시작하면 ip가 바뀝니다. 이걸 방지하기 위해 고정 ip를 할당하는 것입니다. (저는 안 했다가 바뀐지도 몰라서 1시간을 날렸답니다^^..)
- 이때, 탄력적 ip를 할당하고 바로 EC2에 연결하지 않을 시 비용 청구가 되며, 인스턴스를 삭제할 때도 탄력적 ip를 삭제하지 않으면 비용 청구가 되니 유의하시길..
- EC2 서버에 접속하기 위해서 window는 os환경을 Linux로 만들어주어야 합니다. 이때 putty를 사용한다고는 하는데, 아직 잘 몰라서 패스하겠습니다!


### RDS
RDS는 AWS에서 지원하는 클라우기반 관계형 데이터베이스입니다. 
- 파라미터 그룹 생성
time_zone, Character set을 변경해 데이터베이스에 담기는 도메인을 넓혀줍니다. 그 후, 데이터베이스에 연결합니다. 이때, 간혹 파라미터 그룹이 제대로 반영되지 않을 때가 있으니 재부팅해줍니다. (저는 이걸 안해서 1시간을 날렸답니다^^..)
그 후, mySQL workbench에 연결해줍니다. 

### 과제
![image](https://github.com/Bakery-EFUB/Bakery-Back/assets/99666136/c88edf34-8fbc-4c1a-b4ce-137617405da9)
잘 연결되었습니다!!

### 오류
- 인스턴스 생성시 AMI선택을 ubuntu로 안하고 Amazon Linux로 선택해, CEOS에서 준 'deploy.yml'과 달라 4시간을 날렸다. => 해결
- .env.prod를 깃허브에 올려버렸다 => 해결

### 회고
코드 짜는 것보다 더 어려웠다. 1부터 10까지 다 모르는 용어라, 엄청 생소했다. (예지랑 현우오빠 없었으면, 난 울었을 것 같다.)
프리티어로 가입했지만, 돈 나갈까봐 두려워서 엄청 꼼꼼히 찾아본 것 같다. 도커랑 ec2가 어떻게 연결되는 건지, github action은 또 어떻게 배포를 해준다는 건지 이제는 좀 알 것 같다.



# AWS : https 인증



### 로드 밸랜서(ALB)
- 로드 밸런서란 서버에 가해지는 트래픽을 여러대의 서버에게 균등하게 분산시켜주는 역할을 한다.
- 비용 절감과 무중단 서비스 제공에서 장점을 가진다.

![image](https://github.com/Bakery-EFUB/bakery_front/assets/99666136/2e43cc29-457d-4064-b8c2-b4ecab72c663)

1. 리스너: 사용자에게서 요청을 받아들여 이 요청을 처리할 적절한 대상그룹으로 전달
2. 규칙: HTTP관련 정보를 해석한 뒤,어떤 대상그룹에 전달할지 판단되는 기준
3. 대상그룹: 요청을 처리할 EC2가 모여있는 대상그룹

- HTTPS 리스너를 사용하기 위해서는 SSL 인증서가 필수. HTTP 리스너의 포트는 기본적으로 80이며 HTTPS 리스너의 포트는 기본적으로 443이다.
- 상태확인(health checks)은 타겟그룹에 원하는 경로와 포트를 설정하여 HTTP 또는 HTTPS로 잘 요청이 오는지 확인한다.
- ALB의 대상그룹은 HTTP 또는 HTTPS만 허용한다. 이는 대상그룹에 속한 EC2가 해당 protocol만을 받아들인다는 뜻이다.

 
### 에러(400,502,응답 없음)

1. putty를 통한 ssh 접속 후 docker의 log 확인
![image](https://github.com/Bakery-EFUB/bakery_front/assets/99666136/c8bbea78-c89f-4eb9-ad26-bc9b01d2a636)
=> docker는 잘 돌아간다.

2. nginx의 실행여부 확인
![image](https://github.com/Bakery-EFUB/bakery_front/assets/99666136/8c3848de-982e-4f6d-bb53-f13566c572a5)
=> nginx도 잘 돌아간다.

3. env파일의 수정
ALLOWED_HOSTS = ['0.0.0.0']를 하면 400에러가 나고, private_IP를 할당하면 502에러가 난다.

4. 인스턴스 설정부터 재작업
인스턴스를 삭제하고 처음부터 다시 작업했다.
![image](https://github.com/Bakery-EFUB/bakery_front/assets/99666136/8be85360-dd30-4ae0-ba18-b7cad6be087c)
퍼블릭 도메인 주소로 직접 host를 하면 잘되나, 구매한 도메인만 연결하면 다시 400에러가 발생한다.

5. route53의 재설정
![image](https://github.com/Bakery-EFUB/Bakery-Back/assets/99666136/e38ff404-04f3-46e6-9d20-d4b91af3346e)
여기서 주황색 형광펜의 ceos.이 보이나요? 이걸 빈칸으로 뒀어야 했는데, 임의로 설정해서 에러가 났던 것이다.
+ 빨간색으로 설정해둔 것을 alb로 연결하지 않았다.

6. healthy error: 로드밸런서가 active 상태가 되기 전에 대상그룹을 연결해버려서 에러가 났다. 이것때문에 계속 도메인 연결이 안됐던 것...도 이유인 것 같다.
+ 도메인으로 보낼 땐, https://도메인이름/으로 보내주자.

### 에러 해결
![image](https://github.com/Bakery-EFUB/Bakery-Back/assets/99666136/49b72c47-4d99-4254-bafb-02f4900dc8da)


### 후기
설정하나 잘 못해서 시간을 엄청 날렸다.... 덕분에 설정로직을 거의 다 외워버린 것 같다 ㅎ 저 도와주신 분들,, 너무 감사합니다. 운영진 짱짱 멋져요❣






