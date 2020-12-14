"""
    File name           FingerCounter.py
    Author              Kevin J Jijo
    Date                15 November 2020
    Description         Implements opencv to create an immersive Rock/Paper/Scissors experience
"""


import cv2
import numpy as np
import math
import time
import random
import tkinter as tk
import Backend
from tkinter import messagebox
from tkinter import ttk

main_root = tk.Tk()
main_root.geometry("700x500")

""" 
    Function name       Highscore_Window
    Description         This creates a highscore table and then retrieves save data from backend 
"""
def Highscore_Window():

    Highscore_tb = tk.Toplevel(main_root)
    Highscore_tb.resizable(width=1, height=1)

    # Configuring the table
    Table = ttk.Treeview(Highscore_tb, selectmode='browse')
    Table.pack(side='right')

    verscrlbar = ttk.Scrollbar(Highscore_tb, orient="vertical", command=Table.yview)
    verscrlbar.pack(side='left', fill='x')

    # Configuring the scrollbar
    Table.configure(xscrollcommand=verscrlbar.set)

    Table["columns"] = ("1", "2", "3")
    Table['show'] = 'headings'

    Table.column("1", width=90, anchor='c')
    Table.column("2", width=90, anchor='se')
    Table.column("3", width=90, anchor='se')

    Table.heading("1", text="User ID")
    Table.heading("2", text="User Name")
    Table.heading("3", text="Highscore")

    Rows = Backend.Output_User()

    # Naming the rows and entering the data into individual rows
    i=1
    for Row in Rows:
        row_name = "L"+str(i)
        Table.insert("", 'end', text=row_name, values=Row)
        i+=1

""" 
    Function name       History_Window
    Description         This creates a history table and then retrieves save data from backend 
"""
def History_Window():

    History_tb = tk.Toplevel(main_root)
    History_tb.resizable(width=1, height=1)

    # Configuring the table
    Table = ttk.Treeview(History_tb, selectmode='browse')
    Table.pack(side='right')

    verscrlbar = ttk.Scrollbar(History_tb, orient="vertical", command=Table.yview)
    verscrlbar.pack(side='left', fill='x')

    # Configuring the scrollbar
    Table.configure(xscrollcommand=verscrlbar.set)

    Table["columns"] = ("1", "2", "3","4", "5", "6")
    Table['show'] = 'headings'

    Table.column("1", width=90, anchor='c')
    Table.column("2", width=90, anchor='se')
    Table.column("3", width=90, anchor='se')
    Table.column("4", width=90, anchor='se')
    Table.column("5", width=90, anchor='se')
    Table.column("6", width=90, anchor='se')

    Table.heading("1", text="Game No.")
    Table.heading("2", text="User ID")
    Table.heading("3", text="User Name")
    Table.heading("4", text="User Played")
    Table.heading("5", text="Comp Played")
    Table.heading("6", text="Winner")

    Rows = Backend.Output_Game()

    # Naming the rows and entering the data into individual rows
    i=1
    for Row in Rows:
        row_name = "L"+str(i)
        Table.insert("", 'end', text=row_name, values=Row)
        i+=1

""" 
    Function name       Login
    Description         This creates a Login window and asks for the user's name
"""
def Login():

    global user_name

    login_window = tk.Toplevel(main_root)
    login_window.title("Login")
    login_window.geometry("600x100")
    login_window.configure(background="light cyan")

    username_Label = tk.Label(login_window, text="Enter your name :", font=("System", 18), bg="light cyan").grid(row=0, column=0)

    username_Entry = tk.Entry(login_window, textvariable=username, font=("System", 18), bg="pink", fg="red").grid(row=0, column=1)
    user_name = username.get()

    # Clicking on this button will start the chain of nested functions for the game
    loginButton = tk.Button(login_window, text="Login", command=lambda: FingerCounter_init(user_name, login_window), bg="yellow", activebackground="green", fg="blue", font=("System",20)).grid(row=5, column=1, sticky=tk.W)

""" 
    Function name       ExitApplication
    Description         After clicking the Quit button on the main_root start menu, this ends all the windows
"""
def ExitApplication():

    MsgBox = messagebox.askquestion('Exit Application', 'Are you sure you want to exit the game?',
                                       icon='warning')
    if MsgBox == 'yes':
        #cv2.destroyAllWindows()
        main_root.destroy()

""" 
    Function name       Comp_Choice
    Description         After obtaining the user input, a random choice is chosen for the computer
"""
def Comp_Choice(options, game_window):

    try:
        global comp_choice
        global comp_choice_name

        display = random.randint(0, 2)

        if options[display] == "Rock":
            comp_choice = display
            comp_choice_name = options[display]
            comp_played.set(comp_choice_name)
            game_window.update()

        elif options[display] == "Paper":
            comp_choice = display
            comp_choice_name = options[display]
            comp_played.set(comp_choice_name)
            game_window.update()

        elif options[display] == "Scissors":
            comp_choice = display
            comp_choice_name = options[display]
            comp_played.set(comp_choice_name)
            game_window.update()

    except Exception as e:
        print(e)

