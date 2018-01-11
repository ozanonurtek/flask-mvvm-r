from project import app, login_manager
from flask_login import logout_user, current_user, login_required
from flask import render_template, request, url_for, redirect, flash
from project.models import User, db
from project.viewmodels import RegisterViewModel, LoginViewModel, EventViewModel
from project.forms import LoginForm, RegisterForm, EventForm


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template("index.html", title="Anasayfa"), 200


@app.route('/setup')
def setup():
    db.drop_all()
    db.create_all()
    return "OK", 200


@app.route('/giris')
def giris():
    form = LoginForm()
    if not current_user.is_authenticated:
        return render_template("giris.html", title="Giriş", form=form), 200
    else:
        return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    login_view_model = LoginViewModel(form=form, method=request.method)
    login_view_model.validate()
    return redirect(url_for('giris'))


@app.route('/etkinlik')
@login_required
def etkinlik():
    return render_template("wall.html", title="Etkinlik", events=EventViewModel.get_all_events()), 200


@app.route('/rezervasyon')
@login_required
def rezervasyon():
    form = EventForm()
    return render_template("booking.html", title="Rezervasyon", form=form), 200


@app.route('/booking', methods=['POST', 'GET'])
@login_required
def booking():
    form = EventForm(request.form)
    event_view_model = EventViewModel(form, request.method)
    event_view_model.submit_event()
    return redirect(url_for('rezervasyon'))


@app.route('/kayit')
@login_required
def kayit():
    form = RegisterForm()
    if current_user.isAdmin:
        return render_template("kayıt.html", title="Kayıt", form=form), 200
    else:
        return login_manager.unauthorized()


@app.route('/register', methods=['POST'])
@login_required
def register_check():
    form = RegisterForm(request.form)
    register_view_model = RegisterViewModel(form=form, method=request.method)
    register_view_model.validate()
    return redirect(url_for('kayit'))


@app.route('/kullanicilar')
@login_required
def kullanicilar():
    all_user = User.query.filter_by(isAdmin=False).all()
    return render_template("users.html", title="Kullanıcılar", users=all_user), 200


@app.route('/logout')
@login_required
def logout():
    flash("Başarıyla çıkış yaptınız " + current_user.username + ".", "success")
    logout_user()
    return redirect(url_for('index'))
