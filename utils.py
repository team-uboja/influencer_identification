import mysql.connector as connector
import system_constants
import csv
import os
from werkzeug.security import generate_password_hash, check_password_hash

class utils:

    def writeIntoUserDB(self, username, password, mail):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)

            #important: don't put variable table name into statement other than through prepared statements

            sql_prepared_statement = """INSERT INTO Login_credentials (username, password, mail) VALUES  (%s,%s,%s)"""
            insert_values = (username, generate_password_hash(password), mail)

            cursor.execute(sql_prepared_statement, insert_values)
            connection.commit()
            print('Added user to database')

            return True

        except connector.Error as error:
            print("Writing message into Credential DB failed")
            print(error)
            return False

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")


    def readFromUserDB(self, username):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)
            sql_prepared_statement = """select id,username,password,mail from Login_credentials where username = %s"""
            insert_values=(username,)

            cursor.execute(sql_prepared_statement, insert_values)
            userdata = cursor.fetchall()[0]

            clean_return_data ={}
            clean_return_data['id'] = userdata[0]
            clean_return_data['username'] = userdata[1].decode('utf-8')
            clean_return_data['password'] = userdata[2].decode('utf-8')
            clean_return_data['mail'] = userdata[3].decode('utf-8')

            return clean_return_data


        except connector.Error as error:
            print("Reading from DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")

    def readFromUserDBByID(self, user_id):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)
            sql_prepared_statement = """select id,username,password,mail from Login_credentials where id = %s"""
            insert_values=(user_id,)



            cursor.execute(sql_prepared_statement, insert_values)
            userdata = cursor.fetchall()[0]

            clean_return_data ={}
            clean_return_data['id'] = userdata[0]
            clean_return_data['username'] = userdata[1].decode('utf-8')
            clean_return_data['password'] = userdata[2].decode('utf-8')
            clean_return_data['mail'] = userdata[3].decode('utf-8')

            return clean_return_data


        except connector.Error as error:
            print("Reading from DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")


    def check_password(self, username, password):
        return check_password_hash(self.readFromUserDB(username)['password'], password)

