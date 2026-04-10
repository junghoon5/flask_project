from flask import Blueprint, redirect, url_for, render_template
from market.models import Item

bp = Blueprint('main_view', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('main.html')

@bp.route('/signup')
def signup():
    return render_template('auth/signup.html')

@bp.route('/detail/<item_id>/')  # 2. 주소 뒤에 상품 ID를 받도록 설정합니다.
def detail(item_id):
    # 3. DB에서 ID에 해당하는 상품 정보를 하나 가져옵니다.
    product = Item.query.get_or_404(item_id)
    # 4. 가져온 데이터를 'product'라는 이름으로 HTML에 전달합니다.
    return render_template('detail.html', product=product)