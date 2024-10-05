#!/usr/bin/env python
# coding: utf-8

# In[7]:


from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
import time
import sqlite3
import re

try:
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("create table acn(acn_no integer primary key autoincrement,acn_name text,acn_pass text,acn_email text,acn_mob text,acn_bal float,acn_opendate text,acn_gender text)")
    conobj.close()
    print("table created")
except:
    print("something went wrong","Might be table already exist")
win=Tk()
win.state('zoomed')
win.configure(bg='pink')
win.resizable(width=False,height=False)
title=Label(win,text="Banking Automation",font=("arial",50,'bold','underline'),bg='pink')
title.pack()
dt=time.strftime("%d-%b-%Y")
date=Label(win,text=f"{dt}",font=('arial',20,'bold'),bg='pink',fg='blue')
date.place(relx=.85,rely=.1)

def main_screen():
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def forgotpass():
        frm.destroy()
        forgotpass_screen()

    def newuser():
        frm.destroy()
        newuser_screen()

    def login():
        global gacn
        gacn=e_acn.get()
        pwd=e_pass.get()
        if len(gacn)==0 or len(pwd)==0:
            messagebox.showwarning("Validation","EMPTY FEILDS ARE NOT ALLOWED")
            return
        else:

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select * from acn where acn_no=? and acn_pass=?",(gacn,pwd))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Login","Invalid acn or password")
            else:
                frm.destroy()
                welcome_screen()
                

    def clear():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()
    
    lbl_acn=Label(frm,text='ACN NO',font=('arial',20,'bold'),bg='powder blue')
    lbl_acn.place(relx=.3,rely=.1)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.6,rely=.1)
    e_acn.focus()

    lbl_pass=Label(frm,text='pass',font=('arial',20,'bold'),bg='powder blue')
    lbl_pass.place(relx=.3,rely=.2)

    e_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    e_pass.place(relx=.6,rely=.2)

    btn_login=Button(frm,text='LOGIN',font=('arial',20,'bold'),bd=5,command=login)
    btn_login.place(relx=.4,rely=.3)

    btn_clear=Button(frm,command=clear,text='CLEAR',font=('arial',20,'bold'),bd=5)
    btn_clear.place(relx=.5,rely=.3)

    btn_fp=Button(frm,command=forgotpass,width=15,text='Forgot Password',font=('arial',20,'bold'),bd=5)
    btn_fp.place(relx=.4,rely=.42)

    btn_new=Button(frm,command=newuser,width=15,text='Open New Account',font=('arial',20,'bold'),bd=5)
    btn_new.place(relx=.4,rely=.52)

def forgotpass_screen():
    frm=Frame(win)
    frm.configure(bg='green')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def back():
        frm.destroy()
        main_screen()

    def forgotpass_db():
        acn=e_acn.get()
        email=e_email.get()
        mob=e_mob.get()

        if len(acn)==0 and len(email)==0 and len(mob)==0:
            messagebox.showwarning("Submit","Empty feilds are not allowed")
            return

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_pass from acn where acn_no=? and acn_email=? and acn_mob=?",(acn,email,mob))
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showerror("FORGOT PASS","Record Not Found")
        else:
            messagebox.showinfo("Forgot Pass",f"your password={tup[0]}")
        e_acn.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_acn.focus()
        conobj.close()
    def clear():
        e_acn.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_acn.focus()
        
    btn_new=Button(frm,command=back,text='back',font=('arial',20,'bold'),bd=5)
    btn_new.place(relx=0,rely=0)

    lbl_acn=Label(frm,text='ACN',font=('arial',20,'bold'),bg='powder blue')
    lbl_acn.place(relx=.3,rely=.1)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.6,rely=.1)
    e_acn.focus()

    lbl_email=Label(frm,text='EMAIL',font=('arial',20,'bold'),bg='powder blue')
    lbl_email.place(relx=.3,rely=.2)

    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=.6,rely=.2)

    lbl_mob=Label(frm,text='Mob no',font=('arial',20,'bold'),bg='powder blue')
    lbl_mob.place(relx=.3,rely=.3)

    e_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mob.place(relx=.6,rely=.3)

    btn_new=Button(frm,command=forgotpass_db,text='Submit',font=('arial',20,'bold'),bd=5)
    btn_new.place(relx=.6,rely=.4)

    btn_clear=Button(frm,command=clear,text='Clear',font=('arial',20,'bold'),bd=5)
    btn_clear.place(relx=.7,rely=.4)

