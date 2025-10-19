import sqlite3
import re

conn = sqlite3.connect('student_info.db')

cur = conn.cursor()
'''
cur.execute("create table students(rollno INTEGER PRIMARY KEY,name TEXT NOT NULL,dept TEXT NOT NULL,mobileNo TEXT NOT NULL,emailID TEXT NOT NULL)")
print("Table Created!!")
'''
def entry():
    n = int(input("Enter the number of records : "))
    print("Enter Student Details : ")
    for i in range(n):
        print(f"Record : {i+1}")
        rollno = int(input("Enter Student Rollno : "))

        if (rollno >= 1000 and rollno <= 9999):
            pass
        else:
            print("Invalid Value Entered!")

        name = input("Enter Student Name : ")
        if len(name) <= 20:
            pass 
        else: 
            print("Invalid Vallue Entered!")
        
        dept = input("Enter Student Department : ")
        if len(dept) == 3:
            pass
        else:
            print("Invalid Value Entered!")
        
        mobNo = int(input("Enter Student Mobile Number : "))
        if 1000000000 <= mobNo <= 9999999999:
            pass
        else:
            print("Invalid Vallue Entered!")
        
        emailID = input("Enter Student Email-ID : ")
        if re.match(r"^[a-zA-z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",emailID):
            pass
        else:
            print("Invalid Vallue Entered!")
        
        command = "insert into students(rollno,name,dept,mobileNo,emailID) values(?,?,?,?,?)"
        cur.execute(command,(rollno,name,dept,mobNo,emailID))

    result = cur.execute("select * from students")
    for r in result:
        print(f"\n Roll-no : {r[0]} \n Name: {r[1]} \n Department: {r[2]} \n Mobile-No.: {r[3]} \n Email-ID: {r[4]}")

    conn.commit()
    return "Record Inserted Successfully!!"

def del_entry():
    r_no = int(input("Enter Student Rollno : "))
    cmd = f"select * from students where rollno={r_no}"
    result = cur.execute(cmd)
    for r in result:
        print(f"\n Roll-no : {r[0]} \n Name: {r[1]} \n Department: {r[2]} \n Mobile-No.: {r[3]} \n Email-ID: {r[4]}")
    option = input("Is This Record You Wanted To Delete ?(yes/no)")
    if option == "yes":
        cmd = f"delete from students where rollno = {r_no}"
        cur.execute(cmd)
        result = cur.execute("select * from students")
        print("\nAfter Deleting  The Record : ")
        for r in result:
            print(f"\n Roll-no : {r[0]} \n Name: {r[1]} \n Department: {r[2]} \n Mobile-No.: {r[3]} \n Email-ID: {r[4]}")
    elif option == "no":
        print("\nPlease Try Again")

    else:
        print("\nEnter Valid Option(yes/no)")
    
    conn.commit()
    return "Record Deleted Successfully"

while True:
    print("==========================================\n","Welcome to ABC Student Management System","\n==========================================")
    choice = int(input("Select an option to proceed : \n 1. Enter a record \n 2. Delete a record \n 3. Display Records \n 4. Update Record \n 5. Exit \n -->"))
    print("\n==========================================")
    if choice == 1:
        print(entry())
        print("\n==========================================")
    elif choice == 2:
        print(del_entry())
        print("\n==========================================")

    elif choice == 3:
        result = cur.execute("select * from students")
        print("\nDisplaying Records : ")
        for r in result:
            print(f"\n Roll-no : {r[0]} \n Name: {r[1]} \n Department: {r[2]} \n Mobile-No: {r[3]} \n Email-ID: {r[4]} ")
        print("\n==========================================")

    elif choice == 4:
        rno = int(input("Enter Student Rollno To Update : "))
        result = cur.execute(f"select * from students where rollno = {rno}")
        for r in result:
            print(f"\n Roll-no : {r[0]} \n Name: {r[1]} \n Department: {r[2]} \n Mobile-No: {r[3]} \n Email-ID: {r[4]} ")
        ch = input("Enter A Feild To Update(rollno,name,dept,mobileNo,emailID) : ")
        toSet = input("Enter The Value To Update : ")
        feilds = ["rollno","name","dept","mobileNo","emailID"]
        if ch.lower() in feilds:
            cur.execute(f"update students set {ch} = '{toSet}' where rollno = {rno}")
            print("After Updating : ")
            result = cur.execute(f"select * from students where rollno = {rno}")
            for r in result:
                print(f"\n Roll-no : {r[0]} \n Name: {r[1]} \n Department: {r[2]} \n Mobile-No: {r[3]} \n Email-ID: {r[4]} ")
        print("==========================================")
    
    elif choice == 5:
        print("\nExited Successfully!! \n==========================================")
        break

    else:
        print("\nEnter a valid option(1-5)")




conn.close()