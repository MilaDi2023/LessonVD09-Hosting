from app import db, login_manager
from flask_login import UserMixin

# Создаём декоратор, который сообщает Flask, что функция будет использоваться для загрузки пользователя по его ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создаём класс User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    clicks = db.Column(db.Integer, default=0)

    def __repr__(self): # Функция, чтобы представить информацию о пользователе в виде одной строки
        return f"У пользователя {self.username} всего кликов: {self.clicks}"
