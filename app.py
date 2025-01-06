from flask import Flask, render_template, request, redirect, url_for, session
import os
import sys
import io

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Простая база пользователей
users = {'user1': 'password123'}

# Главная страница
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('tasks'))
    return render_template('index.html')

# Страница авторизации
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if users.get(username) == password:
        session['username'] = username
        return redirect(url_for('tasks'))
    return 'Invalid credentials', 401

# Страница с заданиями
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if 'username' not in session:
        return redirect(url_for('index'))

    result = ""
    if request.method == 'POST':
        user_code = request.form['user_code']
        try:
            # Выполняем код безопасно, с использованием перенаправления stdout
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()  # Перехватываем вывод
            exec(user_code)  # Выполнение кода пользователя
            result = sys.stdout.getvalue()  # Получаем результат выполнения
            sys.stdout = old_stdout  # Восстанавливаем stdout
        except Exception as e:
            result = str(e)  # Если ошибка в коде, выводим её
    
    return render_template('tasks.html', result=result)

# Выход из аккаунта
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
