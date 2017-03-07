# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index1():
    """
    lets users login or logout
    """
    # for development purposes only:
    print auth.user_id

    return dict()

def index():
    """
    lets users login or logout
    """
    # for development purposes only:
    print "user_id: %s" % auth.user_id
    
    posts = get_posts()

    post_count = len(posts)
    first_ten = []
    i = 1
    for post in posts[:10]:
        post['index'] = i
        first_ten.append(post)
        i = i + 1

    print "post_count: %s" % post_count
    return dict(post_count=post_count, first_ten = first_ten)

def get_posts():
    """get posts, in reverse chronological order"""
    return db(db.post).select().sort(lambda p: p.updated_on, reverse=True)

@auth.requires_login()
def create_post():
    """form for posting a  new comment"""
    form = SQLFORM(db.post, 
                 labels= {'post_subject': "Subject", 'post_content': "Comment"},
                 submit_button = 'Submit your comment',
                  )

    if form.process(keepvalues=True).accepted:
       response.flash = 'comment accepted'

    elif form.errors:
       response.flash = 'please complete your post'
    else:
       response.flash = 'please post your comment'

    return dict(form=form)

@auth.requires_login()
def edit_post():
    """form for editing an existing post"""
    post = db.post[request.args(0)]
    if not(post and post.user_id == auth.user_id):
        redirect(URL('index'))
    form = SQLFORM(db.post, post,
                 labels= {'post_subject': "Subject", 'post_content': "Comment"},
                 showid= False,
                 deletable= True,
                 submit_button = 'Update your comment',
                  )

    if form.process(keepvalues=True).accepted:
       response.flash = 'comment accepted'

    elif form.errors:
       response.flash = 'please complete your post'
    else:
       response.flash = 'please edit your comment'

    return dict(form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)





