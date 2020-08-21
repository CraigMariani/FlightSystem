import pymysql

class Database():
        def __init__(self): 
                host = "127.0.0.1"
                user = "root"
                password = "Wedgewood79$"
                db = "flightsystem"
                self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                        DictCursor)
                self.cur = self.con.cursor()
        
        # def changeReservation(self, reservationName, updateNum):
        def changeReservation(self, reservationName, flightLeg, flightTimePerLeg, totalFlightTime, layOverTime, updateNum):
                stmt = """
                        UPDATE reservation
                        SET reservationName = %s, flightLeg = %s, flightTimePerLeg = %s, totalFlightTime = %s, layOverTime = %s
                        WHERE reservationNum = %s"""

                # stmt = """
                        
                #         UPDATE reservation
                #         SET reservationName = %s
                #         WHERE reservationNum = %s"""
                data = (reservationName, flightLeg, flightTimePerLeg, totalFlightTime, layOverTime, updateNum)
                self.cur.execute(stmt, data)
                # self.cur.execute(stmt, reservationName, updateNum)
                # self.cur.execute("UPDATE reservation SET reservationName = reservationName WHERE reservationNum = updateNum")
                self.con.commit()

                

        def checkReservation(self, searchReserv, reservation_Name, flight_Leg, flight_Time_Per_Leg, total_Flight_Time, lay_Over_Time):
                stmt = "SELECT * FROM reservation WHERE reservationNum = %s"
                self.cur.execute(stmt, searchReserv)

                row=self.cur.fetchall()
                return row

        def deleteReservation(self, deleteNumber):
                stmt = "DELETE FROM reservation WHERE reservationNum = %s"
                self.cur.execute(stmt, deleteNumber)

                self.con.commit()


        def filterReservations(self, searchNum):
                stmt = "SELECT * FROM reservation WHERE reservationNum = %s"
                self.cur.execute(stmt, searchNum)

                row=self.cur.fetchall()
                return row
                

        def fineReservationsFilter(self, inputColumn, search_Num):
                stmt = "SELECT %s FROM reservation WHERE reservationNum = %s"
                data = (inputColumn, search_Num)
                self.cur.execute(stmt, data)

                row=self.cur.fetchall()
                return row
        
        def findReservationNum(self, search_Num):
                stmt = "SELECT reservationNum FROM reservation WHERE reservationNum = %s"
                self.cur.execute(stmt, search_Num)

                row=self.cur.fetchone()
                return row

        def listReservations(self):
                self.cur.execute("SELECT * FROM reservation")
                result = self.cur.fetchall()
                return result

        def createReservation(self, reservation_Name, flight_Leg, flight_Time_Per_Leg, total_Flight_Time, lay_Over_Time):
                stmt = """INSERT INTO reservation (reservationName, flightLeg, flightTimePerLeg, totalFlightTime, layOverTime)
                VALUES (%s, %s, %s, %s, %s)"""

                val = (reservation_Name, flight_Leg, flight_Time_Per_Leg, total_Flight_Time, lay_Over_Time)
                self.cur.execute(stmt, val)
                self.con.commit()
                
                result = self.cur.fetchall()
                return result
        def checkUser(self, user):  
                stmt = "SELECT username FROM genericuser where username = %s" 
                self.cur.execute(stmt, user) #executes statment with cursor

                row=self.cur.fetchone() #used for capturing a single value
                if row != None:
                        return row['username'] #this returns the column user_name 
    
        def checkPassword(self, user):
                stmt = "SELECT userpassword FROM genericuser where username = %s"
                self.cur.execute(stmt, user)
                row=self.cur.fetchone()
                if row != None:
                        return row['userpassword']

        def importUser(self, firstname, lastname, user, pword):
                stmt = "INSERT INTO genericuser (firstname, lastname, username, userpassword) VALUES (%s, %s, %s, %s)"
                val = (firstname, lastname, user,pword)
                self.cur.execute(stmt,val)
                # self.cur.execute("SELECT MAX user_id FROM users")
                self.cur.execute("DELETE FROM genericuser WHERE username ='' ")
                self.cur.execute("DELETE FROM genericuser WHERE userpassword ='' ")
                self.con.commit()
                result = self.cur.fetchall()
                return result