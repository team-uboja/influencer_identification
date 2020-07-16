import mysql.connector as connector
import system_constants
import csv
import os
from werkzeug.security import generate_password_hash, check_password_hash
import flask

import nltk
import re
import nltk
from nltk.corpus import stopwords
import hashlib
import copy


class utils:

    def __init__(self):
        self.number_alias_mapping={}
        #self.setupNLTK()

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

    #get alias for phone number, if alias does not exist, insert new alias

    def getAliasFromDB(self, phone_number):
        if phone_number in self.number_alias_mapping:
            return self.number_alias_mapping[phone_number]
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)
            sql_prepared_statement = """select phone_number, alias from Number_alias_mapping"""


            cursor.execute(sql_prepared_statement)
            userdata = cursor.fetchall()
            for row in userdata:
                self.number_alias_mapping[row[0].decode('utf-8')] = row[1].decode('utf-8')

            if phone_number in self.number_alias_mapping:
                return self.number_alias_mapping[phone_number]
            else:
                return self.createAlias(phone_number)



        except connector.Error as error:
            print("Reading from DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")



    #get alias for phone number, if alias does not exist, insert new alias

    def getPhoneNumberFromAliasDB(self, alias):

        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)
            sql_prepared_statement = """select phone_number, alias from Number_alias_mapping WHERE alias=%s"""
            insert_values=(alias,)

            cursor.execute(sql_prepared_statement, insert_values)
            userdata = cursor.fetchall()
            for row in userdata:
                return (row[0].decode('utf-8'))

            if phone_number in self.number_alias_mapping:
                return self.number_alias_mapping[phone_number]
            else:
                return self.createAlias(phone_number)



        except connector.Error as error:
            print("Reading from DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")




    def createAlias(self, phone_number):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)

            #important: don't put variable table name into statement other than through prepared statements

            sql_prepared_statement = """INSERT INTO Number_alias_mapping (phone_number, alias) VALUES  (%s,%s)"""
            hash = hashlib.sha3_512(bytes(phone_number,'utf-8'))
            print(hash.digest_size)
            alias=hash.hexdigest()[:10]
            insert_values = (phone_number, alias)

            cursor.execute(sql_prepared_statement, insert_values)
            connection.commit()
            print('Added mapping to database')

            return alias

        except connector.Error as error:
            print("Writing message into mapping DB failed")
            print(error)
            return False

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


                cursor.execute(sql_prepared_statement, insert_values)
                print('Command executed')
                userdata = cursor.fetchall()
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
        print("fillFilters called")
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
        print('getSelectedDataIncoming called')
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



            cursor.execute(sql_prepared_statement, insert_values)
            print('Command executed')
            userdata = cursor.fetchall()
            temp_list_for_json=[]
            #index 2 is from, index 3 is to
            index_list=[1,2,3,4,5,6,13,14,15,16,17]
            for row in userdata:
                return_values = []
                for index in index_list:
                    try:
                        if index == 2 or index == 3 or index == 16:
                            return_values.append(self.getAliasFromDB(row[index].decode('utf-8')))
                        elif index == 6:
                            temp_string = row[index].decode('utf-8').replace(row[16].decode('utf-8'), self.getAliasFromDB(row[16].decode('utf-8')))
                            #print("tempstring before: " + str(temp_string))
                            #names = self.extract_names(copy.deepcopy(temp_string))


                            #for name in names:

                                #temp_string = temp_string.replace(name, self.getAliasFromDB(name))
                            return_values.append(temp_string)
                            #print("tempstring after: " + str(temp_string))
                        else:
                            return_values.append(row[index].decode('utf-8'))
                    except AttributeError as e:
                        if index == 6:
                            print(e)
                        return_values.append(str(row[index]))
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


    def getCampaignIdentifierFromNumber(self, phone_number):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)
            insert_values = (phone_number,)
            print('Insert values:' + str(insert_values))
            #TODO: this is bad style and should be changed at a later point
            sql_prepared_statement = "select campaign_identifier from Outgoing_messages where to_=%s order by timestamp desc"


            cursor.execute(sql_prepared_statement, insert_values)
            data = cursor.fetchall()
            row = data[0]
            print('All data: ' + str(data))
            print('Row: ' + str(row[0]))
            return row[0].decode('utf-8')


        except connector.Error as error:
            print("Reading from Outgoing Message DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")

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
            #TODO: this is bad style and should be changed at a later point
            sql_prepared_statement = "UPDATE Login_credentials SET mail=%s, first_name=%s, last_name=%s, organization=%s, city=%s, \
             country=%s WHERE username = %s"
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
        print('filteredBarChartData called')
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
            influencer_dict={}
            i=0
            for element in sorted_ranking:
                if i >= 3:
                    break
                #make sure only those numbers that actually have more than 0 counts are shown
                if (element[1]>0):
                    influencer_dict[self.getAliasFromDB(element[0])]=element[1]
                    i+=1

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
        print('filteredTimeSeriesData called')
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



            cursor.execute(sql_prepared_statement, insert_values)
            print('Command executed')
            userdata = cursor.fetchall()
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
            #TODO: this is bad style and should be changed at a later point
            sql_prepared_statement = "insert into Campaign (organization, username, mail, geography, collaborators, description, \
            campaign_identifier) VALUES (%s,%s,%s,%s,%s,%s,%s)"
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


    ############################################# NLP engine ###################################

    def setupNLTK(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stop = stopwords.words('english')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')

    def extract_phone_numbers(self,string):
        r = re.compile(r'(\+\d{1-3}?[-\.\s]??\d{2-5}?[-\.\s]??\d{3-6}?[-\.\s]??\d{3-6}?')
        phone_numbers = r.findall(string)
        return [re.sub(r'\D', '', number) for number in phone_numbers]

    def ie_preprocess(self,document):
        document = ' '.join([i for i in document.split() if i not in self.stop])
        sentences = nltk.sent_tokenize(document)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        return sentences

    def extract_names(self,document):
        names = []
        sentences = self.ie_preprocess(document)
        for tagged_sentence in sentences:
            for chunk in nltk.ne_chunk(tagged_sentence):
                if type(chunk) == nltk.tree.Tree:
                    if chunk.label() == 'PERSON':
                        names.append(' '.join([c[0] for c in chunk]))
        print('names in extract names: ' + str(names))
        return names