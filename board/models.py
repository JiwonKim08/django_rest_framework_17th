from django.db import models
from account.models import School,User,CommonInfo

class Board(CommonInfo):
    # DB에 저장할 데이터를 선언
    school_id = models.ForeignKey(School, on_delete=models.CASCADE, related_name='boardId')  # 외래키 자동생성
    name = models.CharField("게시판 이름", max_length=20, unique=True)
    category = models.CharField("카테고리", max_length=20)

    def __str__(self):
        return 'school_id: {}, boardname: {}'.format(self.school_id, self.name)


class Fixed_board(CommonInfo):
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE,related_name='fixedboardId')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("즐겨찾기 게시판 이름", max_length=20)

    def __str__(self):
        return 'fixed_board_name: {}'.format(self.name)


class Post(CommonInfo):
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='postId')
    title = models.CharField("게시물 제목", max_length=100)
    writer = models.ForeignKey(User, on_delete=models.PROTECT)
    postcontent = models.CharField("본문", max_length=255)
    is_anonymous = models.BooleanField("익명 여부", default=False)
    like_cnt = models.PositiveIntegerField("좋아요 수",default=0)
    comment_cnt = models.PositiveIntegerField("댓글 수",default=0)
    scrap_cnt = models.PositiveIntegerField("스크랩 수",default=0)

    def __str__(self):
        return self.title

class Photo(CommonInfo):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photoId')
    file_name = models.CharField("파일 이름", max_length=500)

class Scrap(CommonInfo):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='scrapuserId')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='scrappostId')

class Comment(CommonInfo):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='commentuserId')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='commentpostId')
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE)
    commentcontent = models.CharField(max_length=255, null=False)
    is_anonymous = models.BooleanField("익명 여부", default=False)
    like_cnt = models.PositiveIntegerField("좋아요 수")

    def __str__(self):
        return 'comment_content: {}'.format(self.commentcontent[:10])

