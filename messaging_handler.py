#created by Steffen Schmidt 5/23/2020

import SMS_Twilio_backend
import mysql.connector as connector
import system_constants


class messaging_handler:

    def __init__(self):
        self.backend = SMS_Twilio_backend.SMS_Twilio_backend()

    def sendMessage(self, target_number, message_content):

        status_values = self.backend.sendMessage(target_number, message_content)
        self.writeIntoMessagingDB(status_values, True)

    def receiveMessage(self, status_values):
        self.writeIntoMessagingDB(status_values, False)


    def writeIntoMessagingDB(self, status_values, message_outgoing):

        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)

            #important: don't put variable table name into statement other than through prepared statements
            if message_outgoing:
                sql_prepared_statement = """INSERT INTO Outgoing_messages (from_, to_, cost, currency, content, created , sent, updated, status, error_code, error_message) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            else:
                sql_prepared_statement = """INSERT INTO Incoming_messages (from_, to_, cost, currency, content, created , sent, updated, status, error_code, error_message) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            insert_values = (status_values['from'], status_values['to'], status_values['cost'],status_values['currency'],\
                             status_values['content'],status_values['created'],status_values['sent'],status_values['updated'],\
            status_values['status'],status_values['error_code'],status_values['error_message'])
            cursor.execute(sql_prepared_statement, insert_values)
            connection.commit()
            print('Wrote message into database')

        except connector.Error as error:
            print("Writing message into DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")






