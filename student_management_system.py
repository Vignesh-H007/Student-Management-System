# student_management_gui.py
# Replace console app with this Tkinter GUI (uses student_info.db / students table)
import sqlite3
import re
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "student_info.db"

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def connect_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
            rollno INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            dept TEXT NOT NULL,
            mobileNo TEXT NOT NULL,
            emailID TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_student(rollno, name, dept, mobile, email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO students(rollno, name, dept, mobileNo, emailID) VALUES (?, ?, ?, ?, ?)",
                (rollno, name, dept, mobile, email))
    conn.commit()
    conn.close()

def update_student(original_roll, new_roll, name, dept, mobile, email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE students
        SET rollno = ?, name = ?, dept = ?, mobileNo = ?, emailID = ?
        WHERE rollno = ?
    """, (new_roll, name, dept, mobile, email, original_roll))
    conn.commit()
    conn.close()

def delete_student(rollno):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE rollno = ?", (rollno,))
    conn.commit()
    conn.close()

def fetch_all_students():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT rollno, name, dept, mobileNo, emailID FROM students ORDER BY rollno")
    rows = cur.fetchall()
    conn.close()
    return rows


def validate_inputs(roll, name, dept, mobile, email):
    
    try:
        r = int(roll)
    except ValueError:
        return False, "Roll number must be an integer."
    if not (1000 <= r <= 9999):
        return False, "Roll number must be between 1000 and 9999."

    if len(name.strip()) == 0 or len(name) > 20:
        return False, "Name must be 1-20 characters."

    if len(dept.strip()) == 0 or len(dept) != 3:
        return False, "Department must be exactly 3 characters (e.g. CSE)."

    if not mobile.isdigit() or len(mobile) != 10:
        return False, "Mobile number must be a 10-digit number."

    if not re.match(EMAIL_REGEX, email):
        return False, "Invalid email address."

    return True, ""

class StudentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("760x520")
        self.root.resizable(False, False)

        
        self.selected_original_roll = None

        
        form_frame = tk.LabelFrame(root, text="Add / Update Student", padx=10, pady=10)
        form_frame.pack(fill="x", padx=12, pady=8)

        
        tk.Label(form_frame, text="Roll No").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.roll_entry = tk.Entry(form_frame, width=18)
        self.roll_entry.grid(row=0, column=1, padx=6, pady=6, sticky="w")

        
        tk.Label(form_frame, text="Name").grid(row=0, column=2, padx=6, pady=6, sticky="w")
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=3, padx=6, pady=6, sticky="w")

       
        tk.Label(form_frame, text="Department").grid(row=1, column=0, padx=6, pady=6, sticky="w")
        self.dept_entry = tk.Entry(form_frame, width=18)
        self.dept_entry.grid(row=1, column=1, padx=6, pady=6, sticky="w")

        
        tk.Label(form_frame, text="Mobile No").grid(row=1, column=2, padx=6, pady=6, sticky="w")
        self.mobile_entry = tk.Entry(form_frame, width=30)
        self.mobile_entry.grid(row=1, column=3, padx=6, pady=6, sticky="w")

        
        tk.Label(form_frame, text="Email ID").grid(row=2, column=0, padx=6, pady=6, sticky="w")
        self.email_entry = tk.Entry(form_frame, width=50)
        self.email_entry.grid(row=2, column=1, columnspan=3, padx=6, pady=6, sticky="w")

        
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=8)

        self.add_btn = tk.Button(btn_frame, text="Add Student", width=14, command=self.add_student)
        self.add_btn.grid(row=0, column=0, padx=6)

        self.update_btn = tk.Button(btn_frame, text="Update Student", width=14, command=self.update_student)
        self.update_btn.grid(row=0, column=1, padx=6)

        self.delete_btn = tk.Button(btn_frame, text="Delete Student", width=14, command=self.delete_student)
        self.delete_btn.grid(row=0, column=2, padx=6)

        self.clear_btn = tk.Button(btn_frame, text="Clear Fields", width=14, command=self.clear_inputs)
        self.clear_btn.grid(row=0, column=3, padx=6)

        
        table_frame = tk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=12, pady=(0,12))

        columns = ("rollno", "name", "dept", "mobile", "email")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)
        self.tree.heading("rollno", text="Roll No")
        self.tree.heading("name", text="Name")
        self.tree.heading("dept", text="Department")
        self.tree.heading("mobile", text="Mobile No")
        self.tree.heading("email", text="Email ID")

        self.tree.column("rollno", width=100, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("dept", width=100, anchor="center")
        self.tree.column("mobile", width=120, anchor="center")
        self.tree.column("email", width=200, anchor="w")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, columnspan=2, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

        
        connect_db()
        self.load_data()

    
    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        rows = fetch_all_students()
        for r in rows:
            self.tree.insert("", tk.END, values=r)

    def clear_inputs(self):
        self.roll_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.dept_entry.delete(0, tk.END)
        self.mobile_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.selected_original_roll = None
        # re-enable Add button if disabled previously
        self.add_btn.config(state="normal")

    def add_student(self):
        roll = self.roll_entry.get().strip()
        name = self.name_entry.get().strip()
        dept = self.dept_entry.get().strip()
        mobile = self.mobile_entry.get().strip()
        email = self.email_entry.get().strip()

        valid, msg = validate_inputs(roll, name, dept, mobile, email)
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return

        try:
            insert_student(int(roll), name, dept, mobile, email)
            messagebox.showinfo("Success", "Student added successfully.")
            self.load_data()
            self.clear_inputs()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Roll number already exists.")

    def on_row_selected(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        # values are (rollno, name, dept, mobile, email)
        self.selected_original_roll = int(values[0])
        self.roll_entry.delete(0, tk.END)
        self.roll_entry.insert(0, values[0])
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])
        self.dept_entry.delete(0, tk.END)
        self.dept_entry.insert(0, values[2])
        self.mobile_entry.delete(0, tk.END)
        self.mobile_entry.insert(0, values[3])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[4])

        # disable add while a row is selected to avoid accidental duplicate insert
        self.add_btn.config(state="normal")

    def update_student(self):
        if self.selected_original_roll is None:
            messagebox.showerror("Error", "Select a record from the table to update.")
            return

        new_roll = self.roll_entry.get().strip()
        name = self.name_entry.get().strip()
        dept = self.dept_entry.get().strip()
        mobile = self.mobile_entry.get().strip()
        email = self.email_entry.get().strip()

        valid, msg = validate_inputs(new_roll, name, dept, mobile, email)
        if not valid:
            messagebox.showerror("Validation Error", msg)
            return

        try:
            # If new_roll differs and already exists, this will raise IntegrityError
            update_student(self.selected_original_roll, int(new_roll), name, dept, mobile, email)
            messagebox.showinfo("Success", "Student updated successfully.")
            self.load_data()
            self.clear_inputs()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "The new roll number already exists. Choose a different roll number.")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a record from the table to delete.")
            return
        values = self.tree.item(selected[0], "values")
        roll = int(values[0])

        confirm = messagebox.askyesno("Confirm Delete", f"Delete student with roll no {roll}?")
        if not confirm:
            return
        delete_student(roll)
        messagebox.showinfo("Deleted", "Record deleted successfully.")
        self.load_data()
        self.clear_inputs()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentGUI(root)
    root.mainloop()