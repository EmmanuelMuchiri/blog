from flask import render_template, request, redirect, url_for,abort
from . import main
# from .. import db,photos
from flask_login import login_required,current_user
from ..request import get_quote

@main.route('/')
def index():

    name  = "Quote"
    quote = get_quote()
    
    return render_template('index.html',name = name,quote = quote)