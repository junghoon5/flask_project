from functools import wraps

import requests
from flask import Blueprint, request, redirect, url_for, flash, render_template, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from market import db
from market.forms import UserCreateForm, UserLoginForm
from market.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


# 회원가입(일반)
@bp.route('/signup/', methods=['GET', 'POST'])

# 일반 아이디 회원가입
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 아이디 중복 체크
        user = User.query.filter_by(login_id=form.user_id.data).first()
        if not user:

            new_user = User(
                login_id=form.user_id.data,
                username=form.username.data,
                password=generate_password_hash(form.password1.data),
                email=form.email.data,
                phone=form.phone.data
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash('이미 존재하는 아이디입니다.')
    return render_template('auth/signup.html', form=form)

# 로그인(일반)
@bp.route('/login/', methods=['GET', 'POST'])

# 일반 아이디 로그인
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(login_id=form.username.data).first()
        if not user:
            error = '존재하지 않는 사용자입니다.'
        elif not check_password_hash(user.password, form.password.data):
            error = '비밀번호가 올바르지 않습니다.'
        if error is None:
            session.clear()
            session['user_id'] = user.id

            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():

    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.get(User, user_id)
# 로그인 권한요청 매번하지 않게
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped_view

# 로그아웃 - 세션 정보를 모두 삭제
@bp.route('/logout/')
def logout():
    session.clear() # 세션의 모든 정보(user_id 등) 삭제
    return redirect(url_for('main.index')) # 로그아웃 후 메인 페이지로 이동


# 아이디 찾기
@bp.route('/find_account/', methods=['GET', 'POST'])
def find_account():
    if request.method == 'POST':
        input_name = request.form.get('username')
        input_email = request.form.get('email')
        user = User.query.filter_by(username=input_name, email=input_email).first()
        if user:
            flash(f"찾으시는 아이디는 [{user.login_id}] 입니다.", "success")
        else:
            flash("일치하는 회원 정보가 없습니다.", "danger")
    return render_template('auth/find_account.html')


# 카카오 로그인 설정값
CLIENT_ID = "e17055a5c7eb91012c7140978ae7788a"
CLIENT_SECRET = "pBLVBBvlQebKOiGfJxZWa0h9VxRPRcTu"
REDIRECT_URI = "http://localhost:5000/auth/kakao/callback/"
SIGNOUT_REDIRECT_URI = "http://127.0.0.1:5000/auth/logout/callback/"

# 카카오 서버와 직접 통신하는 클래스
class Oauth:
    def __init__(self):
        self.auth_server = "https://kauth.kakao.com%s"
        self.api_server = "https://kapi.kakao.com%s"
        self.default_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }

   # 유저의 프로필 정보 요청
    def auth(self, code):
        return requests.post(
            url=self.auth_server % "/oauth/token",
            headers=self.default_header,
            data={
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "code": code,
            },
        ).json()

    def userinfo(self, bearer_token):
        return requests.get(
            url=self.api_server % "/v2/user/me",
            headers={**self.default_header, **{"Authorization": bearer_token}}
        ).json()

 # 카카오 로그인 라우팅
@bp.route('/kakao/')
def kakao_sign_in():
    kakao_oauth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&prompt=login"
    return redirect(kakao_oauth_url)


# 카카오 콜백 함수
@bp.route('/kakao/callback/')

# 카카오가 보내준 인증 코드 받기
def callback():
    code = request.args.get("code")
    if not code:
        return redirect(url_for('auth.login'))

# 인증 코드로 토큰 요청
    oauth = Oauth()
    auth_info = oauth.auth(code)

    if "error" in auth_info:
        flash(f"인증 실패: {auth_info.get('error_description')}")
        return redirect(url_for('auth.login'))

# 토큰으로 유저 정보 요청
    user_data = oauth.userinfo("Bearer " + auth_info['access_token'])

    if not user_data or "id" not in user_data:
        flash("카카오 정보를 불러오지 못했습니다.")
        return redirect(url_for('auth.login'))

    kakao_account = user_data.get("kakao_account", {})
    profile = kakao_account.get("profile", {})
    nickname = profile.get("nickname", "카카오유저")
    email = kakao_account.get("email") or f"{user_data.get('id')}@kakao.com"

    # DB 연동 및 로그인
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            login_id=str(user_data.get('id')),
            username=nickname,
            email=email,
            password=generate_password_hash(str(user_data.get('id')))
        )
        db.session.add(user)
        db.session.commit()

    session.clear()
    session['user_id'] = user.id
    session['is_kakao'] = True

    return redirect(url_for('main_view.index'))