""" 
    Function name       RPS_Algo
    Description         Rock/Paper/Scissors algorithm, decides who wins
"""
def RPS_Algo(comp, player, options, game_window, user_name):

    try:

        global points

        if options[player] == "Rock" and options[comp] == "Scissors":
            Update_Points(game_window, player, comp)

        elif options[player] == "Paper" and options[comp] == "Rock":
            Update_Points(game_window, player, comp)

        elif options[player] == "Scissors" and options[comp] == "Paper":
            Update_Points(game_window, player, comp)

        elif player == comp:
            user_id = Backend.Get_User_id(user_name)
            Backend.insert_game(user_id, options[player], options[comp], "Tie")
            pass

        else:
            # Player lost so score is reset to 0
            Backend.insert_User(user_name, points)
            points = 0
            display_points.set(str(points))
            game_window.update()

            # Inserting game details to history
            user_id = Backend.Get_User_id(user_name)
            Backend.insert_game(user_id, options[player], options[comp], "Computer")

    except Exception as e:
        print(e)

""" 
    Function name       Update_Points
    Description         Updates points if player won
"""
def Update_Points(game_window, player, comp):

    global points

    points += 1
    # sets the variable string into the new points score
    display_points.set(str(points))
    game_window.update()

    # Inserting game details to history
    user_id = Backend.Get_User_id(user_name)
    Backend.insert_game(user_id, options[player], options[comp], "User")

""" 
    Function name       Show_Message
    Description         Asks user if recognized hand sign is correct input
"""
def Show_Message(num, options, game_window, user_name):

    try:
        global choice
        global choice_name

        if close == 1:
            return
        MsgBox = tk.messagebox.askquestion('Choice', 'Did you choose '+options[num]+"?")

        if MsgBox == 'yes':
            choice = num
            choice_name = options[num]

            # calls comp_choice which randomly determines what comp plays
            Comp_Choice(options, game_window)
            RPS_Algo(comp_choice, choice, options, game_window, user_name)
        elif MsgBox == 'no ':
            user_played.set("Waiting for user..")

    except Exception as e:
        print(e)

""" 
    Function name       Exit_GameWindow
    Description         Exits the game from the Gam_window and returns back to Start_Menu
"""
def Exit_GameWindow(user_name, game_window, cap):

    global close
    close = 1

    Backend.insert_User(user_name, points)
    game_window.withdraw()
    main_root.deiconify()

""" 
    Function name       FingerCounter_init
    Description         Creates the game window, initializes the camera
"""
def FingerCounter_init(user_name, login_window):

    main_root.withdraw()
    login_window.withdraw()

    if  username.get() == '':
        username.set("Guest")
    user_name = username.get()

    Backend.insert_User(user_name,0)

    game_window = tk.Toplevel(main_root)

    start_time = time.time()
    cap = cv2.VideoCapture(0)

    game_window.title("Gameplay")
    game_window.geometry("600x300")
    game_window.configure(background="light cyan")

    user_played.set("Waiting for user..")
    label3 = tk.Label(game_window, text="User Played : ", font=("System",18), bg="light cyan").grid(sticky = tk.W, column=0,row=0)
    label4 = tk.Label(game_window, textvariable=user_played, font=("System",18), bg="yellow").grid(sticky = tk.W, column=1,row=0)

    comp_played.set("Waiting for computer..")
    label1 = tk.Label(game_window, text="Computer Played : ", font=("System",18), bg="light cyan").grid(sticky = tk.W, column=0,row=1)
    label2 = tk.Label(game_window, textvariable=comp_played, font=("System",18), bg="yellow").grid(sticky = tk.W, column=1,row=1)

    display_points.set("0")
    label5 = tk.Label(game_window, text="Points : ", font=("System",25), bg="light cyan").grid(sticky = tk.W, column=0,row=4, padx = 5, pady = 5)
    label6 = tk.Label(game_window, textvariable=display_points, font=("System",25), bg="pink").grid(sticky = tk.W, column=1,row=4, padx = 5, pady = 5)
    game_window.update()

    temp = Backend.Get_Highscore(user_name)
    highscore_latest.set(temp)
    highscore = tk.Label(game_window, text="Highscore : ", font=("System", 20), bg="light cyan").grid(sticky=tk.W, column=0, row=5, padx=5, pady=5)
    highscore_display = tk.Label(game_window, textvariable=highscore_latest, font=("System", 20), bg="pink").grid(sticky=tk.W, column=1, row=5, padx=5, pady=5)

    exit_button = tk.Button(game_window, text="QUIT?", command=lambda: Exit_GameWindow(user_name, game_window, cap), bg="pink", activebackground="red", font=("System", 23)).grid(sticky=tk.W, column=1, row=6, padx=10, pady=10)
    game_window.update()

    global choice
    global choice_name
    global points
    points = 0

    # Starts the function responsible for image manipulation
    Image_Manipulation(cap, game_window, start_time, user_name)

