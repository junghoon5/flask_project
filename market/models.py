from market import db

# 유저
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(50), unique=True)  # 로그인용
    username = db.Column(db.String(50))               # 닉네임
    password = db.Column(db.String(200))
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(20), unique=True)

# 관리자
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(50), unique=True) # 관리자 로그인
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

# 상품 (4월14일 수정함)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_title = db.Column(db.String(100), unique=False) # 상품 제목
    item_price = db.Column(db.Integer) # 가격
    item_reg_datetime = db.Column(db.DateTime(), unique = False) # 상품 업로드 시간
    item_description = db.Column(db.String(500)) # 상품 내용
    # 어떤 유저가 올린 상품인지 연결 (외래키)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('item_set'))

# 상품 상태
class Item_Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_status = db.Column(db.String(100), unique=False)  # 상품 상태

# 카테고리
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=False)

# 댓글정보테이블
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    # 어떤 상품에 달린 댓글인지 연결 (Foreign Key)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='CASCADE'))
    item = db.relationship('Item', backref=db.backref('comment_set'))

    # (선택) 작성자 기능이 있다면 추가
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

