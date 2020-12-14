"""
    File name           Backend.py
    Author              Kevin J Jijo
    Date                15 November 2020
    Description         Backend software using MySQL
"""

import mysql.connector as sqlcon
from mysql.connector import Error

""" 
    Function name       init
    Description         Creates database and tables if not exist
"""
def init():
    try:
        mycur.execute("CREATE DATABASE IF NOT EXISTS FingerCounter;")
        myconn.commit()

        mycur.execute("USE FingerCounter;")
        myconn.commit()

        mycur.execute("CREATE TABLE IF NOT EXISTS User(User_id smallint UNSIGNED AUTO_INCREMENT primary key, User_name varchar(25) not null, Highscore int(6) not null);")
        myconn.commit()

        mycur.execute("CREATE TABLE IF NOT EXISTS Game(Game_no int(11) UNSIGNED AUTO_INCREMENT primary key, User_id smallint not null, User_played char(10) not null, Comp_played char(10) not null, Winner char(10) not null);")
        myconn.commit()
    except Error as e:
        print("Error occured : ", e)

""" 
    Function name       insert_game
    Description         Inserts data into game table
"""
def insert_game(user_id,user, comp, winner):
    try:
        query="INSERT INTO Game(User_id, User_played, Comp_played, Winner) VALUES (%s,%s,%s,%s)"
        val=(user_id,user, comp, winner)
        mycur.execute(query, val)
        myconn.commit()
    except Error as e:
        print("Error occured : ", e)

""" 
    Function name       insert_User
    Description         Inserts data into user table
"""
def insert_User(username,points):
    try:
        query="Select User_name, Highscore from User"
        mycur.execute(query)
        highscores = mycur.fetchall()
        print(highscores)

        if highscores==[]:
            query = "INSERT INTO User(User_name, Highscore) VALUES (%s,%s)"
            val = (username, points)
            mycur.execute(query, val)
            myconn.commit()

        else:
            for row in highscores:
                if username in row:
                    if points>row[1]:
                        print("Going to update")
                        query = "UPDATE User SET Highscore=%s WHERE User_name=%s"
                        val = (points, username)
                        mycur.execute(query, val)
                        myconn.commit()
                        break
                    else:
                        break
                else:
                    continue
            else:
                print("Going to insert")
                query="INSERT INTO User(User_name, Highscore) VALUES (%s,%s)"
                val=(username,points)
                mycur.execute(query,val)
                myconn.commit()

    except Error as e:
        print("Error occured : ", e)

""" 
    Function name       Output_User
    Description         Retrieves data from User table
"""
def Output_User():
    try:
        query = "Select * from User order by Highscore desc"
        mycur.execute(query)
        highscores = mycur.fetchall()

        return highscores

    except Error as e:
        print("Error occured : ", e)

""" 
    Function name       Output_Game
    Description         Retrieves data from Game table
"""
def Output_Game():
    try:
        query = "Select Game.Game_no, Game.User_id, User.User_name, Game.User_played, Game.Comp_played, Game.Winner from Game inner join User on Game.User_id=User.User_id order by Game_no desc"
        mycur.execute(query)
        history = mycur.fetchall()

        return history

    except Error as e:
        print("Error occured : ", e)

""" 
    Function name       Get_User_id
    Description         Gets user id using user name
"""
def Get_User_id(username):
    try:
        query="Select User_id, User_name from User"
        mycur.execute(query)
        users=mycur.fetchall()
        for row in users:
            if username in row:
                return row[0]

    except Error as e:
        print("Error occured : ", e)

""" 
    Function name       Get_Highscore
    Description         Gets highscore from user table using username
"""
def Get_Highscore(username):
    try:
        query = "Select Highscore, User_name from User"
        mycur.execute(query)
        users = mycur.fetchall()
        for row in users:
            if username in row:
                return row[0]

    except Error as e:
        print("Error occured : ", e)

try:
    myconn = sqlcon.connect(host="localhost", user="root", passwd="password")
    mycur = myconn.cursor()
except Error as e:
    print("Error occured : ", e)

