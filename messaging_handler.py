#created by Steffen Schmidt 5/23/2020

import SMS_Twilio_backend
import mysql.connector as connector
import system_constants
import csv
import os


class messaging_handler:

    def __init__(self):
        self.backend = SMS_Twilio_backend.SMS_Twilio_backend()

    #csv file format must be phonenumber, message
    def parseSubmittedCSVFiles(self):
        with open(os.path.join(system_constants.UPLOAD_FOLDER, system_constants.CSV_FILENAME)) as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:
                print(row)
                self.sendMessage(row[0], row[1], row[2])
            csvfile.close()

    def sendOutMessages(self, message_array, campaign_identifier):
        i=0
        while i<len(message_array):
            self.sendMessage(message_array[i+1], message_array[i+2], campaign_identifier)
            i+=3



    def sendMessage(self, target_number, message_content, campaign_identifier):

        status_values = self.backend.sendMessage(target_number, message_content, campaign_identifier)
        self.writeIntoMessagingDB(status_values, True)

    def receiveMessage(self, status_values, campaign_identifier):
        self.writeIntoMessagingDB(status_values, False)
        self.sendMessage(status_values['from'], 'Thanks a lot for your nomination.', campaign_identifier)


    def writeIntoMessagingDB(self, status_values, message_outgoing):

        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)

            #important: don't put variable table name into statement other than through prepared statements
            if message_outgoing:
                sql_prepared_statement = """INSERT INTO Outgoing_messages (from_, to_, cost, currency, content, created , sent, updated, status, error_code, error_message, campaign_identifier) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                insert_values = (status_values['from'], status_values['to'], status_values['cost'], status_values['currency'], \
                    status_values['content'], status_values['created'], status_values['sent'], status_values['updated'], \
                    status_values['status'], status_values['error_code'], status_values['error_message'], status_values['campaign_identifier'])
            else:
                sql_prepared_statement = """INSERT INTO Incoming_messages (from_, to_, cost, currency, content, created , sent, updated, status, error_code, error_message, from_city, from_zip) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                insert_values = (status_values['from'], status_values['to'], status_values['cost'],status_values['currency'],\
                        status_values['content'],status_values['created'],status_values['sent'],status_values['updated'],\
                        status_values['status'],status_values['error_code'],status_values['error_message'], status_values['from_city'], status_values['from_zip'],\
                        status_values['campaign_identifier'], status_values['voted_for'], status_values['age'])
            cursor.execute(sql_prepared_statement, insert_values)
            connection.commit()
            print('Wrote message into database')

        except connector.Error as error:
            print("Writing message into DB failed")
            print(error)
            print(status_values)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")






