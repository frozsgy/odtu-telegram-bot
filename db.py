import datetime
import logging
import os

import psycopg2


class DB:
    """Class for handling database methods. 

    Attributes:
        __verbose -- turns the verbose mode on, useful for debugging
        __location -- the absolute location for the bot
    """

    __verbose = False

    def __init__(self, verbose=False):
        self.__conn = psycopg2.connect(
            database=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host="db",
            port="5432",
        )
        self.__cursor = self.__conn.cursor()
        self.__verbose = verbose

    def __del__(self):
        self.__cursor.close()
        self.__conn.close()

    def get_token(self):
        """Fetches the Telegram Bot API Token from the database.
        """
        try:
            self.__cursor.execute(
                ''' SELECT data from settings WHERE id = 2 ''')
            return self.__cursor.fetchone()[0]
        except:
            logging.critical("Telegram Bot Secret is not in the database")
            exit()

    def get_offset(self):
        """Fetches the message offset from the database.
        """
        self.__cursor.execute(''' SELECT data from settings WHERE id = 1 ''')
        return self.__cursor.fetchone()[0]

    def update_offset(self, offset):
        """Updates the message offset according to the offset parameter.
        Returns boolean.
        """
        res = True
        try:
            self.__cursor.execute(''' UPDATE settings SET data = (%s) WHERE id = 1 ''', (offset,))
            logging.debug("Offset updated with %s" % offset)
        except:
            res = False
            logging.warning("Offset could not be updated")
        finally:
            self.__conn.commit()
            return res

    def check_if_user_exists(self, uid):
        """Checks if a user with the given user id exists.
        Returns boolean.
        """
        self.__cursor.execute(''' SELECT COUNT(*) from people WHERE uid = (%s) ''', (uid,))
        status = self.__cursor.fetchone()[0]
        if status == 1:
            return True
        else:
            return False

    def add_user(self, uid, fname, lname, uname):
        """Adds a user with the given id, first name, last name, and username to the database.
        Returns boolean.
        """
        res = True
        if self.check_if_user_exists(uid):
            logging.debug("User %s %s (%s) exists in the database" % (fname, lname, uname))
            return res
        else:
            try:
                self.__cursor.execute(''' INSERT into people VALUES((%s),(%s),(%s),(%s)) ''',
                                      (uid, fname, lname, uname))
                logging.debug("User %s %s (%s) created successfully" %
                              (fname, lname, uname))
            except:
                res = False
                logging.warning("User %s %s (%s) cannot be inserted" % (fname, lname, uname))
            finally:
                self.__conn.commit()
                return res

    def check_if_group_exists(self, gid):
        """Checks if a group with the given group id exists.
        Returns boolean.
        """
        self.__cursor.execute(''' SELECT COUNT(*) from groups WHERE gid = (%s) ''', (gid,))
        status = self.__cursor.fetchone()[0]
        if status == 1:
            return True
        else:
            return False

    def add_group(self, gid, title):
        """Adds a group with the given id, and title to the database.
        Returns boolean.
        """
        res = True
        if self.check_if_group_exists(gid):
            logging.debug("Group %s (%s) exists in the database" % (title, gid))
            return res
        else:
            try:
                self.__cursor.execute(''' INSERT into groups VALUES((%s),(%s)) ''', (gid, title))
                logging.debug("Group %s (%s) created successfully" % (title, gid))
            except:
                res = False
                logging.warning("Group %s (%s) cannot be inserted" % (title, gid))
            finally:
                self.__conn.commit()
                return res

    def log(self,
            uid,
            fname,
            lname,
            uname,
            mid,
            time,
            content,
            gid,
            gtitle='private'):
        """Logs the activity to the database.
        Returns boolean.
        """
        self.add_user(uid, fname, lname, uname)
        if gid != 0:
            self.add_group(gid, gtitle)
        res = True
        try:
            self.__cursor.execute(''' INSERT into logs VALUES((%s),(%s),(%s),(%s),(%s)) ''',
                                  (uid, mid, time, content, gid))
            logging.debug("Message %s logged successfully" % (mid))
        except:
            res = False
            logging.warning("Message %s cannot be logged" % (mid))
        finally:
            self.__conn.commit()
            return res

    def get_service_title(self, sid):
        """Fetches the service title with the given service id from the database.
        """
        try:
            self.__cursor.execute(''' SELECT name from services WHERE id = (%s) ''', (sid,))
            return self.__cursor.fetchone()[0]
        except:
            return False

    def check_service(self, uid, service):
        """Checks if a user with the given user id subscribed to the service.
        Returns boolean.
        """
        self.__cursor.execute(''' SELECT COUNT(*) from subscriptions WHERE uid = (%s) and service = (%s)''',
                              (uid, service))
        status = self.__cursor.fetchone()[0]
        if status == 1:
            return True
        else:
            return False

    def add_service(self, uid, service):
        """Adds a service subscription to the database.
        Returns boolean.
        """
        res = True
        if self.check_service(uid, service) is True:
            logging.debug("User %s already subscribed to service %s" % (uid, self.get_service_title(service)))
            return res
        try:
            self.__cursor.execute(''' INSERT into subscriptions VALUES((%s),(%s)) ''', (uid, service))
            logging.debug("User %s subscribed to %s service successfully" % (uid, self.get_service_title(service)))
        except:
            res = False
            logging.warning("User %s cannot subscribe to %s service" % (uid, self.get_service_title(service)))
        finally:
            self.__conn.commit()
            return res

    def remove_service(self, uid, service):
        """Removes a service subscription from the database.
        Returns boolean.
        """
        res = False
        if self.check_service(uid, service) is False:
            logging.debug("User %s has not subscribed to service %s" % (uid, self.get_service_title(service)))
            return res
        try:
            self.__cursor.execute(''' DELETE from subscriptions WHERE uid = (%s) and service = (%s) ''', (uid, service))
            res = True
            logging.debug("User %s unsubscribed from %s service successfully" % (uid, self.get_service_title(service)))
        except:
            logging.warning("User %s cannot unsubscribe to %s service" % (uid, self.get_service_title(service)))
        finally:
            self.__conn.commit()
            return res

    def check_if_service_sent_today(self, service):
        """Checks if the service blast has been sent today.
        Returns boolean.
        """
        now = datetime.datetime.now()
        today = str(now.year) + str(now.month) + str(now.day)
        self.__cursor.execute(''' SELECT COUNT(*) from servicedays WHERE id = (%s) and day = (%s) ''', (service, today))
        status = self.__cursor.fetchone()[0]
        if status == 1:
            return True
        else:
            return False

    def mark_service_sent_today(self, service):
        """Updates a service blast as sent today.
        Returns boolean.
        """
        now = datetime.datetime.now()
        today = str(now.year) + str(now.month) + str(now.day)
        res = True
        try:
            self.__cursor.execute(''' INSERT into servicedays VALUES((%s),(%s)) ''', (service, today))
            logging.debug("Service days for %s updated as sent" % self.get_service_title(service))
        except:
            res = False
            logging.warning("Service days could not be updated")
        finally:
            self.__conn.commit()
            return res

    def get_group_title(self, gid):
        """Fetches the group title with the given group id from the database.
        """
        if self.check_if_group_exists(gid):
            self.__cursor.execute(''' SELECT title from groups WHERE gid = (%s) ''', (gid,))
            return self.__cursor.fetchone()[0]
        else:
            return False

    def get_user(self, uid):
        """Fetches the user details with the given user id from the database.
        """
        if self.check_if_user_exists(uid):
            self.__cursor.execute(''' SELECT * from people WHERE uid = (%s) ''', (uid,))
            return self.__cursor.fetchone()
        else:
            return False

    def get_service_users(self, service):
        """Fetches the user ids subscribed to the given service from the database.
        """
        self.__cursor.execute(''' SELECT * from subscriptions WHERE service = (%s) ''', (service,))
        return self.__cursor.fetchall()

    def list_logs(self):
        """Prints all logs from the database.
        """
        self.__cursor.execute(''' SELECT * FROM logs ORDER by mid ''')
        logging.debug("Printing all logs")
        for i in self.__cursor.fetchall():
            logging.debug(i)

    def list_logs_from_user(self, uid):
        """Prints all logs with the given user id from the database.
        """
        if self.check_if_user_exists(uid):
            user = self.get_user(uid)
            self.__cursor.execute(''' SELECT * FROM logs WHERE uid = (%s) ORDER by mid ''', (uid,))
            logging.debug("Printing all logs from user %s %s (%s)" % (user[1], user[2], user[3]))
            for i in self.__cursor.fetchall():
                logging.debug(i)
        else:
            logging.debug("No user exists with User ID %s" % uid)

    def list_logs_with_user(self):
        """Prints all logs and the user details as a joined table from the database.
        """
        self.__cursor.execute(''' SELECT * FROM logs INNER JOIN people ON logs.uid = people.uid ORDER by mid ''')
        logging.debug("Printing all logs with user data")
        for i in self.__cursor.fetchall():
            logging.debug(i)

    def list_logs_from_group(self, gid):
        """Prints all logs with the given group id from the database.
        """
        if self.check_if_group_exists(gid):
            gtitle = self.get_group_title(gid)
            self.__cursor.execute(''' SELECT * FROM logs WHERE gid = (%s) ORDER by mid ''', (gid,))
            logging.debug("Printing all logs from group %s (%s)" % (gtitle, gid))
            for i in self.__cursor.fetchall():
                logging.debug(i)
        else:
            logging.debug("No group exists with Group ID %s" % gid)

    def list_db(self):
        """Prints all table names from the database.
        """
        self.__cursor.execute(''' SELECT name FROM sqlite_master WHERE type='table' ''')
        logging.debug("Printing all databases")
        for i in self.__cursor.fetchall():
            logging.debug(i)

    def list_users(self):
        """Prints all users from the database.
        """
        self.__cursor.execute(''' SELECT * FROM people ORDER by uid ''')
        logging.debug("Printing all users")
        for i in self.__cursor.fetchall():
            logging.debug(i)

    def list_groups(self):
        """Prints all groups from the database.
        """
        self.__cursor.execute(''' SELECT * FROM groups ORDER by gid ''')
        logging.debug("Printing all groups")
        for i in self.__cursor.fetchall():
            logging.debug(i)
