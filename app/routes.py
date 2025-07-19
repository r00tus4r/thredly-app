from flask import render_template, Blueprint
import json

bp = Blueprint('routes', __name__)

@bp.route('/')
@bp.route('/home')
def home():
    with open('data/threads.json', 'r', encoding='utf-8') as f: threads = json.load(f)
    return render_template('home.html', threads=threads)