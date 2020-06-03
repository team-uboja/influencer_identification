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

    def fillSelectorsIncoming(self):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)
            selector_filling_dict={}
            listForDistinctColumns =['from_', 'to', 'from_city', 'campaign_identifier', 'voted_for', 'age']
            for distinct_column in listForDistinctColumns:
                sql_prepared_statement = """select distinct %s from Incoming_messages"""
                insert_values=(distinct_column,)

                cursor.execute(sql_prepared_statement, insert_values)
                userdata = cursor.fetchall()

                temp_list=[]
                for row in userdata:
                    temp_list.append(row[0].decoder('utf-8'))

                selector_filling_dict[distinct_column] = temp_list

            return selector_filling_dict


        except connector.Error as error:
            print("Reading from DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")

    #items in restriction_dict must be orders from_, to, from_city, campaign_identifier, voted_for, age
    def fillGetSelectedData(self, restriction_dict):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)
            sql_prepared_statement = """select * from Incoming_messages WHERE %s = %s AND %s = %s AND %s = %s \
                            AND %s = %s AND %s = %s"""

            for key in restriction_dict.keys:
                if

                insert_values=(distinct_column,)

                cursor.execute(sql_prepared_statement, insert_values)
                userdata = cursor.fetchall()

                temp_list=[]
                for row in userdata:
                    temp_list.append(row[0].decoder('utf-8'))

                selector_filling_dict[distinct_column] = temp_list

            return selector_filling_dict


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

