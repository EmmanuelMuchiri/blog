from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import PostForm,SubscriberForm,CommentForm
from ..import db,photos
from ..models import User,Post,Role,Subscriber,Comment
from flask_login import login_required,current_user
import markdown2
from ..email import mail_message
from ..request import get_quote

@main.route('/')
def index():

    name  = "Quote"
    quote = get_quote()
    
    return render_template('index.html',name = name,quote = quote)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route("/new_post",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        new_post=Post(title=title,post=post,category=category)

        new_post.save_post()

        subscribers=Subscriber.query.all()

        for subscriber in subscribers:
            mail_message("New Blog Post","email/new_post",subscriber.email,post=new_post)

        return redirect(url_for('main.index'))

    title="Make a post"
    return render_template('new_post.html',title=title,post_form=form)