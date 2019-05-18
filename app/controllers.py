##
## EPITECH PROJECT, 2018
## controllers.py
## File description:
## controllers
##

from app import *
from app.models import *
from app.api import *
from flask import *
import datetime
import pymysql as sql

class Controller(object):

    def __init__(self, app, conn):
        self.app = app
        self.conn = conn
        self.user = User(app, conn)
        self.api = API(app, conn)

    def index(self):
        nb_tasks_pr = []
        nb_tasks_late = -1
        if session.get('username') and session.get('id'):
            nb_tasks_pr = json.loads(self.api.get_number_tasks_in_progress(self.api, session['id']))['result']
            nb_tasks_late = json.loads(self.api.get_number_tasks_late(self.api, session['id']))['result']
        tasks = json.loads(self.api.task_all_tasks())
        return render_template("index.html", nb_tasks_pr=nb_tasks_pr, tasks_list=tasks['result'], nb_tasks_late=nb_tasks_late)

class AuthController(object):

    def __init__(self, app, conn):
        self.app = app
        self.conn = conn
        self.api = API(app, conn)

    def register(self, request):
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password-confirm']
        email = request.form['email']
        result = self.api.user_create(username, password, password_confirm, email)
        flash(json.loads(result))
        return redirect(url_for('route_home'))

    def signin(self, request):
        username = request.form['username']
        password = request.form['password']
        flash(json.loads(self.api.user_login(username, password)))
        return redirect(url_for('route_home'))

    def signout(self, request):
        flash(json.loads(self.api.user_logout()))
        return redirect(url_for('route_home'))

    def edit_password(self, request):
        if not session.get('id'):
            return redirect(url_for('route_home'))
        cur_pass = request.form['current-password']
        new_pass = request.form['new-password']
        new_pass_confirm = request.form['new-password-confirm']
        result = self.api.user_edit_password(session['username'], cur_pass, new_pass, new_pass_confirm)
        flash(json.loads(result))
        return redirect(url_for('route_user_info'))

    def edit_email(self, request):
        if not session.get('id'):
            return redirect(url_for('route_home'))
        email = request.form['email']
        result = self.api.user_edit_email(session['username'], email)
        flash(json.loads(result))
        return redirect(url_for('route_user_info'))

class UserController(object):

    def __init__(self, app, conn):
        self.app = app
        self.conn = conn
        self.api = API(app, conn)

    def view_user_info(self):
        if not session.get('id'):
            return redirect(url_for('route_home'))
        nb_tasks_pr = json.loads(self.api.get_number_tasks_in_progress(self.api, session['id']))['result']
        nb_tasks = self.api.get_number_tasks(self.api)
        nb_tasks_late = json.loads(self.api.get_number_tasks_late(self.api, session['id']))['result']
        user_info = json.loads(self.api.get_user_info(session['id']))
        return render_template("profile.html", user_info=user_info, nb_tasks_pr=nb_tasks_pr, nb_tasks=nb_tasks, nb_tasks_late=nb_tasks_late)

    def view_user_tasks(self):
        if not session.get('id'):
            return redirect(url_for('route_home'))
        tasks = json.loads(self.api.task_get_all(session['id']))
        utc = datetime.datetime.utcnow()
        nb_tasks_pr = json.loads(self.api.get_number_tasks_in_progress(self.api, session['id']))['result']
        nb_tasks_late = json.loads(self.api.get_number_tasks_late(self.api, session['id']))['result']
        return render_template("profile_tasks.html", tasks_list=tasks['result'], nb_tasks_pr=nb_tasks_pr, nb_tasks_late=nb_tasks_late)

    def view_user_task(self, task_id):
        if not session.get('id'):
            return redirect(url_for('route_home'))
        task = None
        result = json.loads(self.api.task_get_by_id(task_id))
        if 'error' in result:
            flash(result)
        else:
            task = result['result']
        nb_tasks_pr = json.loads(self.api.get_number_tasks_in_progress(self.api, session['id']))['result']
        nb_tasks_late = json.loads(self.api.get_number_tasks_late(self.api, session['id']))['result']
        return render_template("view_task.html", task=task, nb_tasks_pr=nb_tasks_pr, nb_tasks_late=nb_tasks_late)

    def edit_task(self, request, task_id, task_page):
        if not session.get('id'):
            return redirect(url_for('route_home'))
        title = request.form['title']
        begin = request.form['date-begin'] + " " + request.form['clock-begin']
        end = request.form['date-end'] + " " + request.form['clock-end']
        status = request.form['status']
        if not request.form.get('private-status'):
            private = 0
        else:
            private = 1
        result = self.api.task_edit(task_id, title, begin, end, status, private)
        flash(json.loads(result))
        if task_page:
            return redirect(url_for('route_user_task', task_id=task_id))
        else:
            return redirect(url_for('route_user_tasks'))

    def create_task(self, request):
        if not session.get('id'):
            return redirect(url_for('route_home'))
        title = request.form['title']
        begin = request.form['date-begin'] + " " + request.form['clock-begin']
        end = request.form['date-end'] + " " + request.form['clock-end']
        status = request.form['status']
        if not request.form.get('private-status'):
            private = 0
        else:
            private = 1
        result = self.api.task_create(title, begin, end, status, private)
        flash(json.loads(result))
        return redirect(url_for('route_user_tasks'))

    def delete_task(self, request, id):
        if not session.get('id'):
            return redirect(url_for('route_home'))
        result = self.api.task_delete(id)
        flash(json.loads(result))
        return redirect(url_for('route_user_tasks'))

class ConnectionManager(object):

    def __init__(self, app):
        self.app = app
        self.conn = None
        self.connect(app.config)

    def connect(self, config):
        try:
            self.conn = sql.connect(host=config['DB_HOST'],
                                    user=config['DB_USER'],
                                    password=config['DB_PASS'],
                                    db=config['DB_NAME'])
            if self.conn == None:
                raise Exception
        except (Exception) as error:
            print(error)
            exit(84)

    def get_connection(self):
        return self.conn