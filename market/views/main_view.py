from flask import Blueprint, redirect, url_for, render_template
from market.models import Item

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template('main.html', items=items)