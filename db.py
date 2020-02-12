import sqlite3
import os

class DB():
    """Class for handling database methods. 

    Attributes:
        __verbose -- turns the verbose mode on, useful for debugging
        __location -- the absolute location for the bot
    """

    __verbose = False
    __location = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, verbose = False):
        self.__conn = sqlite3.connect(self.__location + '/bot.db')
        self.__cursor = self.__conn.cursor()
        self.__verbose = verbose

    def __del__(self):
        self.__conn.close()

    def createDB(self, secret):
        """Creates the database and tables. This method should be called only during the installation.
        """
        try :
            self.__cursor.execute(''' CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, data varchar) ''')
            self.__cursor.execute(''' CREATE TABLE IF NOT EXISTS people (uid varchar NOT NULL UNIQUE , fname text, lname text, uname text) ''')
            self.__cursor.execute(''' CREATE TABLE IF NOT EXISTS logs (uid varchar, mid varchar NOT NULL UNIQUE, time date, content text, gid varchar, FOREIGN KEY(uid) REFERENCES people(uid), FOREIGN KEY(gid) REFERENCES groups(gid)) ''')
            self.__cursor.execute(''' CREATE TABLE IF NOT EXISTS groups (gid varchar NOT NULL UNIQUE, title text) ''')
            self.__cursor.execute(''' INSERT into groups VALUES(0, 'private') ''')
            self.__cursor.execute(''' INSERT into settings VALUES(NULL, 0) ''')
            self.__cursor.execute(''' INSERT into settings VALUES(NULL, ?) ''', (secret,))
        except:
            print('Cannot create DB')
        finally:
            self.__conn.commit()

    def getToken(self):
        """Fetches the Telegram Bot API Token from the database.
        """
        try:
            self.__cursor.execute(''' SELECT data from settings WHERE id = 2 ''')
            return self.__cursor.fetchone()[0]
        except:
            print("Telegram Bot Secret is not in the database")
            exit()
            return False

    def getOffset(self):
        """Fetches the message offset from the database.
        """
        self.__cursor.execute(''' SELECT data from settings WHERE id = 1 ''')
        return self.__cursor.fetchone()[0]

    def updateOffset(self, offset):
        """Updates the message offset according to the offset parameter.
        """
        res = True
        try:
            self.__cursor.execute(''' UPDATE settings SET data = ? WHERE id = 1 ''', (offset,))
            if self.__verbose:
                print("Offset updated with %s" %offset)
        except:
            res = False
            print("Offset could not be updated")
        finally:
            self.__conn.commit()
            return res

    def checkUserExists(self, uid):
        """Checks if a user with the given user id exists.
        Returns boolean.
        """
        self.__cursor.execute(''' SELECT COUNT(*) from people WHERE uid = ? ''', (uid,))
        status = self.__cursor.fetchone()[0]
        if status == 1:
            return True
        else :
            return False

    def addUser(self, uid, fname, lname, uname):
        """Adds a user with the given id, first name, last name, and username to the database.
        Returns boolean.
        """
        res = True
        if self.checkUserExists(uid):
            if self.__verbose:
                print("User %s %s (%s) exists in the database" % (fname, lname, uname))
            return res
        else :
            try:
                self.__cursor.execute(''' INSERT into people VALUES(?,?,?,?) ''', (uid, fname, lname, uname))
                if self.__verbose:
                    print("User %s %s (%s) created succesfully" % (fname, lname, uname))
            except:
                res = False
                if self.__verbose:
                    print("User %s %s (%s) cannot be inserted" % (fname, lname, uname))
            finally:
                self.__conn.commit()
                return res

    def checkGroupExists(self, gid):
        """Checks if a group with the given group id exists.
        Returns boolean.
        """
        self.__cursor.execute(''' SELECT COUNT(*) from groups WHERE gid = ? ''', (gid,))
        status = self.__cursor.fetchone()[0]
        if status == 1:
            return True
        else :
            return False

    def addGroup(self, gid, title):
        """Adds a group with the given id, and title to the database.
        Returns boolean.
        """
        res = True
        if self.checkGroupExists(gid):
            if self.__verbose:
                print("Group %s (%s) exists in the database" % (title, gid))
            return res
        else :
            try:
                self.__cursor.execute(''' INSERT into groups VALUES(?,?) ''', (gid, title))
                if self.__verbose:
                    print("Group %s (%s) created succesfully" % (title, gid))
            except:
                res = False
                if self.__verbose:
                    print("Group %s (%s) cannot be inserted" % (title, gid))
            finally:
                self.__conn.commit()
                return res

    def log(self, uid, fname, lname, uname, mid, time, content, gid, gtitle = 'private'):
        """Logs the activity to the database.
        Returns boolean.
        """
        self.addUser(uid, fname, lname, uname)
        if gid != 0:
            self.addGroup(gid, gtitle)
        res = True
        try:
            self.__cursor.execute(''' INSERT into logs VALUES(?,?,?,?,?) ''', (uid, mid, time, content, gid))
            if self.__verbose:
                print("Message %s logged succesfully" % (mid))
        except:
            res = False
            if self.__verbose:
                print("Message %s cannot be logged" % (mid))
        finally:
            self.__conn.commit()
            return res

    def getGroupTitle(self, gid):
        """Fetches the group title with the given group id from the database.
        """
        if self.checkGroupExists(gid):
            self.__cursor.execute(''' SELECT title from groups WHERE gid = ? ''', (gid,))
            return self.__cursor.fetchone()[0]
        else :
            return False

    def getUser(self, uid):
        """Fetches the user details with the given user id from the database.
        """
        if self.checkUserExists(uid):
            self.__cursor.execute(''' SELECT * from people WHERE uid = ? ''', (uid,))
            return self.__cursor.fetchone()
        else :
            return False

    def listLogs(self):
        """Prints all logs from the database.
        """
        self.__cursor.execute(''' SELECT * FROM logs ORDER by mid ''')
        print("Printing all logs")
        for i  in self.__cursor.fetchall():
            print(i)

    def listLogsFromUser(self, uid):
        """Prints all logs with the given user id from the database.
        """
        if self.checkUserExists(uid):
            user = self.getUser(uid)
            self.__cursor.execute(''' SELECT * FROM logs WHERE uid = ? ORDER by mid ''', (uid,))
            print("Printing all logs from user %s %s (%s)" % (user[1], user[2], user[3]))
            for i in self.__cursor.fetchall():
                print(i)
        else :
            print("No user exists with User ID %s" % uid)

    def listLogsWithUser(self):
        """Prints all logs and the user details as a joined table from the database.
        """
        self.__cursor.execute(''' SELECT * FROM logs INNER JOIN people ON logs.uid = people.uid ORDER by mid ''')
        print("Printing all logs with user data")
        for i  in self.__cursor.fetchall():
            print(i)

    def listLogsFromGroup(self, gid):
        """Prints all logs with the given group id from the database.
        """
        if self.checkGroupExists(gid):
            gtitle = self.getGroupTitle(gid)
            self.__cursor.execute(''' SELECT * FROM logs WHERE gid = ? ORDER by mid ''', (gid,))
            print("Printing all logs from group %s (%s)" % (gtitle, gid))
            for i in self.__cursor.fetchall():
                print(i)
        else :
            print("No group exists with Group ID %s" % gid)

    def listDB(self):
        """Prints all table names from the database.
        """
        self.__cursor.execute(''' SELECT name FROM sqlite_master WHERE type='table' ''')
        print("Printing all databases")
        for i  in self.__cursor.fetchall():
            print(i)

    def listUsers(self):
        """Prints all users from the database.
        """
        self.__cursor.execute(''' SELECT * FROM people ORDER by uid ''')
        print("Printing all users")
        for i  in self.__cursor.fetchall():
            print(i)

    def listGroups(self):
        """Prints all groups from the database.
        """
        self.__cursor.execute(''' SELECT * FROM groups ORDER by gid ''')
        print("Printing all groups")
        for i  in self.__cursor.fetchall():
            print(i)
