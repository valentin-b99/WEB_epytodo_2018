##
## EPITECH PROJECT, 2018
## models.py
## File description:
## models
##

from app import *
from flask import *
import hashlib
import time
from datetime import datetime

class User(object):

    def __init__(self, app, conn):
        self.app = app
        self.conn = conn
        self.table = "user"
        self.fk = "user_has_task"

    def exists(self, username):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(1) FROM %s WHERE username = '%s'"
                % (self.table, username))
            exists = cur.fetchone()[0]
            cur.close()
            return True if exists == 1 else False
        except (Exception) as error:
            print(error)
            return True
        return True

    def exists_id(self, user_id):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(1) FROM %s WHERE user_id = '%s'"
                % (self.table, user_id))
            exists = cur.fetchone()[0]
            cur.close()
            return True if exists == 1 else False
        except (Exception) as error:
            print(error)
            return True
        return True

    def exists_email(self, email):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(1) FROM %s WHERE email = '%s'"
                % (self.table, email))
            exists = cur.fetchone()[0]
            cur.close()
            return True if exists == 1 else False
        except (Exception) as error:
            print(error)
            return True
        return True

    def create(self, username, password, email):
        p_hash = self.app.config['PASSWORD_HASH']
        try:
            hash = hashlib.sha512()
            hash.update(p_hash.encode())
            hash.update(password.encode())
            digest = hash.hexdigest()
            cur = self.conn.cursor()
            cur.execute("INSERT INTO %s (username, password, email) VALUES ('%s', '%s', '%s')"
                % (self.table, username, digest, email))
            self.conn.commit()
            cur.close()
        except (Exception) as error:
            print(error)

    def edit_password(self, username, password):
        p_hash = self.app.config['PASSWORD_HASH']
        try:
            hash = hashlib.sha512()
            hash.update(p_hash.encode())
            hash.update(password.encode())
            digest = hash.hexdigest()
            cur = self.conn.cursor()
            cur.execute("UPDATE %s SET password='%s' WHERE username='%s'"
                % (self.table, digest, username))
            self.conn.commit()
            cur.close()
        except (Exception) as error:
            print(error)

    def edit_email(self, username, email):
        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE %s SET email='%s' WHERE username='%s'"
                % (self.table, email, username))
            self.conn.commit()
            cur.close()
        except (Exception) as error:
            print(error)

    def get_id(self, username):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT user_id FROM %s WHERE username = '%s'"
                % (self.table, username))
            id = cur.fetchone()[0]
            cur.close()
            return id
        except (Exception) as err:
            print(err)
            return -1
        return -1

    def check_password(self, username, password):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT password FROM %s WHERE username = '%s'"
                % (self.table, username))
            pwd = cur.fetchone()[0]
            cur.close()
            p_hash = self.app.config['PASSWORD_HASH']
            hash = hashlib.sha512()
            hash.update(p_hash.encode())
            hash.update(password.encode())
            digest = hash.hexdigest()
            return True if digest == pwd else False
        except (Exception) as err:
            print(err)
            return False
        return False

    def get_user_info(self, user_id):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM %s WHERE user_id = '%d'"
                % (self.table, user_id))
            info = list(cur.fetchall()[0])
            cur.close()
            return info
        except (Exception) as err:
            print(err)
        return info


class Task(object):

    def __init__(self, app, conn):
        self.app = app
        self.conn = conn
        self.table = "task"
        self.fk = "user_has_task"

    def id_exist(self, id):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(1) FROM %s WHERE task_id = '%d'"
                % (self.table, id))
            exists = cur.fetchone()[0]
            cur.close()
            return True if exists == 1 else False
        except (Exception) as err:
            print(err)
        return True

    def get_task_by_id(self, id):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM %s WHERE task_id = '%d'"
                % (self.table, id))
            task = list(cur.fetchall()[0])
            cur.close()
            return task
        except (Exception) as err:
            print(err)
        return None

    def get_tasks_by_user_id(self, user_id):
        tasks = []
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT fk_task_id FROM %s WHERE fk_user_id = '%d'"
                % (self.fk, user_id))
            ids = list(cur.fetchall())
            cur.close()
            for id in ids:
                cur = self.conn.cursor()
                cur.execute("SELECT * FROM %s WHERE task_id = '%d'"
                    % (self.table, id[0]))
                task = list(cur.fetchall()[0])
                tasks.append(task)
                cur.close()
            return tasks
        except (Exception) as err:
            print(err)
        return tasks

    def get_all_tasks(self):
        tasks = []
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT * FROM %s" % (self.table))
            ids = list(cur.fetchall())
            cur.close()
            for id in ids:
                cur = self.conn.cursor()
                cur.execute("SELECT * FROM %s WHERE task_id = '%d'"
                    % (self.table, id[0]))
                task = list(cur.fetchall()[0])
                cur.close()
                if not task[5]:
                    cur = self.conn.cursor()
                    cur.execute("SELECT fk_user_id FROM %s WHERE fk_task_id = '%d'"
                        % (self.fk, id[0]))
                    task[5] = cur.fetchall()[0][0]
                    cur.close()
                    tasks.append(task)
            return tasks
        except (Exception) as err:
            print(err)
        return tasks

    def edit_task(self, task_id, title, begin, end, status, private):
        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE %s SET title='%s',begin='%s',end='%s',status='%s',private='%d' WHERE task_id='%d'"
                % (self.table, title, begin, end, status, private, task_id))
            self.conn.commit()
            cur.close()
        except (Exception) as err:
            print(err)

    def create_task(self, user_id, title, begin, end, status, private):
        try:
            cur = self.conn.cursor()
            print("title: %s\nbegin: %s\nend: %s\nstatus: %s\n" % (title, begin, end, status))
            cur.execute("INSERT INTO task (`begin`, `end`, `title`, `status`, `private`) VALUES ('%s','%s','%s','%s','%d')"
                % (begin, end, title, status, private))
            self.conn.commit()
            id = cur.lastrowid
            cur.close()
            if not id:
                return False
            cur = self.conn.cursor()
            cur.execute("INSERT INTO user_has_task (fk_user_id, fk_task_id) VALUES (%d, %d)"
                % (user_id, id))
            self.conn.commit()
            cur.close()
        except (Exception) as err:
            print(err)
            return False
        return True

    def delete_task(self, id):
        id = int(id)
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT COUNT(1) FROM %s WHERE fk_task_id = %d AND fk_user_id = %d"
                % (self.fk, id, session['id']))
            res = cur.fetchone()[0]
            cur.close()
            if res != 1:
                return False
            cur = self.conn.cursor()
            cur.execute("DELETE FROM %s WHERE fk_task_id = %d AND fk_user_id = %d"
                % (self.fk, id, session['id']))
            self.conn.commit()
            cur.close()
            cur = self.conn.cursor()
            cur.execute("DELETE FROM %s WHERE task_id = %d"
                % (self.table, id))
            self.conn.commit()
            cur.close()
        except (Exception) as err:
            print(err)
            return False
        return True
