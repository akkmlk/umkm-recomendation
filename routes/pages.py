from flask import Blueprint, render_template, session, redirect, abort, request

pages = Blueprint("pages", __name__)

@pages.route('/')
def index():
    return render_template('index.html')

@pages.route('/result')
def result():
    return render_template('result-search.html')

@pages.route('/detail-product')
def detail_product():
    return render_template('detail-product.html')