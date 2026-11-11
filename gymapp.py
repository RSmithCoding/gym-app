import sqlite3
import os
from datetime import date

def clear():
    os.system('clear')

def createdatabase():

    con = sqlite3.connect('gymapp.db')
    cur = con.cursor()

#   CREATE DATABASE
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute("""CREATE TABLE IF NOT EXISTS Exercises(
                exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise_name TEXT NOT NULL,
                body_area TEXT NOT NULL,
                secondary_area TEXT
                )
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS Sessions(
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_name TEXT
                )
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS SessionExercises(
                exercise_id INTEGER,
                session_id INTEGER,
                PRIMARY KEY (exercise_id, session_id),
                FOREIGN KEY (exercise_id) REFERENCES Exercises(exercise_id) ON DELETE CASCADE, 
                FOREIGN KEY (session_id) REFERENCES Sessions(session_id) ON DELETE CASCADE
                )
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS WorkoutHistory(
                wo_history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                workout_date TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES Sessions(session_id) ON DELETE SET NULL
                )
    """)

    cur.execute("""CREATE TABLE IF NOT EXISTS TrainingLog(
                training_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                wo_history_id INTEGER,
                exercise_id INTEGER,
                sets INTEGER,
                reps INTEGER,
                weight REAL,
                FOREIGN KEY (wo_history_id) REFERENCES WorkoutHistory(wo_history_id) ON DELETE CASCADE,
                FOREIGN KEY (exercise_id) REFERENCES Exercises(exercise_id) ON DELETE CASCADE
                )
    """)
#   POPULATE TABLE WITH DEFAULT DATA
    
    cur.execute("""INSERT INTO Exercises VALUES
                (NULL, "Bench Press", "Chest", "Triceps, Shoulders"
                )
    """)
    con.commit()
    con.close()


