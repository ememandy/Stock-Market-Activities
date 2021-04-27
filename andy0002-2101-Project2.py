

#
# Author:        Emem-Akeabasi Andy
#
# Created:       15/04/2021
# Purpose:       Stock Market Activity application using a Tkinter based GUI
# Copyright:     (c) Emem Andy 2021
#
#---------------------------------------------------------------------------


import tkinter as tk
import tkinter.messagebox
from tkcalendar import Calendar
import sqlite3
from tkinter import ttk

#First top level window
class StockEntry:
    def __init__(self, master):
        self.master = master 
        self.master.geometry('1480x750+100+50')
        self.master.title('Activity Entry')
        self.master.configure(background='#A1CDEC')
        self.CreateWidgets()
        
        
    
    def CreateWidgets(self):
        
        Frame1 = tk.Frame(self.master, bg='#A1CDEC') #this is the fram for the application
        Frame1.grid()
        
        #this is the label for the title of the application
        self.mainLabel = tk.Label(Frame1, text="STOCK ACTIVITY ENTRY", bd=2, relief="solid", font=("Lucida Grande", 30, "bold"), fg="black", bg="#990000")
        self.mainLabel.grid(row=0, column=2)
        
        #entry variables
        self.date = tk.StringVar()
        self.symbol = tk.StringVar()
        self.transaction = tk.StringVar()
        self.quantity = tk.StringVar()
        self.price = tk.DoubleVar()
        
        
        
        #these are stock activity entry labels
        
        #stock calendar and entry
        self.calendar = Calendar(Frame1, selectmode = 'day', date_pattern = 'yyyy-mm-dd')
        self.calendar.grid(row=1,column=0)
        self.dateEntry = tk.Label(Frame1, text='')
        self.dateEntry.grid(row=2,column=0)
        self.dateEntry.config(width=22, relief=tk.RIDGE)
        
        #stock symbol label
        self.symLabel = tk.Label(Frame1, text="Stock Symbol", font=("Gothic Bold", 18, 'bold'), fg="#333333") 
        self.symLabel.grid(row=1,column=1)
        self.symEntry = tk.Entry(Frame1, textvariable=self.symbol)
        self.symEntry.grid(row=2,column=1)
        self.symEntry.config(width=25, relief=tk.RIDGE)
        
        #transaction type label
        self.transLabel = tk.Label(Frame1, text="Transaction (BUY/SELL)", font=("Gothic Bold", 18, 'bold'), fg="#333333") 
        self.transLabel.grid(row=1, column=2)
        self.transEntry = tk.Entry(Frame1, textvariable=self.transaction)
        self.transEntry.grid(row=2,column=2)
        self.transEntry.config(width=25, relief=tk.RIDGE)
        
        #stock quantity label
        self.quantLabel = tk.Label(Frame1, text="Quantity", font=("Gothic Bold", 18, 'bold'), fg="#333333") 
        self.quantLabel.grid(row=1,column=4)
        self.quantEntry = tk.Entry(Frame1,  textvariable=self.quantity)
        self.quantEntry.grid(row=2,column=4)
        self.quantEntry.config(width=25, relief=tk.RIDGE)
        
        #transacted stock price label
        self.priceLabel = tk.Label(Frame1, text="Price", font=("Gothic Bold", 18, 'bold'), fg="#333333") 
        self.priceLabel.grid(row=1, column=9)
        self.priceEntry = tk.Entry(Frame1, textvariable=self.price)
        self.priceEntry.grid(row=2,column=9)
        self.priceEntry.config(width=25, relief=tk.RIDGE)
        
            
        
        #Date selection
        def SelectDate():
            self.date = self.calendar.get_date()
            self.dateEntry.config(text=self.date)  
        
        
        #this adds user entry to the database
        def Record():
            Item1 = self.symbol.get()
            Item2 = self.transaction.get()
            Item3 = self.quantity.get()
            #Item4 = isinstance(self.price.get(),float) 
            
            if (Item1.isalpha() and Item2.isalpha() and Item3.isdigit() and isinstance(self.price.get(),float)):
                
                tkinter.messagebox.showinfo("Correct Date Entires", "Saved Successfully in Stocks Database")
                #self.valid_message.config(text="Saved Successfully in Stocks Database")
                
                #Creates a database or connects to one  
                conn = sqlite3.connect('stocks.db')
        
                #Create cursor
                c = conn.cursor()
            
                #Insert to stocks table
                c.execute("INSERT INTO stocks VALUES (:date, :symbol, :transaction, :quantity, :price)",
                         {
                             'date': self.calendar.get_date(),
                             'symbol': self.symbol.get(),
                             'transaction': self.transaction.get(),
                             'quantity': self.quantity.get(),
                             'price': round(self.price.get(),2)
                         })
            
            
                #Commit changes
                conn.commit()
            
                #Clse connection
                conn.close()  
                return True
            else:
                tkinter.messagebox.showwarning("Wrong Data", "Invalid data input")
                self.symbol.set('')
                self.transaction.set('')
                self.quantity.set(0)
                self.price.set(0.0)
                return False
                    
                
        #Create searches function that searches the database and displays on the screen
        def Search():
            #Creates a database or connects to one  
            conn = sqlite3.connect('stocks.db')
        
            #Create cursor
            c = conn.cursor()
            
            
                
            #stocks table cloumns
            colns = (self.calendar.get_date(), self.symbol.get(), self.transaction.get(), self.quantity.get(), round(self.price.get(),2))
            
            #Query the database
            c.execute("SELECT * FROM stocks WHERE date=? AND symbol=? AND trans=? AND quantity=? AND price=?", colns)
            records = c.fetchall()

            if not records:
                tkinter.messagebox.showwarning("Wrong Search", "Search returned nothing on search")

            else:
                #Loop through results
                print_records = ''
                for record in records:
                    print_records += str(record[0]) + "  " + str(record[1]) + "  " + str(record[2]) + "   " + str(record[3]) + "  " + "$" + str(record[4]) + "\n"
            
            
                #this displays the result from the search button clicked
                self.queryLabel = tk.Label(Frame1, text=print_records, font=("Lucida Grande", 17, 'bold'), fg="#333333")
                self.queryLabel.grid(row=11, column=0, columnspan=14)
            
                #Close Connection
                conn.close()
            
                
                
           
        #Resets the user input entry
        def Reset():
            self.symbol.set('')
            self.transaction.set('')
            self.quantity.set(0)
            self.price.set(0.0)
    
                
        #this creates an exported txt file of stock activities
        def ExportTxt():
            
            #Creates a database or connects to one  
            conn = sqlite3.connect('stocks.db')
        
            #Create cursor
            c = conn.cursor()
            
            c.execute("SELECT DISTINCT date, symbol, trans, quantity, price FROM stocks WHERE quantity > 0 ORDER BY date DESC")
            exp_txt = c.fetchall()
            
            self.text_file = open('stock_activity.txt', 'w')
            
            #Loop through records
            txt_line = ''
            for line in exp_txt:
                txt_line += "User Activity: " + " " + str(line[0]) + "  " + str(line[1]) + "  " + str(line[2]) + "  " + str(line[3]) + "  " + "$" + str(line[4]) + "\n"
                self.text_file.write(txt_line)
            self.text_file.close()
            
            #Close Connection
            conn.close()
        
        #Kills the application
        def iExit():
            iExit = tkinter.messagebox.askyesno("Validate Entry Widget", "Confirm if you want to exit")
            if iExit > 0:
                self.master.destroy()
                return
            
        #these are for the entry buttons
        #date button
        self.dateButton = tk.Button(Frame1, text="Select Date", font=("Gothic Bold", 15), bd=5, relief=tk.RAISED, padx=12, pady=12, command=SelectDate)
        self.dateButton.grid(row=5, column=0)
        
        #record button
        self.recordButton = tk.Button(Frame1, text="Record", font=("Gothic", 15), bd=5, relief=tk.RAISED, padx=12, pady=12, command=Record)
        self.recordButton.grid(row=7, column=1)

        #reset button
        self.resetButton = tk.Button(Frame1, text="Clear", font=("Gothic", 15), bd=5, relief=tk.RAISED, padx=12, pady=12, command=Reset)
        self.resetButton.grid(row=7, column=2)

        #search button
        self.searchButton = tk.Button(Frame1, text="Search", font=("Gothic", 15), bd=5, relief=tk.RAISED, padx=12, pady=12, command=Search)
        self.searchButton.grid(row=7, column=3)

        #export button
        self.exportButton = tk.Button(Frame1, text="Export", font=("Gothic Bold", 15), bd=5, relief=tk.RAISED, padx=12, pady=12, command=ExportTxt)
        self.exportButton.grid(row=9,column=6)

        #exit button
        self.ExitButton = tk.Button(Frame1, text="Exit", font=("Gothic Bold", 15), bd=5, relief=tk.RAISED, padx=12, pady=12, command=iExit)
        self.ExitButton.grid(row=9,column=2)  
        
