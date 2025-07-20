from flask import render_template, Blueprint
import json
from flask_login import login_required

bp = Blueprint('routes', __name__)

@bp.route('/')
@bp.route('/home')
@login_required
def home():
    with open('data/threads.json', 'r', encoding='utf-8') as f: threads = json.load(f)
    return render_template('home.html', threads=threads)