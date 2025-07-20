from flask import render_template, Blueprint, flash, redirect, url_for
import json
from flask_login import login_required, current_user
from .forms import ThreadForm
from .models import Thread
from . import db

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def home():
    threads = Thread.query.all()
    form = ThreadForm()
    if form.validate_on_submit():
        thread = Thread(body=form.body.data, author=current_user)
        db.session.add(thread)
        db.session.commit()
        flash('Thread created successfully.', category='success')
        return redirect(url_for('routes.home'))
    return render_template('home.html', threads=threads, form=form)