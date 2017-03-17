import sqlite3 as sql
from datetime import datetime as dt


class DatabaseHandler:

    def __init__(self):
        self._users_table="users"
        self._credentials_table="credentials"
        self._items_table = "items_table"
        self._entries_table = "entries"
        self._dbName = "sort-bot.db"

        self._check_for_integrity()

    def _execute_SELECT(self, table, conds, cols=["*"],limit=None, order=None, groupBy=None):
        """
                    function that executes a SELECT query
        :param cols:        the list of columns we want. default ['*']
        :param table:       the table name
        :param conds:       the conditions, as a string
        :param limit:       how many results to return. default None
        :param order:       the way to order the results. default None
        :param groupBy:     the way to group the results. default None
        :return:            the list representing the results of the query
        """

        cols_string = ",".join(cols)
        query = "SELECT " + cols_string + " FROM " + str(table)

        if conds!= None:
            query += " WHERE " + str(conds)

        if order != None:
            query += " ORDER BY " + str(order)

        if groupBy != None:
            query += " GROUP BY " + str(groupBy)

        if limit != None:
            query += " LIMIT " + str(limit)

        print(query)
        con = sql.connect(self._dbName)
        cur = con.cursor()
        print(query)
        cur.execute(query)
        results = list(set(cur.fetchall()))
        con.commit()
        con.close()

        return results

    def _execute_query(self, query, *args):
        """
            Function that executes a given query, except SELECT queries
        :param query:       the query to be executed
        :param args:        the arguments to be inserted
        :return:
        """

        con = sql.connect(self._dbName)
        cur = con.cursor()
        print(query)
        cur.execute(query, args)
        con.commit()
        con.close()

    def _check_for_integrity(self):
        """
            Function that checks the database for integrity and repairs any necessary errors
        :return: -
        """

        #(1) For the credentials table

        #query = "DROP TABLE credentials"
        #self._execute_query(query)

        query = "CREATE TABLE IF NOT EXISTS " \
                "credentials (" \
                    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "userID INT," \
                    "username VARCHAR(50)," \
                    "pass VARCHAR(50)" \
                ")"

        self._execute_query(query)

        #query = "DROP TABLE users"
        #self._execute_query(query)

        query = ""
        # (2) For the users table
        query = "CREATE TABLE IF NOT EXISTS " \
                "users (" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "firstName VARCHAR(50)," \
                "lastName VARCHAR(50)," \
                "email VARCHAR(50)" \
                ")"

        self._execute_query(query)

        query = ""

        query = "DROP TABLE items"
        self._execute_query(query)

        #(3) For the items table
        query = "CREATE TABLE IF NOT EXISTS " \
                "items (" \
                    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "itemName VARCHAR(50)," \
                    "points INT" \
                ")"

        self._execute_query(query)
        query = ""


        query = "INSERT INTO items(itemName, points)" \
                "VALUES " \
                    "('plastic', 3)," \
                    "('carboard', 2)," \
                    "('paper', 1), " \
                    "('mixed', 0)" \

        self._execute_query(query)
        query = ""

        # For the entries table

        query = "CREATE TABLE IF NOT EXISTS " \
                "entries (" \
                    "id INTEGER PRIMARY KEY AUTOINCREMENT,"\
                    "userID INT,"\
                    "itemID INT, " \
                    "'date' DATE," \
                    "FOREIGN KEY(userID) REFERENCES users(id)," \
                    "FOREIGN KEY(itemID) REFERENCES items(id)" \
                ")"

        self._execute_query(query)

    def check_signin(self, userName, password):
        """
            Function that checks if a given username and password are valid
        :param userName:        the username we want to check
        :param password:
        :return:
        """
        conditions = 'username="' + str(userName) + '" AND pass="' + str(password) + '"'

        found_ids = self._execute_SELECT(self._credentials_table,
                                         conditions,
                                         cols=['userID'])

        result = dict()
        if len(found_ids) != 0:
            result['success'] = True
            result['id'] = found_ids[0][0]
        else:
            result['success'] = False
            result['id'] = -1

        return result

    def signup(self, user, password, first_name, last_name, email):
        """

        :param user:            The username we want to insert
        :param password:        The password we want to insert
        :param first_name:      The 1st name
        :param last_name:       The last name
        :param email:           The email
        :return:                a dictionary with the required result
        """
        insert_query2 = "INSERT INTO " + self._credentials_table + '(username, pass, userID)' + \
            'VALUES (?, ?, ?)'

        insert_query1 = "INSERT INTO " + self._users_table + '(firstName, lastName, email)' + \
            'VALUES(?, ?, ?)'

        select_condition_2 = 'firstName="' + str(first_name) + '" AND lastName= "' + str(last_name) + \
            '" AND email="' + str(email) + '"'

        select_condition_1 = 'username="' + str(user) + '"'
        try:
            already_existent = self._execute_SELECT(self._credentials_table, select_condition_1)
            if len(already_existent) != 0:
                # we already have a user with that username
                result = {
                    "success": False,
                    "comments": "duplicate"
                }
                print(already_existent)
                return result

            self._execute_query(insert_query1, first_name, last_name, email)

            id = self._execute_SELECT(self._users_table,
                                      select_condition_2,
                                      cols=['id'],
                                      order="id DESC",
                                      limit=1)

            self._execute_query(insert_query2, user, password, id[0][0])

            result = {
                "success": True,
                "comments": ""
            }
            return result

        except:
            # Let's delete the data we tried to insert into the tables

            query = "DELETE FROM " + self._credentials_table + " WHERE " + select_condition_1
            self._execute_query(query)

            query = "DELETE FROM " + self._users_table + " WHERE " + select_condition_2
            self._execute_query(query)

            result = {
                "success": False,
                "comments": ""
            }

            return result

    def insert_new_entry(self, userID, itemID):
        """
            Method that adds a new entry to our database
        :param userID:          the id of the user that adds the entry
        :param itemID:          the id of the item represented by the entry
        :return:                -
        """
        insert_query = "INSERT INTO " + self._entries_table + "(userID, itemID, date)" + \
            "VALUES(?, ?, ?)"

        time = dt.now()
        try:
            self._execute_query(insert_query, userID, itemID, time)

            result = {
                "success": True,
                "comments": ""
            }

            return result
        except:
            result = {
                "success": False,
                "comments": ""
            }
            return result

    def _get_last_point(self, userID):
        """
            Function that returns the last points that the user received
        :param userID:      the id for the user we want
        :return:            the last number of points
        """

        query = "SELECT t.points FROM" \
                    "(SELECT it.id AS id, it.points AS points FROM " \
                        "entries AS e INNER JOIN " \
                        "items as it ON e.itemID = it.id" \
                        " WHERE e.userID=" + str(userID) + \
                    ") AS t " \
                "ORDER BY t.id DESC " \
                "LIMIT 1"

        con = sql.connect(self._dbName)
        cur = con.cursor()
        cur.execute(query)
        result = list(set(cur.fetchall()))
        con.commit()
        con.close()

        return result[0][0]

    def _get_points(self, userID):
        """
            Function that returns the total points for a specific user
        :param userID:          the id of the user we want
        :return:                the total
        """

        query = "SELECT SUM(t.p) FROM" \
                    "(SELECT it.points AS p FROM " \
                        "entries AS e INNER JOIN " \
                        "items as it ON e.itemID = it.id" \
                    " WHERE e.userID=" + str(userID) + \
                    ") AS t"

        print(query)
        con = sql.connect(self._dbName)
        cur = con.cursor()
        cur.execute(query)
        result = list(set(cur.fetchall()))
        con.commit()
        con.close()

        return result[0][0]

    def _get_history(self, userID):
        """
            Function that returns the last 10 entries from the user's log
        :param userID:      the id of the user we want
        :return:            the history in the required format
        """
        query = "SELECT it.itemName, e.date, it.points " \
                    "FROM( SELECT * " \
                                "FROM entries " \
                            "WHERE userID=" + str(userID) + \
                         ") AS e " \
                    "INNER JOIN items AS it " \
                         "ON e.itemID = it.id " \
                "ORDER BY date DESC " \
                "LIMIT 10"
        print(query)
        con = sql.connect(self._dbName)
        cur = con.cursor()
        cur.execute(query)
        raw = list(set(cur.fetchall()))
        con.commit()
        con.close()

        result = list()

        for entry in raw:
            new_entry = dict()
            new_entry["item"] = entry[0]
            new_entry["date"] = entry[1]
            new_entry["points"] = entry[2]
            result.append(new_entry)

        return result


    def get_general_data(self, userID):
        """
            The Method that returns the general data for a given user
        :param userID:          the user we want the data for
        :return:                a dictionary in the required format
        """
        # (1) getting the first and last name of the user
        first_last = self._execute_SELECT(table=self._users_table,
                                          conds="id=" + str(userID),
                                          cols=['firstName', 'lastName'])

        result = dict()
        result['first_name'] = first_last[0][0]
        result['last_name'] = first_last[0][1]

        # (2) getting the total number of points of the user
        result['points'] = dict()
        result['points']['total'] = self._get_points(userID)

        # (3) getting the last points that the user got
        result['points']['last'] = self._get_last_point(userID)

        # (4) getting the history
        result['history'] = self._get_history(userID)

        return result


