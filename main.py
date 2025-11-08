import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

books = {}
users = {}

def add_book():
    book_id_text = book_id_entry.get()
    title = title_entry.get()
    author = author_entry.get()

    if book_id_text == "" or title == "" or author == "":
        messagebox.showerror("Error", "Please fill all fields!")
        return
    try:
        book_id = int(book_id_text)
    except:
        messagebox.showerror("Error", "Book ID should be a number!")
        return
    if book_id in books:
        messagebox.showerror("Error", "This Book ID already used!")
        return

    books[book_id] = {"title": title, "author": author, "issued": False}
    messagebox.showinfo("Success", "Book added!")
    book_id_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)

def register_user():
    user_id_text = user_id_entry.get()
    name = user_name_entry.get()

    if user_id_text == "" or name == "":
        messagebox.showerror("Error", "Please fill all fields!")
        return
    try:
        user_id = int(user_id_text)
    except:
        messagebox.showerror("Error", "User ID should be a number!")
        return
    if user_id in users:
        messagebox.showerror("Error", "This User ID already exists!")
        return

    users[user_id] = {"name": name, "borrowed": {}}
    messagebox.showinfo("Success", "User registered!")
    user_id_entry.delete(0, tk.END)
    user_name_entry.delete(0, tk.END)

def issue_book():
    book_id_text = issue_book_id_entry.get()
    user_id_text = issue_user_id_entry.get()

    if book_id_text == "" or user_id_text == "":
        messagebox.showerror("Error", "Please enter both IDs!")
        retur
    try:
        book_id = int(book_id_text)
        user_id = int(user_id_text)
    except:
        messagebox.showerror("Error", "IDs should be numbers!")
        return
    if book_id not in books:
        messagebox.showerror("Error", "Book not found!")
    elif user_id not in users:
        messagebox.showerror("Error", "User not found!")
    elif books[book_id]["issued"] == True:
        messagebox.showerror("Error", "Book is already issued!")
    else:
        books[book_id]["issued"] = True
        due_date = datetime.now() + timedelta(days=14)
        users[user_id]["borrowed"][book_id] = due_date
        messagebox.showinfo("Success", "Book issued. Due "+str(due_date.date()))
        issue_book_id_entry.delete(0, tk.END)
        issue_user_id_entry.delete(0, tk.END)

def return_book():
    book_id_text = return_book_id_entry.get()
    user_id_text = return_user_id_entry.get()

    if book_id_text == "" or user_id_text == "":
        messagebox.showerror("Error", "Please enter both IDs!")
        return
    try:
        book_id = int(book_id_text)
        user_id = int(user_id_text)
    except:
        messagebox.showerror("Error", "IDs should be numbers!")
        return
    if user_id not in users:
        messagebox.showerror("Error", "User not found!")
        return
    if book_id not in users[user_id]["borrowed"]:
        messagebox.showerror("Error", "This user didn't borrow this book!")
        return

    due_date = users[user_id]["borrowed"][book_id]
    del users[user_id]["borrowed"][book_id]
    books[book_id]["issued"] = False
    return_date = datetime.now()
    fine = 0
    if return_date > due_date:
        delta = return_date - due_date
        fine = delta.days * 10
    messagebox.showinfo("Book Returned", "Book returned!\nFine: "+str(fine))
    return_book_id_entry.delete(0, tk.END)
    return_user_id_entry.delete(0, tk.END)

def show_books():
    all_books = ""
    for b in books:
        status = "Issued" if books[b]["issued"] else "Available"
        all_books += "ID:"+str(b)+" Title:"+books[b]["title"]+" Author:"+books[b]["author"]+" Status:"+status+"\n"
    if all_books == "":
        all_books = "No books in library yet."
    messagebox.showinfo("Books List", all_books)

def show_users():
    all_users = ""
    for u in users:
        borrowed = users[u]["borrowed"]
        bor_str = ""
        if len(borrowed) == 0:
            bor_str = "None"
        else:
            for bk_id in borrowed:
                bor_str += str(bk_id)+"(due "+str(borrowed[bk_id].date())+"), "
            bor_str = bor_str[:-2]  # last comma remove
        all_users += "ID:"+str(u)+" Name:"+users[u]["name"]+" Borrowed: "+bor_str+"\n"
    if all_users == "":
        all_users = "No users registered yet."
    messagebox.showinfo("Users List", all_users)
window = tk.Tk()
window.title("Python Project - Library ManagementSystem")

# Add Book 
tk.Label(window, text="Add Book").grid(row=0, column=0, columnspan=2)

tk.Label(window, text="Book ID").grid(row=1, column=0)
book_id_entry = tk.Entry(window)
book_id_entry.grid(row=1, column=1)

tk.Label(window, text="Title").grid(row=2, column=0)
title_entry = tk.Entry(window)
title_entry.grid(row=2, column=1)

tk.Label(window, text="Author").grid(row=3, column=0)
author_entry = tk.Entry(window)
author_entry.grid(row=3, column=1)

tk.Button(window, text="Add", command=add_book).grid(row=4, column=0, columnspan=2)

# Register User 
tk.Label(window, text="Register User").grid(row=5, column=0, columnspan=2)

tk.Label(window, text="User ID").grid(row=6, column=0)
user_id_entry = tk.Entry(window)
user_id_entry.grid(row=6, column=1)

tk.Label(window, text="Name").grid(row=7, column=0)
user_name_entry = tk.Entry(window)
user_name_entry.grid(row=7, column=1)

tk.Button(window, text="Register", command=register_user).grid(row=8, column=0, columnspan=2)

# Issue Book 
tk.Label(window, text="Issue Book").grid(row=9, column=0, columnspan=2)

tk.Label(window, text="Book ID").grid(row=10, column=0)
issue_book_id_entry = tk.Entry(window)
issue_book_id_entry.grid(row=10, column=1)

tk.Label(window, text="User ID").grid(row=11, column=0)
issue_user_id_entry = tk.Entry(window)
issue_user_id_entry.grid(row=11, column=1)

tk.Button(window, text="Issue", command=issue_book).grid(row=12, column=0, columnspan=2)

# Return Boo
tk.Label(window, text="Return Book").grid(row=13, column=0, columnspan=2)

tk.Label(window, text="Book ID").grid(row=14, column=0)
return_book_id_entry = tk.Entry(window)
return_book_id_entry.grid(row=14, column=1)

tk.Label(window, text="User ID").grid(row=15, column=0)
return_user_id_entry = tk.Entry(window)
return_user_id_entry.grid(row=15, column=1)

tk.Button(window, text="Return", command=return_book).grid(row=16, column=0, columnspan=2)

# Show buttons and credits
tk.Button(window, text="Show Books", command=show_books).grid(row=17, column=0)
tk.Button(window, text="Show Users", command=show_users).grid(row=17, column=1)
tk.Label(window, text="Made by: Kaavya K. Rao, 92510133009, EK3").grid(row=18, column=0, columnspan=2)

window.mainloop()
