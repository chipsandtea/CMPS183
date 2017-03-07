
# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import json

def get_user_name_from_email(email):
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])



def index():

    posts = db(db.post).select(orderby=~db.post.created_on, limitby=(0,20))
    for p in posts:
        p.name = get_user_name_from_email(p.user_email)
    return dict(posts=posts)


@auth.requires_login()
def edit():

    if request.args(0) is None:
        form_type = 'create'
        form = SQLFORM(db.post)
    else:
        form_type = 'made'
        p = ((db.post.user_email == auth.user.email) & (db.post.id == request.args(0)))
        q = db(p).select().first()
        if q is None:
            session.flash = T('Not Authorized')
            redirect(URL('default', 'index'))
        form = SQLFORM(db.post, q, showid=False,deletable=True,)
    if form.process().accepted:
        logger.info("Our items are: %r" % form.vars.post_content)
        if form_type == 'create':
            session.flash = T('Added new post')
        else:
            session.flash = T('Edited your post')
        redirect(URL('default', 'index'))
    elif form.process().errors:
        session.flash = T('Please enter content.')

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


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
