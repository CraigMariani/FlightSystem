from flask import Flask, render_template, request, session, url_for, redirect
import pymysql
import dbClass, sys
from passlib.hash import sha256_crypt

app = Flask(__name__)

hashedPassword = None
# app.secret_key = 'super secret key'

@app.route('/')
def home():
    return render_template('hello.html')

@app.route('/updateReservation.html', methods=['GET', 'POST'])
def alterReservations():
    def db_query():
        db = dbClass.Database()
        updateNum = None #search key for finding reservation to update
        flightNum = None
        reservationName = None
        flightLeg = None
        flightTimePerLeg = None
        totalFlightTime = None
        layOverTime = None

        newReserv = None

        print("before PUT")
        if request.method == 'POST':
            print("after PUT")
            
            updateNum = request.form['reservNumber']
            reservationName = request.form['reservName']
            flightLeg = request.form['flightLeg']
            flightTimePerLeg = request.form['flightTime']
            totalFlightTime = request.form['totalFlightTime']
            layOverTime = request.form['layOverTime']

            
            print("before update")
            newReserv = db.changeReservation(reservationName, flightLeg, flightTimePerLeg, totalFlightTime, layOverTime, updateNum)
            # newReserv = db.changeReservation(reservationName, updateNum)
            print("updated table")
        return newReserv

    result = db_query()

    return render_template('updateReservation.html', content_type='application/json')


@app.route('/showReservations.html', methods=['GET','POST'])
def showReservations():
    def db_query():
        db = dbClass.Database()
        searchNum = None #search key for finding reservation to display
        allValues = None #lists all values when True
        inputs = ["reservationNum", "flightNum", "reservationName", "flightTimePerLeg", "totalFlightTime", "layOverTime"]
        
        if request.method == 'POST':
            searchNum = request.form['searchNum']
            

            if searchNum != '':
                reserves = db.filterReservations(searchNum)
                return reserves

                # for i in range(len(inputs)):
                #     print(request.form.get(i))
                #     if request.form.get(i) == True:
                #         reserves = db.fineReservationsFilter(request.form.get(i), searchNum)
                #     else:
                #         reserves = db.filterReservations(searchNum)
                
            else:
                reserves = db.listReservations()


            # else:
            #     print("No search Val")
            #     reserves = db.listReservations()
            # for i in range(len(inputs)):
            #     if request.form.get(i) == True:
            #         reserves = db.fineReservationsFilter(i, searchNum)
            #     else:
            #         reserves = db.filterReservations(searchNum)
            
            
        else:
            reserves = db.listReservations()

        
        return reserves
    result = db_query()
    return render_template('showReservations.html', result=result, content_type='application/json')

@app.route('/deleteReservation.html', methods=['GET', 'POST'])
def deleteReservation():
    def db_query():
        db = dbClass.Database()
        deleteNum = None
        message = None
        

        if request.method == 'POST':
            
            deleteNum = request.form['deleteNumber']
            db.deleteReservation(deleteNum)
            message = "Reservation Sucessfully Deleted"

        
        return message

    message = db_query()
            
    return render_template('deleteReservation.html', message=message, content_type='application/json')

@app.route('/reservation.html', methods=['GET','POST'])
def reservation():

    error = False
    message = None 

    reservationNum = None
    flightNum = None
    flightLeg = None
    flightTimePerLeg = None
    totalFlightTime = None
    layOverTime = None

    db = dbClass.Database()

    if request.method == 'POST':
        reservationName = request.form['reservName']
        flightLeg = request.form['flightLeg']
        flightTimePerLeg = request.form['flightTime']
        totalFlightTime = request.form['totalFlightTime']
        layOverTime = request.form['layOverTime']

        # change this! it's not adding to reservation because flightNum is null!
        if reservationName != None:
            db.createReservation(reservationName, flightLeg, flightTimePerLeg, totalFlightTime, layOverTime)

            message = "Reservation sucessfully created."
        
        else:
            # message is not displaying! Find out why!
            message = "Error, could not make reservation."
    
    return render_template('reservation.html', message=message)


        
@app.route('/signup.html', methods=['GET','POST']) 
def signup():
    message = None
    userInputName = None
    userInputPassword = None
    signupUser = None
    signupPassword = None



    db = dbClass.Database()
    
    if request.method == 'POST':
        firstName = request.form['firstname']
        lastName = request.form['lastname']
        userInputName = request.form['username']
        userInputPassword = request.form['password']

        
        global hashedPassword
        hashedPassword = sha256_crypt.encrypt(userInputPassword)
   
        db.importUser( firstName, lastName, userInputName, hashedPassword)
        message = "Sign up successful"
        

        # else:
        #     error = "Error could not input to database"

    return render_template('signup.html', messsage= message)


@app.route('/login.html', methods=['GET','POST'])
def login():
    error=None  
    db = dbClass.Database()
    verified = False


    if request.method == 'POST': #if the user asks to submit his login to the database
       
    #access HTML input in login.HTML, stores firstname, lastbame, username and password submitted 
        
        userInputName = request.form['username']
        userInputPassword = request.form['password']

    #access Python in dbClass.py 
        userCheck = db.checkUser(userInputName)
        pwdCheck = db.checkPassword(userInputName)

        if userCheck == userInputName:
            
            global hashedPassword

            verified = sha256_crypt.verify(userInputPassword,hashedPassword)
            if verified == True or userInputPassword == pwdCheck:
                # session['logged_in'] = True
                # currentUser = db.getUserID(userCheck)
                return redirect(url_for('home'))#redirect to home

            else:
                error = 'Verification failed'
        else:
            error = 'Invalid Credentials. Please try again'

    return render_template('login.html', error=error, verified=verified)


if __name__ == "__main__":
    app.run()