def exercise():
    header()
    con = sqlite3.connect('gymapp.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("SELECT exercise_id, exercise_name, body_area, secondary_area FROM Exercises ORDER BY body_area ASC")
    con.commit()
    allexercises = cur.fetchall()
    
    rowcount = len(allexercises)
    record = 0

    con.close()

#   DISPLAY EXERCISES     
    print("")
    print(f"\tID\t\tExercise Name\t\t     Target Body Area\t\tSecondary Area")
    print("")
    while record < rowcount:
        print("{:<25}{:<29}{:<27}{:<10}".format(allexercises[record][0],allexercises[record][1],allexercises[record][2],allexercises[record][3]))
        record = record + 1
    print("")
    choice = input("Please select 'b' to go back, 'a' to add a new record, 'd' to delete or 'm' to modify and existing record.. ")

    while choice.lower() != "b" or "a" or "d" or "m":
            if choice.lower() == "b":
                header()
                mainmenu()
            elif choice.lower() == "a":
                add_exercise()
            elif choice.lower() == "d":
                delete_exercise()
            elif choice.lower() == "m":
                modify_exercise()

            clear()
            header()
            exercise()

def add_exercise():
    con = sqlite3.connect('gymapp.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    header()
    print('Add New Exercise...')
    print()
    new_name = input("Enter the exercise name: ")
    print()
    new_body_area = input("Enter the primary body area: ")
    print()
    new_secondary_area = input("Enter the secondary body area: ")
    print()
    print()

    choice = input("Would you like to add the above to the database? Press 'y' to confirm or 'n' to return.. ")

    new_exercise = new_name, new_body_area, new_secondary_area

    while choice.lower() != "y" or "n":
        if choice.lower() == "y":
            cur.execute("INSERT INTO Exercises VALUES (NULL,?,?,?)", new_exercise)
            con.commit()
            con.close()
            exercise()
        elif choice == "n":
            return
        else:
            print("Please press 'y' or 'n'")

def delete_exercise():
    con = sqlite3.connect('gymapp.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("SELECT * FROM Exercises")
    con.commit()
    allexercises = cur.fetchall()
    validids = [row[0] for row in allexercises]
    
    check = 0
    print()

    while check != 1:
        
        idtodel = input("Please type the ID number of the Exercise to DELETE follow by ENTER or 'b' to go back.. ")

        if idtodel.lower() == "b":
            header()
            exercise()
        elif idtodel.isdigit():
            indextodel = int(idtodel)
            if indextodel in validids:
                cur.execute("DELETE FROM Exercises WHERE exercise_id=?", (idtodel,))
                con.commit()
                check = 1

    con.close() 
    header()
    exercise()        

def modify_exercise():

    con = sqlite3.connect('gymapp.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("SELECT * FROM Exercises")
    con.commit()
    allexercises = cur.fetchall()
    validids = [row[0] for row in allexercises]
        
    check = 0
    print()
    
    while check != 1:
        
        idtomod = input("Please type the ID number of the Exercise to MODIFY follow by ENTER or 'b' to go back.. ")
    
        if idtomod.lower() == "b":
            header()
            exercise()
        elif idtomod.isdigit():
            indextodel = int(idtomod)
            if indextodel in validids:
                cur.execute("SELECT * FROM Exercises WHERE exercise_id=?", (idtomod,))
                existing_record = cur.fetchone()
                con.commit()
                header()
                print("Current Exercise details:\n")
                print(f"Name:\t\t\t{existing_record[1]}\n")
                print(f"Primary Area:\t\t{existing_record[2]}\n")
                print(f"Secondary Area:\t\t{existing_record[3]}\n")
                print("New Exercise details:\n")
                new_namemod = input("Please enter the new or existing name: ")
                print()
                new_primarymod = input("Please enter the new or existing primary area: ")
                print()
                new_secondarymod = input("Please enter the new or existing secondary area: ")
                print()
                choice = input("Are you happy with the changes? 'y' to confirm or 'n' to go back.. ")

                while choice.lower() != "y" or "n":
                    if choice.lower() == "y":
                        cur.execute("UPDATE Exercises SET exercise_name=?, body_area=?, secondary_area=? WHERE exercise_id=?", (new_namemod,new_primarymod,new_secondarymod,idtomod))
                        con.commit()
                        check = 1
                        return
                    elif choice.lower() == "n":
                        check = 1
                        return
                    else:
                        print("Please press 'y' or 'n'")
                
        
        con.close() 
        header()
        exercise()
    return

def newsession():
    con = sqlite3.connect('gymapp.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    header()

    try: 
        cur.execute("SELECT * FROM Exercises")
        allexercises = cur.fetchall()
        if not allexercises:
            print("No exercises found in database! Please add exercises first.")

        selected_exercise_ids = []
        current_filter = None

        while True:
            header()

            if selected_exercise_ids:
                print(f"Current Session:\t{len(selected_exercise_ids)} exercise(s) added.\n")
            else:
                print("Current Session:\tEmpty\n")

            print(f"Exercise Filter:\t{current_filter if current_filter else 'None - Showing All'}\n")

            for exercise_id, exercise_name, body_area, secondary_area in allexercises:
                if current_filter and body_area.strip().lower() != current_filter:
                    continue

                if exercise_id in selected_exercise_ids:
                    status = "✅"
                    status_w = 7
                else:
                    status = " "
                    status_w = 8

                print(f"{status:<{status_w}}{exercise_id:<6}{exercise_name:<20}{body_area:<20}{secondary_area:<20}")

            print("")
            print("Type the exercise ID to add or remove it to the session, type 'f' to filter by body area.")
            print("Type 'c' to clear the selections, 'b' to go back to main menu or 's' to save the session.")
            print("")
            choice = input("Please make a selection.. ")

            if choice == "f":
                filted_areas = sorted(list({row[2].strip() for row in allexercises if row[2]}))
                print("\nAvailable Body Areas :", " / ".join(filted_areas))
                fil_input = input("Type Body Area to filter: ").strip().lower()

                if fil_input in [a.lower() for a in filted_areas]:
                    current_filter = fil_input
                else:
                    print("Body Area not found")
            elif choice == "c":
                current_filter = None
            elif choice == "b":
                return
            elif choice.isdigit():
                target_id = int(choice)
                found_ids = [row[0] for row in allexercises]
                if target_id in found_ids:
                    if target_id in selected_exercise_ids:
                        selected_exercise_ids.remove(target_id)
                    else:
                        selected_exercise_ids.append(target_id)
                else:
                    print("Invalid Exercise ID") 
            elif choice == "s":
                break                   
            else:
                print("Please select from the choices available")

        print("")
        savesession = input("Would you like to save this session? type 'y' or 'n'.. ").lower()

        if savesession == "n":
            return
        elif savesession == "y":
            print("")
            getname = input("Please give your Session a name or pressing 'Enter' will name it 'Workout Session'.. ")
            if not getname:
                getname = str("Workout Session")
            
            cur.execute("INSERT INTO Sessions (session_name) VALUES (?)", (getname,))

            new_session_id = cur.lastrowid

            for id in selected_exercise_ids:
                cur.execute("INSERT INTO SessionExercises (session_id, exercise_id) VALUES (?,?)", (new_session_id,id))

            con.commit()
           

    except sqlite3.Error as e:
        print(f"Database Error! {e}")
        input("Press any key to continue..")
        con.rollback()
    finally:
        con.close()

    
    return

def viewsession():

    con = sqlite3.connect('gymapp.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    header()

    cur.execute("SELECT session_id, session_name FROM Sessions")
    
    allsessions = cur.fetchall()

    if not allsessions:
        input("No Sessions found!, press any key to return to main menu..")
        con.close()
        return header()

    print("ID\tSession Name")
    print("")

    for session_id, session_name in allsessions:
        print("{:<8}{:<20}".format(session_id,session_name))

    print("" * 3)    

    validids = [row[0] for row in allsessions]

    try: 
        showsession = int(input("Please enter the ID of the session to view.. "))
        print("")
    except ValueError:
        print("")
        input("Please use a ID number listed, press any key to continue..")
        con.close()
        return viewsession()

    if showsession not in validids:
        input("Please enter a valid ID, press any key to continue..")
        con.close()
        return viewsession()

    
    
    cur.execute("""SELECT
                s.session_name,
                e.exercise_name
                FROM Sessions s
                LEFT JOIN SessionExercises se ON se.session_id = s.session_id
                LEFT JOIN Exercises e ON se.exercise_id = e.exercise_id
                WHERE s.session_id = ? 
                """, (showsession,))

    exercisematch = cur.fetchall()

    if exercisematch[0][1] is None:
        input("There are no Exercises listed for this session, press any key to return.. ")
        con.close()
        return header()
    else:
        print(f"The following exercises for {exercisematch[0][0]}:")
        print("")
        for row in exercisematch:
            print(row[1])

    print("")
    choice = input("Please make a selection 'v' to view another, 'b' back to go main menu,\n'd' to delete this session or 't' to start training.. ").strip().lower()

    while choice != "v" or "b" or "d" or "t":
        if choice == "v":
            con.close()
            return viewsession()
        elif choice == "b":
            con.close()
            return header()
        elif choice == "d":
            checkdel = input("Are you sure you want to delete this session? 'y' or 'n'.. ").lower()
            if checkdel == "y":
                cur.execute("DELETE FROM Sessions WHERE session_id=?", (showsession,))
                con.commit()
                return
            else:
                return
        elif choice == "t":
            con.close()
            return training(showsession)

        else:
            print("")
            input("Please enter a valid choice, press any key to retry.. ")
            con.close()
            return viewsession()

def pretraining():
        
    con = sqlite3.connect('gymapp.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    header()
    
    cur.execute("SELECT session_id, session_name FROM Sessions")
        
    allsessions = cur.fetchall()
    
    if not allsessions:
        input("No Sessions found!, press any key to return to main menu..")
        con.close()
        return header()
    
    print("ID\tSession Name")
    print("")
    
    for session_id, session_name in allsessions:
        print("{:<8}{:<20}".format(session_id,session_name))
    
    print("" * 3)    
    
    validids = [row[0] for row in allsessions]
    
    try: 
        showsession = int(input("Please enter the ID of the session to train.. "))
        print("")
    except ValueError:
        print("")
        input("Please use a ID number listed, press any key to continue..")
        con.close()
        return pretraining()
    
    if showsession not in validids:
        input("Please enter a valid ID, press any key to continue..")
        con.close()
        return pretraining()  

    return training(showsession)      

def training(sessionid):

    header()
    today = date.today().isoformat()

    con = sqlite3.connect('gymapp.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute("INSERT INTO WorkoutHistory (session_id, workout_date) VALUES (?,?)", (sessionid, today))

    currentwoid = cur.lastrowid

    cur.execute("""SELECT
                    e.exercise_id,
                    e.exercise_name
                    FROM SessionExercises se
                    JOIN Exercises e ON se.exercise_id = e.exercise_id
                    WHERE se.session_id = ? 
                    """, (sessionid,))

    sessionex = cur.fetchall()
    

    if not sessionex:
        con.close()
        print("")
        print("There are no Exercises listed on this Session, please add some Exercises.. ")
        return header()

    print("")
    print("Time to start training!")
    print("")

    sets_log = []

    for exercise_id, exercise_name in sessionex:
        header()
        print(f"Exercise: {exercise_name}")
        print("")
        print("For each set enter the reps and weight. Press Enter on reps not used to skip")

        for setnum in range(1,6):
            print("")
            repsinput = input(f"Set No. : {setnum}\tReps completed : ").strip()
            if repsinput == "":
                weightinput = "0.00"
                break
            
            print("")
            weightinput = input(f"Set No. : {setnum}\tWeight lifted : ").strip()

            try:

                reps = int(repsinput)
                weight = float(weightinput)

                sets_log.append((currentwoid, exercise_id, setnum, reps, weight))

            except ValueError:
                input("Invalid entry this set will not count, press any key to continue.")

    if sets_log:

        cur.executemany("""INSERT INTO TrainingLog (
                        wo_history_id, 
                        exercise_id, 
                        sets, 
                        reps, 
                        weight) VALUES (?, ?, ?, ?, ?)""", sets_log 
                        )
        con.commit()

    else:
        print("")
        input("No data was entered training session will be cleared, press any key.. ")
        cur.execute("DELETE FROM WorkoutHistory WHERE wo_history_id = ?", (currentwoid,))
        con.commit()

    header()
    input("Training Session Complete!, Press any key to return to main menu.. ")
    con.close()


def header():
    clear()
    print("----------------------------------------------------------------------------------------------------------")
    print("|                                          WELCOME TO GYM APP                                            |")
    print("----------------------------------------------------------------------------------------------------------")
    print("")
    return

def mainmenu():
    print("[1] VIEW / ADD / DELETE EXERCISES                            [5]")
    print("")
    print("[2] CREATE A NEW GYM SESSION                                 [6]")
    print("")
    print("[3] VIEW / DELETE A GYM SESSION                              [7]")
    print("")
    print("[4] START TRAINING                                           [8]")
    print("""
        """ * 20)

    choice = input("Please make a selection, or 'q' to Quit.. ").lower()
    
    while choice != 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or q:
        if choice == "1":
            exercise()
        elif choice == "2":
            newsession()
        elif choice == "3":
            viewsession()
        elif choice == "4":
            pretraining()
        elif choice == "5":
            header()
        elif choice == "6":
            header()
        elif choice == "7":
            header()
        elif choice == "8":
            header()
        elif choice == "q":
            quit()
        else: input("Please press 1 - 8 or 'q', press any key to acknowledge...").lower()
        clear()
        header()
        mainmenu()


file_exists = os.path.exists('gymapp.db')

if file_exists:
    header()
    mainmenu()
else:
    clear()
    input("Database not found in app directory, Press any key to create new database.. ")
    createdatabase()
    print("")
    input("Database created, press any key to run Gym App.. ")
    header()
    mainmenu()
