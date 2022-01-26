from tkinter import * 
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessagebox

root = Tk()
root.title('Library Book Management System')

def Database():
    global con,cursor
    con = sqlite3.connect('books.db')
    cursor = con.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS library(mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, bookname TEXT, author TEXT, year_of_publication INTEGER, isbn INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS issued(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, bookname TEXT, author TEXT, year_of_publication INTEGER, isbn INTEGER)')
    

def Add():
    if BOOKNAME.get()=='' or AUTHOR.get() == '' or YEAR_OF_PUBLICATION.get() == '' or ISBN.get() == '':
        txt_result.config(text='Please enter all fields',fg='red')
    else:
        Database()
        cursor.execute('INSERT INTO library(bookname,author,year_of_publication,isbn) VALUES(?,?,?,?)',(str(BOOKNAME.get()),str(AUTHOR.get()),str(YEAR_OF_PUBLICATION.get()),str(ISBN.get())))
        con.commit()
        BOOKNAME.set('')
        AUTHOR.set('')
        YEAR_OF_PUBLICATION.set('')
        ISBN.set('')
        cursor.close()
        con.close()
        txt_result.config(text='Entry successful!',fg='green')
        
def Display():
    tree.delete(*tree.get_children())
    Database()
    cursor.execute('SELECT * FROM library ORDER BY mem_id ASC')
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('','end',values=(data[0],data[1],data[2],data[3],data[4]))
    cursor.close()
    txt_result.config(text='Successfully fetched data!',fg='black')
        
def Search():
    if BOOKNAME.get()=='' and AUTHOR.get() == '' and YEAR_OF_PUBLICATION.get() == '' and ISBN.get() == '':
        txt_result.config(text='Please enter the fields',fg='red')
    else:
        tree.delete(*tree.get_children())
        Database()
        cursor.execute('SELECT * FROM library where bookname = ? or author = ? or year_of_publication = ? or isbn = ?',(BOOKNAME.get(),AUTHOR.get(),YEAR_OF_PUBLICATION.get(),ISBN.get()))
        rows = cursor.fetchall()
        for data in rows:
            tree.insert('','end',values=(data[0],data[1],data[2],data[3],data[4]))
        cursor.close()
        txt_result.config(text='Successfully searched data!',fg='black')

def Issue():
    if not tree.selection():
        txt_result.config(text="Please select an item first", fg="red")
    else:
        Database()
        tree.delete(*tree.get_children())
        tree1.delete(*tree1.get_children())
        cursor.execute('INSERT INTO issued(bookname,author,year_of_publication,isbn) VALUES(?,?,?,?)',(str(BOOKNAME.get()),str(AUTHOR.get()),str(YEAR_OF_PUBLICATION.get()),str(ISBN.get())))
        con.commit()
        cursor.execute("SELECT * FROM `issued` ORDER BY id ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree1.insert('', 'end', values=(data[0],data[1], data[2], data[3], data[4]))
        cursor.close()
        con.close()
        BOOKNAME.set('')
        AUTHOR.set('')
        YEAR_OF_PUBLICATION.set('')
        ISBN.set('')
        btn_add.config(state=NORMAL)
        btn_display.config(state=NORMAL)
        btn_displayissued.config(state=NORMAL)
        btn_search.config(state=NORMAL)
        btn_issue.config(state=NORMAL)
        btn_delete.config(state=NORMAL)    
        txt_result.config(text="Successfully issued the book!", fg="black")
    

def DisplayIssued():
    
    Database()
    tree.delete(*tree.get_children())
    tree1.delete(*tree1.get_children())
    cursor.execute('SELECT * FROM issued ORDER BY id ASC')
    con.commit()
    fetch = cursor.fetchall()
    for data in fetch:
        tree1.insert('', 'end', values=(data[0],data[1], data[2], data[3], data[4]))
    txt_result.config(text='Successfully displayed issued books!',fg='black')
    cursor.close()
    con.close()
    BOOKNAME.set('')
    AUTHOR.set('')
    YEAR_OF_PUBLICATION.set('')
    ISBN.set('')
    btn_add.config(state=NORMAL)
    btn_display.config(state=NORMAL)
    btn_displayissued.config(state=NORMAL)
    btn_search.config(state=NORMAL)
    btn_issue.config(state=NORMAL)
    btn_delete.config(state=NORMAL)    
    
def OnSelected(event):
    global mem_id,temp;
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    BOOKNAME.set('')
    AUTHOR.set('')
    YEAR_OF_PUBLICATION.set('')
    ISBN.set('')
    BOOKNAME.set(selecteditem[1])
    AUTHOR.set(selecteditem[2])
    YEAR_OF_PUBLICATION.set(selecteditem[3])
    ISBN.set(selecteditem[4])
    btn_add.config(state=DISABLED)
    btn_display.config(state=NORMAL)
    btn_displayissued.config(state=NORMAL)
    btn_search.config(state=NORMAL)
    btn_issue.config(state=NORMAL)
    btn_delete.config(state=NORMAL)
    
def Delete():
    if not tree.selection():
        txt_result.config(text="Please select an item first", fg="red")
    else:
        result = tkMessagebox.askquestion('Library Book Management System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `library` WHERE `mem_id` = %d" % selecteditem[0])
            con.commit()
            cursor.close()
            con.close()
            txt_result.config(text="Successfully deleted the data!", fg="black")

def Exit():
    result = tkMessagebox.askquestion('Library Book Management System','Do you want to exit ? (y/n)',icon='warning')
    if result == 'yes':
        root.destroy()
        exit()