""" 
    Function name       Image_Manipulation
    Description         Manipulates the obtained camera input to make hand recognition easier
"""
def Image_Manipulation(cap, game_window, start_time, user_name):

    global close

    while (close==0):
        try:

            # Creates the frame window which is unaltered camera footage
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            # Used later to define how the pixels will interact with nearby pixels
            kernel = np.ones((3, 3), np.uint8)

            # Defines the square where hand recognition will take place
            roi = frame[100:300, 100:300]
            cv2.rectangle(frame, (100,100), (300,300), (255,0,0),2)

            # Converts image to hsv image
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            lower = np.array([0, 20, 70], dtype="uint8")
            upper = np.array([20, 255, 255], dtype="uint8")

            # Creates mask, in which all colours have been filtered except yellow to dark brown
            mask = cv2.inRange(hsv, lower, upper)
            mask = cv2.GaussianBlur(mask, (5,5), 100)
            mask = cv2.dilate(mask, kernel, iterations=3)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # Calls the function where calculations to detect number of fingers begin
            Defects_Counter(mask, roi, frame, game_window, start_time, user_name)

        except:
            pass

        # To quit from the while loop, in which the csv windows is created
        if (cv2.waitKey(1) & 0xFF == ord('q')) or (close == 1):
            close = 0
            break

    # Destroys cv2 windows
    cv2.destroyAllWindows()
    cap.release()

""" 
    Function name       Defects_Counter
    Description         Uses cosine theory to determine the number of defects
"""
def Defects_Counter(mask, roi, frame, game_window, start_time, user_name):

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(contours, key=lambda x: cv2.contourArea(x))

    epsilon = 0.0005 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)


    hull = cv2.convexHull(cnt)

    areaHull = cv2.contourArea(hull)
    areacnt = cv2.contourArea(cnt)

    arearatio = ((areaHull-areacnt)/areacnt)*100

    hull = cv2.convexHull(approx, returnPoints=False)
    defects = cv2.convexityDefects(approx, hull)

    """==if defects is not None:
                l = 0"""
    l = 0

    # Calculates area, perimeter and sides of defects to determine number of fingers
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i][0]
        start = tuple(approx[s][0])
        end = tuple(approx[e][0])
        far = tuple(approx[f][0])
        pt=(100, 100)

        a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
        s = (a + b + c)/2
        ar = np.sqrt(s * (s - a) * (s - b) * (s - c))

        dHull = (2 * ar) / a

        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

        if angle <= 90 and d>30:
            l += 1
            cv2.circle(roi, far, 3, [255, 0, 0], -1)

        cv2.line(roi, start, end, [0, 255, 0], 2)

    User_Choice(l, areacnt, frame, mask, game_window, start_time, user_name)

""" 
    Function name       User_Choice
    Description         Determines number of fingers and asks user to finalize input
"""
def User_Choice(l, areacnt, frame, mask, game_window, start_time, user_name):

    time_passed = int(time.time()-start_time)

    if time_passed % 5 == 0:
        l += 1
        if l == 1:
            if areacnt<2000:
                cv2.putText(frame,'Put hand in the box',(0,50), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255), 3, cv2.LINE_AA)
            else:
                cv2.putText(frame,'Rock',(0,50), cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,255), 3, cv2.LINE_AA)

                Show_Message(0, options, game_window, user_name)

                user_played.set(choice_name)
                game_window.update()

        elif l == 2:
            cv2.putText(frame, 'Scissors', (0, 50), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 3, cv2.LINE_AA)

            Show_Message(2, options, game_window, user_name)

            user_played.set(choice_name)
            game_window.update()

        elif l == 5:
            cv2.putText(frame,'Paper',(0,50), cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,255), 3, cv2.LINE_AA)

            Show_Message(1,options, game_window, user_name)

            user_played.set(choice_name)
            game_window.update()

        else :
            cv2.putText(frame,'Invalid Input',(10,50), cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,255), 3, cv2.LINE_AA)

    cv2.imshow('mask', mask)
    cv2.imshow('frame', frame)

comp_choice = 0
comp_choice_name = ""
choice = 0
choice_name = ""
points = 0
options = ["Rock", "Paper", "Scissors"]
close = 0

username = tk.StringVar()
user_played = tk.StringVar()
comp_played = tk.StringVar()
display_points = tk.StringVar()
highscore_latest = tk.StringVar()


main_root.configure(background="light cyan")
main_root.title("Start Menu")


# Creating Start Menu
label = tk.Label(main_root, text="WELCOME TO\nROCK, PAPER, SCISSORS!", font=("System", 35), bg="light cyan").pack()

greet_button = tk.Button(main_root, text="PLAY NOW", command=Login, bg="yellow", activebackground="green", fg="blue", font=("System", 30)).pack(pady=10)

highscore_button = tk.Button(main_root, text="HIGHSCORES", command=Highscore_Window, bg="light slate blue", activebackground="green", fg="blue", font=("System", 25)).pack(pady=10)

history_button = tk.Button(main_root, text="HISTORY", command=History_Window, bg="light green", activebackground="green", fg="blue", font=("System", 25)).pack(pady=10)

close_button = tk.Button(main_root, text="QUIT?", command=ExitApplication, bg="pink", activebackground="red", fg="blue", font=("System", 15)).pack(pady=10)


Backend.init()

main_root.mainloop()