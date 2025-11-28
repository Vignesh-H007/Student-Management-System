# Student Management System (Python + Tkinter + SQLite3)

A fully functional **Student Management System** built using  
**Python (Tkinter GUI) + SQLite3 Database**.

This is the **upgraded version** of the previous console-based program.  
Now includes a clean graphical interface for easier data entry and management.

---

## 🎯 Features
- Add new student records  
- View all students in a table (Treeview)  
- Update existing student details  
- Delete student records  
- Click a row to auto-fill the update form  
- Full input validation (Roll No, Dept, Mobile, Email, etc.)  
- Permanent storage using SQLite  
- Clean and simple Tkinter interface

---

## 🗂️ Database Table Structure (`students`)
| Field     | Type    | Description |
|-----------|---------|-------------|
| `rollno`  | INTEGER | Unique student ID (Primary Key) |
| `name`    | TEXT    | Student’s name |
| `dept`    | TEXT    | Department (3-letter code) |
| `mobileNo`| TEXT    | 10-digit mobile number |
| `emailID` | TEXT    | Valid email address |

---

## 🚀 How to Run the GUI Version
```bash
python student_management_system_gui.py