
from search import Search
from flask import Flask, render_template, redirect, url_for, request, session
import os
import random

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('search.html', search='hello world')
	# return redirect(url_for("item", product=''))

# @app.route("/item/<search>/", methods=["GET", "POST"])
# def pairs(search):
# 	if request.method == 'POST':
# 		search = request.form.get("search", search)
# 		return redirect(url_for("search", search))

# 	return render_template('search.html', search=search)

app.run(debug=True) 