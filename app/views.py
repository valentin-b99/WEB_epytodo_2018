##
## EPITECH PROJECT, 2018
## views.py
## File description:
## views
##

from app import *

@app.route('/', methods = ['GET'])
def route_home():
    controller = Controller(app, get_connection())
    return controller.index()

@app.route('/register', methods = ['POST'])
def route_register():
    controller = AuthController(app, get_connection())
    return controller.register(request)

@app.route('/signin', methods = ['POST'])
def route_signin():
    controller = AuthController(app, get_connection())
    return controller.signin(request)

@app.route('/signout', methods = ['POST'])
def route_signout():
    controller = AuthController(app, get_connection())
    return controller.signout(request)

@app.route('/user', methods = ['GET'])
def route_user_info():
    controller = UserController(app, get_connection())
    return controller.view_user_info()

@app.route('/user/task', methods = ['GET'])
def route_user_tasks():
    controller = UserController(app, get_connection())
    return controller.view_user_tasks()

@app.route('/user/task/<int:task_id>', methods = ['GET'])
def route_user_task(task_id):
    controller = UserController(app, get_connection())
    return controller.view_user_task(task_id)

@app.route('/user/task/add', methods = ['POST'])
def route_create_task():
    controller = UserController(app, get_connection())
    return controller.create_task(request)

@app.route('/user/task/del/<int:task_id>', methods = ['POST'])
def route_delete_task(task_id):
    controller = UserController(app, get_connection())
    return controller.delete_task(request, task_id)

@app.route('/user/task/<int:task_id>', methods = ['POST'])
def route_edit_task(task_id):
    controller = UserController(app, get_connection())
    return controller.edit_task(request, task_id, True)

@app.route('/user/task/edit/<int:task_id>', methods = ['POST'])
def route_edit_task2(task_id):
    controller = UserController(app, get_connection())
    return controller.edit_task(request, task_id, False)

@app.route('/user/edit/password', methods = ['POST'])
def route_user_edit_password():
    controller = AuthController(app, get_connection())
    return controller.edit_password(request)

@app.route('/user/edit/email', methods = ['POST'])
def route_user_edit_email():
    controller = AuthController(app, get_connection())
    return controller.edit_email(request)