def newuser_screen():
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def back():
        frm.destroy()
        main_screen()

    def newuser_db():
        name=e_name.get()
        pwd=e_pass.get()
        email=e_email.get()
        mob=e_mob.get()
        gender=cb_gender.get()
        bal=0
        opendate=time.strftime("%d-%b-%Y")

        if len(name)==0 and len(pwd)==0 and len(email)==0 and len(mob)==0 and len(gender)==0:
            messagebox.showwarning("submit","EMPTY FEILDS ARE NOT ALLOWED")
            return

        match=re.fullmatch("[a-zA-Z0-9_]+@[a-zA-Z0-9]+\.[a-zA-Z]+",email)
        if match==None:
            messagebox.showwarning("Validation","Invalid gmail")
            return

        match=re.fullmatch("[6-9][0-9]{9}",mob)
        if match==None:
            messagebox.showwarning("Validation","Invalid Mobile NO")
            return

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("insert into acn(acn_name,acn_pass,acn_email,acn_mob,acn_bal,acn_opendate,acn_gender) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,bal,opendate,gender))
        conobj.commit()
        conobj.close()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select max(acn_no) from acn")
        tup=curobj.fetchone()
        conobj.close()

        messagebox.showinfo("New User",f"account created succesfully acn no={tup[0]}")
        e_name.delete(0,"end")
        e_pass.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        cb_gender.delete(0,"end")
        
        

    def clear():
        e_name.delete(0,"end")
        e_email.delete(0,"end")
        e_pass.delete(0,"end")
        e_mob.delete(0,"end")
        cb_gender.delete(0,"end")

    btn_new=Button(frm,command=back,text='back',font=('arial',20,'bold'),bd=5)
    btn_new.place(relx=.0,rely=0)

    lbl_name=Label(frm,text='user name',font=('arial',20,'bold'),bg='powder blue')
    lbl_name.place(relx=.3,rely=.1)

    e_name=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_name.place(relx=.6,rely=.1)
    e_name.focus()

    lbl_pass=Label(frm,text='Password',font=('arial',20,'bold'),bg='powder blue')
    lbl_pass.place(relx=.3,rely=.2)

    e_pass=Entry(frm,font=('arial',20,'bold'),bd=5,show='*')
    e_pass.place(relx=.6,rely=.2)

    lbl_email=Label(frm,text='EMAIL',font=('arial',20,'bold'),bg='powder blue')
    lbl_email.place(relx=.3,rely=.3)

    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=.6,rely=.3)

    lbl_mob=Label(frm,text='Mob no',font=('arial',20,'bold'),bg='powder blue')
    lbl_mob.place(relx=.3,rely=.4)

    e_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mob.place(relx=.6,rely=.4)

    lbl_gender=Label(frm,text='gender',font=('arial',20,'bold'),bg='powder blue')
    lbl_gender.place(relx=.3,rely=.5)

    cb_gender=Combobox(frm,values=['-------select-------','male','female'],font=('arial',20,'bold'))
    cb_gender.place(relx=.6,rely=.5)
    
    btn_new=Button(frm,command=newuser_db,text='Submit',font=('arial',20,'bold'))
    btn_new.place(relx=.6,rely=.6)

    btn_clear=Button(frm,text='Clear',font=('arial',20,'bold'))
    btn_clear.place(relx=.7,rely=.6)

