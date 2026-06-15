from ext import app, db
from flask import render_template, redirect, flash, request
from forms import RegisterForm, PlaceForm, LoginForm, ReviewForm
from models import Place, Review, User
from flask_login import login_user, logout_user, login_required, current_user
from os import path
from flask_paginate import Pagination, get_page_parameter


@app.route("/")
def home():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 6
    places = Place.query.paginate(page=page, per_page=per_page)
    pagination = Pagination(page=page, total=places.total, per_page=per_page)
    return render_template("index.html", places=places.items, pagination=pagination)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, role=form.role.data)
        new_user.password_set(form.password.data)
        new_user.create()
        flash("Registration successful :D")
        return redirect("/")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password_check(form.password.data):
            login_user(user)
            flash("Login Successful :D")
            return redirect("/")
        flash("Invalid username or password :(")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/add_place", methods=["GET", "POST"])
@login_required
def add_place():
    if current_user.role != "Admin":
        flash("You don't have permission:(")
        return redirect("/")
    form = PlaceForm()
    if form.validate_on_submit():
        new_place = Place(
            title=form.title.data,
            known_since=form.known_since.data,
            description=form.description.data
        )
        img = form.image.data
        if img:
            directory = path.join(app.root_path, "static", "images", img.filename)
            img.save(directory)
            new_place.image = img.filename
        flag = form.flag.data
        if flag:
            directory = path.join(app.root_path, "static", "images", flag.filename)
            flag.save(directory)
            new_place.flag = flag.filename
        new_place.create()
        flash("Place added successfully! :D")
        return redirect("/")
    return render_template("add_place.html", form=form)


@app.route("/update_place/<int:place_id>", methods=["GET", "POST"])
@login_required
def update_place(place_id):
    if current_user.role != "Admin":
        flash("You don't have permission:(")
        return redirect("/")
    place = Place.query.get(place_id)
    form = PlaceForm(title=place.title, known_since=place.known_since)
    if form.validate_on_submit():
        place.title = form.title.data
        place.known_since = form.known_since.data
        image = form.image.data
        if image:
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            place.image = image.filename
        place.save()
        return redirect("/")
    return render_template("add_place.html", form=form)


@app.route("/delete_place/<int:place_id>")
@login_required
def delete_place(place_id):
    if current_user.role != "Admin":
        flash("You don't have permission :(")
        return redirect("/")
    place = Place.query.get(place_id)
    place.delete()
    return redirect("/")


@app.route("/place/<int:place_id>", methods=["GET", "POST"])
def view_place_details(place_id):
    place = Place.query.get(place_id)
    reviews = Review.query.filter_by(place_id=place_id).all()
    form = ReviewForm()
    if form.validate_on_submit():
        new_review = Review(text=form.text.data, place_id=place_id)
        new_review.create()
        return redirect(f"/place/{place_id}")
    return render_template("place_details.html",
                           place=place,
                           reviews=reviews,
                           form=form)