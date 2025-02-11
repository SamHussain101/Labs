import click, sys
from models import db, User, Todo
from sqlalchemy.exc import IntegrityError
from app import app


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.init_app(app)  # Ensure db is initialized
    db.create_all()
    bob = User('bob', 'bob@mail.com', 'bobpass')
    bob.todos.append(Todo('wash car'))
    db.session.add(bob)
    db.session.commit()
    print(bob)
    print('Database initialized')


@app.cli.command("get-user", help="Retrieves a User by username or id")
@click.argument('key', default='bob')
def get_user(key):
    user = User.query.filter_by(username=key).first()
    if not user:
        try:
            user = User.query.get(int(key))
        except ValueError:
            print(f'{key} not found!')
            return
        if not user:
            print(f'{key} not found!')
            return
    print(user)


@app.cli.command("change-email")
@click.argument('username', default='bob')
@click.argument('email', default='bob@mail.com')
def change_email(username, email):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f'{username} not found!')
        return
    user.email = email
    db.session.commit()
    print(user)


@app.cli.command('get-users')
def get_users():
    users = User.query.all()
    print(users)


@app.cli.command('create-user')
@click.argument('username', default='rick')
@click.argument('email', default='rick@mail.com')
@click.argument('password', default='rickpass')
def create_user(username, email, password):
    new_user = User(username, email, password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print("Username or email already taken!")
    else:
        print(new_user)


@app.cli.command('delete-user')
@click.argument('username', default='bob')
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f'{username} not found!')
        return
    db.session.delete(user)
    db.session.commit()
    print(f'{username} deleted')


@app.cli.command('add-todo')
@click.argument('username', default='bob')
@click.argument('text', default='wash car')
def add_task(username, text):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f'{username} not found!')
        return
    new_todo = Todo(text)
    user.todos.append(new_todo)
    db.session.commit()
    print('Todo added!')


@app.cli.command('get-todos')
@click.argument('username', default='bob')
def get_user_todos(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f'{username} not found!')
        return
    print(user.todos)


@app.cli.command('toggle-todo')
@click.argument('todo_id', default=1)
@click.argument('username', default='bob')
def toggle_todo_command(todo_id, username):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f'{username} not found!')
        return

    todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
    if not todo:
        print(f'{username} has no todo with ID {todo_id}')
        return

    todo.toggle()
    db.session.commit()  # Commit change
    print(f'{todo.text} is {"done" if todo.done else "not done"}!')


@app.cli.command('add-category', help="Adds a category to a todo")
@click.argument('category', default='chores')
@click.argument('todo_id', default=1)
@click.argument('username', default='bob')
def add_todo_category_command(category, todo_id, username):
    user = User.query.filter_by(username=username).first()
    if not user:
        print(f'User {username} not found!')
        return

    res = user.add_todo_category(todo_id, category)
    if not res:
        print(f'{username} has no todo with ID {todo_id}')
        return

    todo = Todo.query.get(todo_id)
    print(todo)
