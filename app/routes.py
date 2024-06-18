from flask import render_template, request, redirect, url_for, flash
from app import app, db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@login_required # На главную страницу index.html юзер попадет, только если он залогинен
def index():
    return render_template('index.html')

# Создаём маршрут для страницы регистрации аккаунта, обрабатываем методы GET и POST
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Кодируем пароль для безопасной передачи данных
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login')) # Идёт переброс на страницу login.html

    return render_template('register.html', form=form)

# Создаём маршрут для страницы входа в аккаунт, также обрабатываем методы GET и POST
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() # Ищем в БД первого попавшегося юзера с указанным username
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Введены неверные данные', 'danger')

    return render_template('login.html', form=form)


# Создаём маршрут для страницы редактирования данных юзера
@app.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
        db.session.commit()
        flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('update_account.html', title='Update Account', form=form)


# Создаём маршрут для выхода из аккаунта
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# Создаём маршрут для игры
@app.route('/click')
@login_required
def click():
    current_user.clicks += 1
    db.session.commit()
    return redirect(url_for('index'))