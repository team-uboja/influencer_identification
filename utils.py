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

    def getAllTableData(self):
        try:
                connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME,
                                               password=system_constants.AMAZON_RDS_DB1_PASSWORD \
                                               , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com',
                                               port='3306', database='Ubuntu')

                cursor = connection.cursor(prepared=True)
                # TODO: this is bad style and should be changed at a later point
                insert_values = ()
                sql_prepared_statement = "select * from Incoming_messages"

                print(sql_prepared_statement)

                print('Insert values: ' + str(insert_values))
                cursor.execute(sql_prepared_statement, insert_values)
                print('Command executed')
                userdata = cursor.fetchall()
                print('Raw user data: ' + str(userdata))
                return_values = {}
                return_values['timestamp'] = []
                return_values['from'] = []
                return_values['to'] = []
                return_values['cost'] = []
                return_values['currency'] = []
                return_values['content'] = []
                return_values['from_city'] = []
                return_values['from_zip'] = []
                return_values['campaign_identifier'] = []
                return_values['voted_for'] = []
                return_values['age'] = []
                for row in userdata:

                    return_values['timestamp'].append(str(row[1]))
                    return_values['from'].append(row[2].decode('utf-8'))
                    return_values['to'].append(row[3].decode('utf-8'))
                    return_values['cost'].append(row[4].decode('utf-8'))
                    return_values['currency'].append(row[5].decode('utf-8'))
                    return_values['content'].append(row[6].decode('utf-8'))
                    return_values['from_city'].append(row[13].decode('utf-8'))
                    return_values['from_zip'].append(row[14].decode('utf-8'))
                    return_values['campaign_identifier'].append(row[15].decode('utf-8'))
                    return_values['voted_for'].append(row[16].decode('utf-8'))
                    return_values['age'].append(str(row[17]))
                    print('Return values: ' + str(return_values))


                return flask.jsonify(return_values)

        except connector.Error as error:
            print("Writing into DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")

    def fillFilters(self):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME,
                                           password=system_constants.AMAZON_RDS_DB1_PASSWORD \
                                           , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com',
                                           port='3306', database='Ubuntu')

            cursor = connection.cursor(prepared=True)
            # TODO: this is bad style and should be changed at a later point
            filter_keys =['from_', 'from_city', 'campaign_identifier', 'voted_for']
            filter_values={}
            for key in filter_keys:

                sql_prepared_statement = "select distinct " + key +" from Incoming_messages"

                cursor.execute(sql_prepared_statement)

                userdata = cursor.fetchall()
                temp_list=[]
                for row in userdata:
                    temp_list.append(row[0].decode('utf-8'))
                filter_values[key]=temp_list

            return flask.jsonify(filter_values)

        except connector.Error as error:
            print("Writing into DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")



    # items in restriction_dict must be elements from_, to, from_city, campaign_identifier, voted_for, age

    def getSelectedDataIncoming(self, restriction_dict):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)
            #TODO: this is bad style and should be changed at a later point
            insert_values = ()
            sql_prepared_statement = "select * from Incoming_messages WHERE "
            for key in restriction_dict.keys():
                if restriction_dict[key] == 'ALL':
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
                return_values = []
                return_values.append(str(row[1]))
                return_values.append(row[2].decode('utf-8'))
                return_values.append(row[3].decode('utf-8'))
                return_values.append(row[4].decode('utf-8'))
                return_values.append(row[5].decode('utf-8'))
                return_values.append(row[6].decode('utf-8'))
                return_values.append(row[13].decode('utf-8'))
                return_values.append(row[14].decode('utf-8'))
                return_values.append(row[15].decode('utf-8'))
                return_values.append(row[16].decode('utf-8'))
                return_values.append(str(row[17]))
                print('Return values: ' + str(return_values))
                temp_list_for_json.append(return_values)



            return temp_list_for_json


        except connector.Error as error:
            print("Reading from DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")


    def getDownloadFile(self, restriction_dict):

        data_list = self.getSelectedDataIncoming(restriction_dict)
        with open('temp.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in data_list:
                csv_writer.writerow(row)
        return csvfile


    def getUserInfo(self, username):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')
            print(username)

            cursor=connection.cursor(prepared=True)
            insert_values = (username,)
            #TODO: this is bad style and should be changed at a later point
            sql_prepared_statement = "select username, mail, first_name, last_name, organization, city, \
             country from Login_credentials WHERE username = %s"


            cursor.execute(sql_prepared_statement, insert_values)
            row = cursor.fetchall()[0]

            return_values = {}
            return_values['username'] = row[0].decode('utf-8')
            return_values['email'] = row[1].decode('utf-8')
            return_values['first_name'] = row[2].decode('utf-8')
            return_values['last_name'] = row[3].decode('utf-8')
            return_values['organization'] = row[4].decode('utf-8')
            return_values['city'] = row[5].decode('utf-8')
            return_values['country'] = row[6].decode('utf-8')

            return flask.jsonify(return_values)


        except connector.Error as error:
            print("Reading from credential DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")

    def updateUserInfo(self, organization, username, mail, first_name, last_name, city, country):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')
            print(username)

            cursor=connection.cursor(prepared=True)
            insert_values = (mail, first_name,last_name, organization, city, country, username)
            print(insert_values)
            #TODO: this is bad style and should be changed at a later point
            sql_prepared_statement = "UPDATE Login_credentials SET mail=%s, first_name=%s, last_name=%s, organization=%s, city=%s, \
             country=%s WHERE username = %s"
            print(sql_prepared_statement)
            cursor.execute(sql_prepared_statement, insert_values)
            connection.commit()

            return True


        except connector.Error as error:
            print("Updating credential DB failed")
            print(error)
            return False

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")

    def filteredBarChartData(self, restriction_dict):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME,
                                           password=system_constants.AMAZON_RDS_DB1_PASSWORD \
                                           , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com',
                                           port='3306', database='Ubuntu')

            cursor = connection.cursor(prepared=True)
            # TODO: this is bad style and should be changed at a later point


            sql_prepared_statement = "select distinct voted_for from Incoming_messages"

            cursor.execute(sql_prepared_statement)

            userdata = cursor.fetchall()
            print(userdata)
            influencer_dict={}
            #get vote count
            for row in userdata:
                voted_for=row[0].decode('utf-8')
                insert_values=(voted_for,)
                sql_prepared_statement = "select count(*) from Incoming_messages WHERE voted_for=%s AND "

                for key in restriction_dict.keys():
                    if restriction_dict[key] == 'ALL':
                        sql_prepared_statement += "'a'=%s AND "
                        insert_values += ('a',)
                    else:
                        sql_prepared_statement += key + "=%s AND "
                        insert_values += (restriction_dict[key],)
                sql_prepared_statement += "'a'=%s"
                insert_values += ('a',)

                cursor.execute(sql_prepared_statement, insert_values)
                count_data=cursor.fetchall()[0]
                influencer_dict[voted_for]=count_data[0]

            sorted_ranking = sorted(influencer_dict.items(), key=lambda x: x[1], reverse=True)
            print(sorted_ranking)
            influencer_dict={}
            for element in sorted_ranking:
                influencer_dict[element[0]]=element[1]
            print(influencer_dict)
            return flask.jsonify(influencer_dict)

        except connector.Error as error:
            print("Reading from incoming message DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")


    def filteredTimeSeriesData(self, restriction_dict):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)

            #TODO: this is bad style and should be changed at a later point
            #TODO: Fix hack to group by timestamp here (and not on the UI)
            insert_values = ()
            sql_prepared_statement = "select timestamp from Incoming_messages WHERE "
            for key in restriction_dict.keys():
                if restriction_dict[key] == 'ALL':
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
                temp_list_for_json.append(str(row[0]))

            return flask.jsonify(temp_list_for_json)


        except connector.Error as error:
            print("Reading from DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")


    def writeCampaignInfo(self, organization, username, mail, geography, collaborators, description, campaign_identifier):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')
            print(username)

            cursor=connection.cursor(prepared=True)
            insert_values = (organization, username, mail, geography, collaborators, description, campaign_identifier)
            print(insert_values)
            #TODO: this is bad style and should be changed at a later point
            sql_prepared_statement = "insert into Campaign (organization, username, mail, geography, collaborators, description, \
            campaign_identifier) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            print(sql_prepared_statement)
            cursor.execute(sql_prepared_statement, insert_values)
            connection.commit()

            return True


        except connector.Error as error:
            print("Writing into campaign DB failed")
            print(error)
            return False

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")


    def check_password(self, username, password):
        return check_password_hash(self.readFromUserDB(username)['password'], password)

