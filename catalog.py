#!/usr/bin/env python2
#
#
from flask import (
    Flask, render_template, request, redirect,
    jsonify, url_for, flash, make_response
    )
from flask import session as login_session

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from catalog_database import Base, User, CatalogItem

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'secret key'
# Connect to Database and create database session
engine = create_engine(
    'postgresql://catalog:password@localhost/catalog'
    )
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

scope = 'https://www.googleapis.com/auth/userinfo.email'
scope = scope + ' https://www.googleapis.com/auth/userinfo.profile'
# Displays the description of an item if an item is provited,
# otherwise displays a list of item within the requested category
# if a category is provided, otherwise displays the latest 10 items


@app.route('/')
@app.route('/<category>')
@app.route('/<category>/<item>')
def showCategory(category=None, item=None):
    query = session.query(
        CatalogItem.category.distinct().label('category')).order_by(asc(
            CatalogItem.category
        )
        )
    categories = [row.category for row in query.all()]
    if category is not None:
        items = session.query(CatalogItem).filter_by(
            category=category).order_by(asc(CatalogItem.name))
    else:
        items = session.query(CatalogItem).order_by(
            desc(CatalogItem.id)).limit(10).all()
    if item is not None:
        item = session.query(CatalogItem).filter_by(
            category=category, name=item).limit(1).one()
    return render_template(
        'catalog_new.html', categories=categories,
        entry=item, items=items, login_session=login_session
        )

# GET displays the page to create a new item,
# POST adds a new item to the database


@app.route('/new', methods=['GET', 'POST'])
def createItem():
    if login_session.get('email') is not None:
        if request.method == 'POST':
            if login_session.get('email') is not None:
                newItem = CatalogItem(
                    name=request.form['name'],
                    description=request.form['description'],
                    category=request.form['category'],
                    user_email=login_session['email']
                    )
                session.add(newItem)
                session.commit()
                flash(request.form['name'] + " created.")
                return redirect(url_for(
                    'showCategory',
                    category=request.form['category'],
                    item=request.form['name'])
                    )
            else:
                flash("Error: You must be logged in to create an item.")
                return redirect(url_for('showCategory'))
        else:
            return render_template(
                'createItem.html',
                login_session=login_session
                )
    else:
        return redirect(url_for('login'))

# GET displays the page to edit a item, POST edits an item in the database


@app.route('/<category>/<item>/edit', methods=['GET', 'POST'])
def editItem(category, item):
    if login_session.get('email') is not None:
        if request.method == 'POST':
            item = session.query(CatalogItem).filter_by(
                category=category, name=item
                ).limit(1).one()
            if login_session['email'] == item.user_email:
                item.name = request.form['name']
                item.description = request.form['description']
                item.category = request.form['category']
                session.commit()
                flash(request.form['name'] + " edited.")
                return redirect(url_for('showCategory'))
            else:
                flash(
                    '''Error: You must be logged in and
                    have created an item to edit that item.'''
                )
                return redirect(url_for('showCategory'))
        else:
                item = session.query(CatalogItem).filter_by(
                    category=category, name=item
                    ).limit(1).one()
                return render_template(
                    'editItem.html', item=item, login_session=login_session
                    )
    else:
        return redirect(url_for('login'))

# GET displays a confirmation page to delete an item, POST deletes the item


@app.route('/<category>/<item>/delete', methods=['GET', 'POST'])
def deleteItem(category, item):
    if login_session.get('email') is not None:
        if request.method == 'POST':
            itemName = item
            if session.query(CatalogItem).filter_by(
                    category=category, name=item
                    ).limit(1).count() > 0:
                item = session.query(CatalogItem).filter_by(
                    category=category,
                    name=item
                    ).limit(1).one()
            else:
                flash(item + " not found")
                return redirect(url_for('showCategory'))
            if login_session['email'] == item.user_email:
                session.delete(item)
                session.commit()
                flash(itemName + " deleted.")
                return redirect(url_for('showCategory'))
            else:
                flash(
                    '''Error: Items can only be deleted
                     by the user who made them.'''
                )
                return redirect(url_for('showCategory'))
        else:
            return render_template(
                'deleteItem.html', category=category, item=item,
                login_session=login_session
                )
    else:
        return redirect(url_for('login'))

# API -----------------------------------------------------
# GET returns a json object of the categories


@app.route('/api/v1')
def catalogJson():
    query = session.query(CatalogItem).order_by(asc(CatalogItem.name))
    items = query.all()
    return jsonify([item.serialize for item in items])

# GET returns a json object of the items within a category


@app.route('/api/v1/<category>')
def categoryJson(category):
    query = session.query(CatalogItem).filter_by(
        category=category
        ).order_by(asc(CatalogItem.name))
    items = query.all()
    return jsonify([item.serialize for item in items])

# GET returns a json object of an item


@app.route('/api/v1/<category>/<item>')
def itemJson(category, item):
    item = session.query(CatalogItem).filter_by(
        category=category, name=item
        ).one()
    return jsonify(item.serialize)

# Authentication --------------------------------------------
# redirect the user to OAuth provider


@app.route('/login')
def login():
    flow = flow_from_clientsecrets(
        '/home/ubuntu/udacity-linux-configuration/client_secrets.json',
        scope=scope,
        redirect_uri = 'http://3.220.93.200.xip.io/connect'
	)
    return redirect(flow.step1_get_authorize_url())

# POST logs the user in


@app.route('/connect', methods=['Get', 'POST'])
def connect():
    flow = flow_from_clientsecrets(
        '/home/ubuntu/udacity-linux-configuration/client_secrets.json',
        scope=scope,
        redirect_uri=url_for('connect', _external=True))
    # exchange the token for credentials
    try:
        code = request.args.get('code')
        if code is not None:
            credentials = flow.step2_exchange(code)
        else:
            return "access was denied"
    except FlowExchangeError:
        return "failed to aqcuire authorization"
    # use the credentials to get the users information
    # and store it in the login_session
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': credentials.access_token}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['name'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['access_token'] = credentials.access_token
    if session.query(User).filter_by(email=login_session['email']).count() == 0:
	newUser = User(email=login_session['email'],name=login_session['name'],picture=login_session['picture'])
	session.add(newUser)
	session.commit()
    flash('logged in as ' + login_session['name'])
    return redirect(url_for('showCategory'))

# POST logs a user out


@app.route('/disconnect', methods=['POST', 'GET'])
def disconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        flash('User not logged in')
        return redirect(url_for('showCategory'))
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        login_session['email'] = None
        flash('User successfully logged out.')
        return redirect(url_for('showCategory'))
    else:
        flash('Failed to log user out')
        return redirect(url_for('showCategory'))

if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