#Second top level window
class StockDisplay:
    
    def __init__(self,second):
        self.second=second
        self.second.title("Activity Display")
        self.second.geometry("1000x550+700+50")
        self.second.configure(background='#A1CDEC')
        self.CreateWidgets()
        
    def CreateWidgets(self):
        Frame2 = tk.Frame(self.second, bg='#A1CDEC') #this is the second frame
        Frame2.grid()
        
        #this is the label for the title of the application
        self.mainLabel = tk.Label(Frame2, text="STOCK ACTIVITY DISPLAY", bd=2, relief="solid", font=("Lucida Grande", 30, "bold"), fg="black", bg="#990000")
        self.mainLabel.grid(row=0, column=3)
        
        self.oldTransLabel = tk.Label(Frame2, text="",font=("Lucida Grande", 17, 'bold'), fg="#333333")
        self.oldTransLabel.grid(row=6,column=3)

        self.newTransLabel = tk.Label(Frame2, text='',font=("Lucida Grande", 17, 'bold'), fg="#333333")
        self.newTransLabel.grid(row=7,column=3)

        self.uniqueStockLabel = tk.Label(Frame2, text="", font=("Lucida Grande", 17, 'bold'), fg="#333333")
        self.uniqueStockLabel.grid(row=8,column=3)

        self.cheapPriceLabel = tk.Label(Frame2, text="", font=("Lucida Grande", 17, 'bold'), fg="#333333")
        self.cheapPriceLabel.grid(row=9,column=3)

        self.expPriceLabel = tk.Label(Frame2, text="", font=("Lucida Grande", 17, 'bold'), fg="#333333")
        self.expPriceLabel.grid(row=10,column=3)

        self.popStockLabel = tk.Label(Frame2, text="",  font=("Lucida Grande", 17, 'bold'), fg="#333333")
        self.popStockLabel.grid(row=11,column=3)


        #Summary of Stock Activities
        def Summary():
            
            #Creates a database or connects to one  
            conn = sqlite3.connect('stocks.db')
        
            #Create cursor
            c = conn.cursor()
            
            #Oldest transaction
            self.oldest_transac = c.execute("SELECT symbol, MIN(date) FROM stocks")
            old_tran = c.fetchone()
            self.oldTransLabel.config(text=f"Oldest Transaction: {str(old_tran[0]) + ' ' + str(old_tran[1])}")
            
            #Newest transaction
            self.newest_transac = c.execute("SELECT symbol, MAX(date) FROM stocks")
            new_tran = c.fetchone()
            self.newTransLabel.config(text=f"Newest Transaction: {str(new_tran[0]) + ' ' + str(new_tran[1])}")
            
            #Unique stocks
            self.uniqueStock = c.execute("SELECT symbol, COUNT(symbol) FROM stocks where (trans='BUY' AND quantity > 0) OR (trans='SELL' AND quantity > 0) GROUP BY symbol")
            unique_stocks = c.fetchall()
            
            distinct_stocks = ''
            for row in unique_stocks:
                distinct_stocks += str(row[0]) + ' ' + str(row[1]) + ' '
            self.uniqueStockLabel.config(text=f"Unique Stocks: {str(distinct_stocks)}")
            
            #Cheapest price paid for any stock
            c.execute("SELECT symbol, MIN(price) FROM stocks WHERE trans='BUY' AND price > 0")
            chp_prc = c.fetchone()
            self.cheapPriceLabel.config(text=f"Cheapest Stock Price: {str(chp_prc[0]) + ' ' + '$' + str(chp_prc[1])}")
            
            #Most expensive price paid for any stock
            self.expensive_price = c.execute("SELECT symbol, MAX(price) FROM stocks WHERE trans='BUY'")
            exp_prc = c.fetchone()
            self.expPriceLabel.config(text=f"Most Expensive Stock Price: {str(exp_prc[0]) + ' ' + '$' + str(exp_prc[1])}")
            
            
            #Most traded stock
            self.popStock = c.execute("SELECT symbol, COUNT(symbol) FROM stocks GROUP BY symbol HAVING COUNT(symbol) IN (SELECT MAX(name) FROM (SELECT COUNT(symbol) as name FROM stocks GROUP BY symbol))")
            pop_stock = c.fetchone()
            self.popStockLabel.config(text=f"Most Traded Stock: {pop_stock[0]}")
            
            #Commit Changes
            conn.commit()
            
            #Close Connection
            conn.close()
            
             #Resets the display labels
        def SummaryReset():
            self.oldTransLabel.config(text="")
            self.newTransLabel.config(text="")
            self.uniqueStockLabel.config(text="")
            self.cheapPriceLabel.config(text="")
            self.expPriceLabel.config(text="")
            self.popStockLabel.config(text="")  
        
        #User's Stock Activities
        def Activity():
            #Creates a database or connects to one  
            conn = sqlite3.connect('stocks.db')
        
            #Create cursor
            c = conn.cursor()
            
            c.execute("SELECT * FROM stocks WHERE quantity > 0 ORDER BY date")
            activities = c.fetchall()
            
            stock_activities = ''
            for activity in activities:
                stock_activities += str(activity[0]) + " " + str(activity[1]) + " " + str(activity[2]) + " " + str(activity[3]) + " " + str(activity[4]) + "\n"
                
            self.stockActivityLabel = tk.Label(Frame2, text=stock_activities, font=("Lucida Grande", 17, 'bold'), fg="#333333")
            self.stockActivityLabel.grid(row=5,column=4)
            
            #Commit Changes
            conn.commit()
            
            #Close Connection
            conn.close()
            
        #Activiy Reset Button   
        def ActivityReset():
            self.stockActivityLabel.config(text="")

       
        
        #Kill application
        def iExit():
            iExit = tkinter.messagebox.askyesno("Validate Display Widget", "Confirm if you want to exit")
            if iExit > 0:
                self.second.destroy()
                
        
        #Summary Button
        self.summaryButton = tk.Button(Frame2, text="STOCK SUMMARY", font=("Gothic Bold", 15), bd=5, relief=tk.RAISED, padx=12, pady=12, command=Summary)
        self.summaryButton.grid(row=3, column=3)        
        
        #Activities Button
        self.activityButton = tk.Button(Frame2, text="STOCK ACTIVITIES", font=("Gothic Bold", 15), bd=5, relief=tk.RAISED, padx=12, pady=12, command=Activity)
        self.activityButton.grid(row=3,column=4)
        
        #Stock activity Reset Button
        self.activityResetButton = tk.Button(Frame2, text="Activity Reset", font=("Gothic", 15), bd=5, relief=tk.RAISED, padx=12, pady=12, command=ActivityReset)
        self.activityResetButton.grid(row=4,column=4)
        
        #Stock Summary Reset Button
        self.summaryResetButton = tk.Button(Frame2, text="Summary Reset", font=("Gothic", 15), bd=5, relief=tk.RAISED, padx=12, pady=12, command=SummaryReset)
        self.summaryResetButton.grid(row=4, column=3)
        
        #Exit Button
        self.exitButton = tk.Button(Frame2, text="EXIT", font=("Gothic Bold", 15), bd=5, relief=tk.RAISED, padx=12, pady=12, command=iExit)
        self.exitButton.grid(row=5,column=2)

        
        
        
    
#Main Function        
def main():
    
    #Creates a database or connects to one
    conn = sqlite3.connect('stocks.db')
    
    #Create cursor
    c = conn.cursor()
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS stocks
                (date text, 
                symbol text, 
                trans text,
                quantity integer,
                price real)''')
    
    #Commit changes
    conn.commit()
    
    #Close Connection
    conn.close()
    
    master = tk.Tk()
    second = tk.Tk()
    
    app1 = StockEntry(master)
    app2 = StockDisplay(second)
        
    master.mainloop()
    second.mainloop()
    
    
if __name__ == '__main__':
    main()
        