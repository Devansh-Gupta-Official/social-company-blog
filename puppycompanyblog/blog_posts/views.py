#creating views
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from puppycompanyblog import db
from puppycompanyblog.models import BlogPost
from puppycompanyblog.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts', __name__)


#CREATE
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data, text=form.text.data, user_id=current_user.id)  #current_user.id is the foreign key to the User model
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created')
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)


#VIEW
@blog_posts.route('/<int:blog_post_id>') #dynamic url #int:blog_post_id is the variable that will be passed to the function #blog_post_id is the variable name
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title, date=blog_post.date, post=blog_post)