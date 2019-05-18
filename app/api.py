##
## EPITECH PROJECT, 2018
## api.py
## File description:
## api
##

from app import *
from app.models import *
from flask import *
import datetime

class API(object):

    def __init__(self, app, conn):
        self.app = app
        self.conn = conn
        self.user = User(app, conn)
        self.task = Task(app, conn)

    def user_create(self, username, password, password_confirm, email):
        res = {}
        if not username.isalnum():
            res['error'] = "internal error"
        elif self.user.exists(username):
            res['error'] = "account already exists"
        elif not username or not password or not email:
            res['error'] = "internal error"
        elif password != password_confirm:
            res['error'] = "Password doesn't match"
        elif self.user.exists_email(email):
            res['error'] = "email already used"
        else:
            self.user.create(username, password, email)
            session['username'] = username
            session['id'] = self.user.get_id(username)
            res['result'] = "account %s created and you are login !" % (username)
        return json.dumps(res)

    def user_login(self, username, password):
        ret = {}
        if not username and not password:
            ret['error'] = "login or password does not match"
        else:
            if not self.user.exists(username):
                ret['error'] = "login or password does not match"
            elif not self.user.check_password(username, password):
                ret['error'] = "login or password does not match"
            else:
                session['username'] = username
                session['id'] = self.user.get_id(username)
                ret['result'] = "Login successful"
        return json.dumps(ret)

    def user_logout(self):
        ret = {}
        session.pop('username', None)
        session.pop('id', None)
        ret['result'] = "Logout successful"
        return json.dumps(ret)

    def user_edit_password(self, username, curr_pass, new_pass, new_pass_confirm):
        res = {}
        if not self.user.exists(username):
            res['error'] = "user doesn't exists"
        elif not self.user.check_password(username, curr_pass):
            res['error'] = "Current password doesn't match"
        elif new_pass != new_pass_confirm:
            res['error'] = "New passwords doesn't match"
        elif new_pass == curr_pass:
            res['error'] = "New password can't be the same as current"
        else:
            self.user.edit_password(username, new_pass)
            res['result'] = "Password edit"
        return json.dumps(res)

    def user_edit_email(self, username, email):
        res = {}
        if not self.user.exists(username):
            res['error'] = "user doesn't exists"
        elif self.user.exists_email(email):
            res['error'] = "Email already used"
        else:
            self.user.edit_email(username, email)
            res['result'] = "Email edit"
        return json.dumps(res)

    def get_user_info(self, user_id):
        res = {}
        if self.user.exists_id(user_id):
            result = self.user.get_user_info(user_id)
        else:
            res['error'] = "user doesn't exists"
        res['result'] = result
        return json.dumps(result)

    def task_edit(self, id, title, begin, end, status, private):
        ret = {}
        if session['username']:
            if self.task.id_exist(id):
                self.task.edit_task(id, title, begin, end, status, private)
                ret['result'] = "update done"
            else:
                ret['error'] = "task id does not exist"
        else:
            ret['error'] = "you must be logged in"
        return json.dumps(ret)

    def task_create(self, title, begin, end, status, private):
        ret = {}
        if session['username']:
            if not "None" in title or not title == None:
                if self.task.create_task(session['id'], title, begin, end, status, private):
                    ret['result'] = "new task added"
                else:
                    ret['error'] = "internal error"
            else:
                ret['error'] = "internal error"
        else:
            ret['error'] = "you must be logged in"
        return json.dumps(ret)

    def task_delete(self, id):
        ret = {}
        if session['username']:
            if self.task.id_exist(id):
                if self.task.delete_task(id):
                    ret['result'] = "deleted"
                else:
                    ret['error'] = 'internal error'
            else:
                ret['error'] = "task id does not exist"
        else:
            ret['error'] = "you must be logged in"
        return json.dumps(ret)

    def task_get_by_id(self, task_id):
        ret = {}
        if self.task.id_exist(task_id):
            res = self.task.get_task_by_id(task_id)
            if res == None:
                ret['error'] = "internal error"
            else:
                if (datetime.datetime.now() >= res[2]):
                    res.append(True)
                else:
                    res.append(False)
                if (datetime.datetime.now() > res[3]):
                    res.append(True)
                else:
                    res.append(False)
                res.append((res[3] - datetime.datetime.now()).days)
                res.append(datetime.datetime.strftime(res[2], "%Y/%m/%d"))
                res.append(datetime.datetime.strftime(res[2], "%H:%M"))
                res.append(datetime.datetime.strftime(res[3], "%Y/%m/%d"))
                res.append(datetime.datetime.strftime(res[3], "%H:%M"))
                res[2] = datetime.datetime.strftime(res[2], "%A %d %B %Y, at %H:%M")
                res[3] = datetime.datetime.strftime(res[3], "%A %d %B %Y, at %H:%M")
                ret['result'] = res
        else:
            ret['error'] = "internal error"
        return json.dumps(ret)

    def task_get_all(self, user_id):
        ret = {}
        if self.user.exists_id(user_id):
            result = self.task.get_tasks_by_user_id(user_id)
            for i in range(0, len(result)):
                if (datetime.datetime.now() >= result[i][2]):
                    result[i].append(True)
                else:
                    result[i].append(False)
                if (datetime.datetime.now() > result[i][3]):
                    result[i].append(True)
                else:
                    result[i].append(False)
                result[i].append(datetime.datetime.strftime(result[i][2], "%Y/%m/%d"))
                result[i].append(datetime.datetime.strftime(result[i][2], "%H:%M"))
                result[i].append(datetime.datetime.strftime(result[i][3], "%Y/%m/%d"))
                result[i].append(datetime.datetime.strftime(result[i][3], "%H:%M"))
                result[i][2] = datetime.datetime.strftime(result[i][2], "%a %d %b %Y, at %H:%M")
                result[i][3] = datetime.datetime.strftime(result[i][3], "%a %d %b %Y, at %H:%M")
            ret['result'] = result
        else:
            ret['error'] = "user doesn't exists"
        return json.dumps(ret)

    def task_all_tasks(self):
        ret = {}
        result = self.task.get_all_tasks()
        for i in range(0, len(result)):
            start_tab = [
                datetime.datetime.strftime(result[i][2], "%d"),
                datetime.datetime.strftime(result[i][2], "%m"),
                datetime.datetime.strftime(result[i][2], "%Y"),
                datetime.datetime.strftime(result[i][2], "%H"),
                datetime.datetime.strftime(result[i][2], "%M")
            ]
            end_tab = [
                datetime.datetime.strftime(result[i][3], "%d"),
                datetime.datetime.strftime(result[i][3], "%m"),
                datetime.datetime.strftime(result[i][3], "%Y"),
                datetime.datetime.strftime(result[i][3], "%H"),
                datetime.datetime.strftime(result[i][3], "%M")
            ]
            result[i][2] = start_tab
            result[i][3] = end_tab
            if self.user.exists_id(result[i][5]):
                result[i][5] = self.user.get_user_info(result[i][5])[1]
        ret['result'] = result
        return json.dumps(ret)

    def get_number_tasks(self, api):
        count = 0
        tasks_wait = 0
        tasks_done = 0
        tasks_in_pr = 0
        tasks = api.task_get_all(session['id'])
        tasks = json.loads(tasks)
        count = len(tasks['result'])
        for task in tasks['result']:
            if task[4] == "not started":
                tasks_wait += 1
            elif task[4] == "in progress":
                tasks_in_pr += 1
            elif task[4] == "done":
                tasks_done += 1
        return [count, tasks_wait, tasks_done, tasks_in_pr]

    def get_number_tasks_in_progress(self, api, user_id):
        count = 0
        tasks_wait = 0
        tasks_done = 0
        tasks_in_pr = 0
        ret = {}
        if self.user.exists_id(user_id):
            result = self.task.get_tasks_by_user_id(user_id)
            for i in range(0, len(result)):
                if (datetime.datetime.now() >= result[i][2] and datetime.datetime.now() < result[i][3]):
                    if result[i][4] == "not started":
                        tasks_wait += 1
                    elif result[i][4] == "in progress":
                        tasks_in_pr += 1
                    elif result[i][4] == "done":
                        tasks_done += 1
                    count += 1
            ret['result'] = [count, tasks_wait, tasks_done, tasks_in_pr]
        else:
            ret['error'] = "user doesn't exists"
        return json.dumps(ret)

    def get_number_tasks_late(self, api, user_id):
        count = 0
        ret = {}
        if self.user.exists_id(user_id):
            result = self.task.get_tasks_by_user_id(user_id)
            for i in range(0, len(result)):
                if (datetime.datetime.now() >= result[i][3]):
                    if result[i][4] == "not started":
                        count += 1
                    elif result[i][4] == "in progress":
                        count += 1
            ret['result'] = count
        else:
            ret['error'] = "user doesn't exists"
        return json.dumps(ret)