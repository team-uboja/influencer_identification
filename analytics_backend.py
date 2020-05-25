#created by Steffen Schmidt on 5/24/2020
import mysql.connector as connector
import system_constants
import flask



class analytics_backend:

    def conductAnalysis(self):
        try:
            connection = connector.connect(user=system_constants.AMAZON_RDS_DB1_USERNAME, password = system_constants.AMAZON_RDS_DB1_PASSWORD\
                , host='ubuntu-db1.cq7wudipahsy.us-east-2.rds.amazonaws.com', port='3306', database='Ubuntu')

            cursor=connection.cursor(prepared=True)
            sql_statement = "select (content, from_city) from Incoming_messages"

            cursor.execute(sql_statement)
            votes = cursor.fetchall()

            ranking = {}

            for vote in votes:
                if vote[0] not in ranking:
                    ranking[vote[0]] = [1,[vote[1]]]
                else:
                    ranking[vote[0]][0] = ranking[vote[0]][0]+1
                    ranking[vote[0]][1].append(vote[1])

            sorted_ranking = sorted(ranking.items(), key=lambda x: x[0], reverse=False)

            return flask.jsonify({"Name1": sorted_ranking.keys[0],"Name2": sorted_ranking.keys[1],"Name3": sorted_ranking.keys[2], \
                                  "Name4": sorted_ranking.keys[3],"Name5": sorted_ranking.keys[4],"Count1": sorted_ranking.items[0][0], \
                                  "Count2": sorted_ranking.items[1][0],"Count3": sorted_ranking.items[2][0],"Count4": sorted_ranking.items[3][0], \
                                  "Count5": sorted_ranking.items[4][0],"City1": max(set(sorted_ranking.items[0][1]), key=sorted_ranking.items[0][1].count),\
                                  "City2": max(set(sorted_ranking.items[1][1]), key=sorted_ranking.items[1][1].count), \
                                  "City3": max(set(sorted_ranking.items[2][1]), key=sorted_ranking.items[2][1].count), \
                                  "City4": max(set(sorted_ranking.items[3][1]), key=sorted_ranking.items[3][1].count), \
                                  "City5": max(set(sorted_ranking.items[4][1]), key=sorted_ranking.items[4][1].count)})


        except connector.Error as error:
            print("Writing message into DB failed")
            print(error)

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("Connection to DB has been closed")

