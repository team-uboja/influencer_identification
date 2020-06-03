import mysql.connector as connector
import system_constants
import csv
import os
from werkzeug.security import generate_password_hash, check_password_hash
import flask

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
                    temp_list.append(row[0].decode('utf-8'))

                selector_filling_dict[distinct_column] = temp_list

            return flask.jsonify(selector_filling_dict)


        except connector.Error as error:
            print("Reading from DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")

    #items in restriction_dict must be elements from_, to, from_city, campaign_identifier, voted_for, age
    def getSelectedDataIncoming(self, restriction_dict):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)
            #TODO: this is bad style and should be changed at a later point
            insert_values = ()
            sql_prepared_statement = "select * from Incoming_messages WHERE "
            for key in restriction_dict.keys():
                if restriction_dict[key] == None:
                    sql_prepared_statement+= "'a'=%s AND "
                    insert_values+=('a',)
                else:
                    sql_prepared_statement+= key +"=%s AND "
                    insert_values+=(restriction_dict[key],)
            sql_prepared_statement += "'a'=%s"
            insert_values += ('a',)


            print(sql_prepared_statement)

            print('Insert values: ' + str(insert_values))
            cursor.execute(sql_prepared_statement, insert_values)
            print('Command executed')
            userdata = cursor.fetchall()
            print('Raw user data: ' + str(userdata))
            temp_list_for_json=[]
            for row in userdata:
                return_values = {}
                return_values['timestamp'] = str(row[1])
                return_values['from'] = row[2].decode('utf-8')
                return_values['to'] = row[3].decode('utf-8')
                return_values['cost'] = row[4].decode('utf-8')
                return_values['currency'] = row[5].decode('utf-8')
                return_values['content'] = row[6].decode('utf-8')
                return_values['from_city'] = row[13].decode('utf-8')
                return_values['from_zip'] = row[14].decode('utf-8')
                return_values['campaign_identifier'] = row[15].decode('utf-8')
                return_values['voted_for'] = row[16].decode('utf-8')
                return_values['age'] = str(row[17])
                print('Return values: ' + str(return_values))
                temp_list_for_json.append(return_values)



            return flask.jsonify(temp_list_for_json)


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