def welcome_screen():
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def logout():
        frm.destroy()
        main_screen()

    def details():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        lbl_wel=Label(ifrm,text='this is details screen',font=('arial',20,'bold'),bg='white',fg='blue')
        lbl_wel.pack()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_name,acn_opendate,acn_bal,acn_gender,acn_email,acn_mob from acn where acn_no=?",(gacn))
        tup=curobj.fetchone()

        lbl_name=Label(ifrm,text=f"Owner Name:{tup[0]}",font=('arial',20,'bold'),bg='white')
        lbl_name.place(relx=0,rely=.1)

        lbl_opendate=Label(ifrm,text=f"Open Date:{tup[1]}",font=('arial',20,'bold'),bg='white')
        lbl_opendate.place(relx=0,rely=.2)

        lbl_bal=Label(ifrm,text=f"Available Balance:{tup[2]}",font=('arial',20,'bold'),bg='white')
        lbl_bal.place(relx=0,rely=.3)

        lbl_gender=Label(ifrm,text=f"Gender:{tup[3]}",font=('arial',20,'bold'),bg='white')
        lbl_gender.place(relx=0,rely=.4)

        lbl_email=Label(ifrm,text=f"Email:{tup[4]}",font=('arial',20,'bold'),bg='white')
        lbl_email.place(relx=0,rely=.5)

        lbl_mob=Label(ifrm,text=f"Mobile NO:{tup[5]}",font=('arial',20,'bold'),bg='white')
        lbl_mob.place(relx=0,rely=.6)
        
        conobj.close()

    def update():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_name,acn_pass,acn_email,acn_mob from acn")
        tup=curobj.fetchone()
        conobj.close()

        lbl_wel=Label(ifrm,text='this is update screen',font=('arial',20,'bold'),bg='white',fg='blue')
        lbl_wel.pack()

        lbl_name=Label(ifrm,text='user name',font=('arial',20,'bold'),bg='powder blue')
        lbl_name.place(relx=.1,rely=.2)
    
        e_name=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_name.place(relx=.1,rely=.3)
        e_name.insert(0,tup[0])
        e_name.focus()
    
        lbl_pass=Label(ifrm,text='Password',font=('arial',20,'bold'),bg='powder blue')
        lbl_pass.place(relx=.1,rely=.5)
    
        e_pass=Entry(ifrm,font=('arial',20,'bold'),bd=5,show='*')
        e_pass.place(relx=.1,rely=.6)
        e_pass.insert(0,tup[1])
        
        lbl_email=Label(ifrm,text='EMAIL',font=('arial',20,'bold'),bg='powder blue')
        lbl_email.place(relx=.4,rely=.2)
    
        e_email=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_email.place(relx=.4,rely=.3)
        e_email.insert(0,tup[2])
    
        lbl_mob=Label(ifrm,text='Mob no',font=('arial',20,'bold'),bg='powder blue')
        lbl_mob.place(relx=.4,rely=.5)
    
        e_mob=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_mob.place(relx=.4,rely=.6)
        e_mob.insert(0,tup[3])

        def update_db():
            name=e_name.get()
            pwd=e_pass.get()
            email=e_email.get()
            mob=e_mob.get()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update acn set acn_name=?,acn_pass=?,acn_email=?,acn_mob=? where acn_no=?",(name,pwd,email,mob,gacn))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Updated","Record Updated Succesfully")
            welcome_screen()

        btn_update=Button(ifrm,command=update_db,text="Update",font=('arial',20,'bold'))
        btn_update.place(relx=.8,rely=.8)
        

    def deposit():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        lbl_wel=Label(ifrm,text='this is deposit screen',font=('arial',20,'bold'),bg='white',fg='blue')
        lbl_wel.pack()

        lbl_amt=Label(ifrm,text='Amount',font=('arial',20,'bold'),bg='white')
        lbl_amt.place(relx=0.2,rely=0.2)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.2)
        e_amt.focus()

        def deposit_db():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update acn set acn_bal=acn_bal+? where acn_no=?",(amt,gacn))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Deposit",f"{amt} rupees credited to your account")
            e_amt.delete(0,"end")

        btn_deposit=Button(ifrm,command=deposit_db,text="Deposit",font=('arial',20,'bold'))
        btn_deposit.place(relx=.8,rely=.8)
    

    def withdraw():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        lbl_wel=Label(ifrm,text='this is withdraw screen',font=('arial',20,'bold'),bg='white',fg='blue')
        lbl_wel.pack()

        lbl_wdr=Label(ifrm,text='Amount',font=('arial',20,'bold'),bg='white')
        lbl_wdr.place(relx=0.2,rely=0.2)

        e_wdr=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_wdr.place(relx=.4,rely=.2)
        e_wdr.focus()

        def withdraw_db():
            amt=float(e_wdr.get())

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from acn where acn_no=?",(gacn,))
            tup=curobj.fetchone()
            avail_bal=tup[0]
            conobj.close()

            if avail_bal>=amt:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("update acn set acn_bal=acn_bal-? where acn_no=?",(amt,gacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Withdraw",f"{amt} rupees debited from your account")
                e_wdr.delete(0,"end")
            else:
                messagebox.showerror("Withdraw","Insufficient Balance")
                e_wdr.delete(0,"end")

        btn_withdraw=Button(ifrm,command=withdraw_db,text="Withdraw",font=('arial',20,'bold'))
        btn_withdraw.place(relx=.8,rely=.8)

    def transfer():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        lbl_wel=Label(ifrm,text='this is transfer screen',font=('arial',20,'bold'),bg='white',fg='blue')
        lbl_wel.pack()

        lbl_to=Label(ifrm,text='TO',font=('arial',20,'bold'),bg='white')
        lbl_to.place(relx=0.1,rely=0.2)

        e_to=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_to.place(relx=.4,rely=.2)
        e_to.focus()

        lbl_amt=Label(ifrm,text='Amount',font=('arial',20,'bold'),bg='white')
        lbl_amt.place(relx=0.1,rely=0.4)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.4)

        def transfer_db():
            to_acn=e_to.get()
            amt=float(e_amt.get())

            if to_acn==gacn:
                messagebox.showwarning("Transfer","Both to Account and senders account cannot be same")
                return
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from acn where acn_no=?",(gacn,))
            tup=curobj.fetchone()
            avail_bal=tup[0]
            conobj.close()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_no from acn where acn_no=?",(to_acn))
            tup=curobj.fetchone()
            conobj.close()

            if tup==None:
                messagebox.showwarning("Transfer","Recievers account no is not correct")
                return
            if avail_bal>=amt:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("update acn set acn_bal=acn_bal+? where acn_no=?",(amt,to_acn))
                curobj.execute("update acn set acn_bal=acn_bal-? where acn_no=?",(amt,gacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Transfer",f"{amt} Amount transfered to {to_acn} succesfully")
            

        btn_transfer=Button(ifrm,command=transfer_db,text="Transfer",font=('arial',20,'bold'))
        btn_transfer.place(relx=.8,rely=.8)

 
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("select acn_name from acn where acn_no=?",(gacn,))
    tup=curobj.fetchone()
    conobj.close()
    
    lbl_wel=Label(frm,text=f"welcome,{tup[0]}",font=('arial',20,'bold'),bg='powder blue')
    lbl_wel.place(relx=0,rely=0)

    btn_logout=Button(frm,text='Logout',font=('arial',20,'bold'),command=logout)
    btn_logout.place(relx=.88,rely=0)

    btn_details=Button(frm,command=details,text='details',font=('arial',20,'bold'))
    btn_details.place(relx=0,rely=.1)

    btn_update=Button(frm,command=update,text='update',font=('arial',20,'bold'))
    btn_update.place(relx=0,rely=.2)

    btn_deposit=Button(frm,command=deposit,text='deposit',font=('arial',20,'bold'))
    btn_deposit.place(relx=0,rely=.3)

    btn_withdraw=Button(frm,command=withdraw,text='withdraw',font=('arial',20,'bold'))
    btn_withdraw.place(relx=0,rely=.4)

    btn_transfer=Button(frm,command=transfer,text='transfer',font=('arial',20,'bold'))
    btn_transfer.place(relx=0,rely=.5)


main_screen()

win.mainloop()


# # import sqlite3
# conobj=sqlite3.connect(database="bank.sqlite")
# curobj=conobj.cursor()
# curobj.execute("select max(acn_no) from acn")
# tup=curobj.fetchone()
# print(tup[0])
# conobj.commit()
# conobj.close()

# In[11]:


import sqlite3
conobj=sqlite3.connect(database="bank.sqlite")
curobj=conobj.cursor()
curobj.execute("select * from acn")
print(curobj.fetchall())
conobj.commit()
conobj.close()


# In[ ]:




