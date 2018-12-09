

import db
import tkinter as tk
from tkinter import ttk
from objects import Item


class ThanksMessage(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding = "10 10 10 10")
        self.parent = parent

        ttk.Label(parent, text="Thank you for shopping with us!\nHave a Great Day!").grid(
            column=0, row=0, columnspan=2, pady=10)
        ttk.Button(parent, text="Exit", command=parent.destroy).grid(row=1,
            column=0, sticky=tk.E)


class confirmRemoveMessage(ttk.Frame):
    def __init__(self, parent, removeFrame):
        ttk.Frame.__init__(self, parent, padding = "10 10 10 10")
        self.parent = parent

        ttk.Label(parent, text="Are you sure you would like to remove that item from the database?").grid(
                column=0, row=0, columnspan=2, pady=10)

        ttk.Button(parent, text="Yes", command= lambda: self.doubleFunct(removeFrame)).grid(row=1,
            column = 0)
        ttk.Button(parent, text="No", command=parent.destroy).grid(row=1,
            column = 1)

    def doubleFunct(self, frame):
        removeFrame.remove(frame)
        self.parent.destroy()

class confirmMessage(ttk.Frame):
    def __init__(self, parent, removeAdd):
        ttk.Frame.__init__(self, parent, padding = "10 10 10 10")
        self.parent = parent

        if removeAdd == 0:
            ttk.Label(parent, text="Item was removed from database.").grid(
                column=0, row=0)
        else:
            ttk.Label(parent, text="Item was added to database").grid(
                column=0, row=0)
        ttk.Button(parent, text="OK", command=parent.destroy).grid(row=1,
        column = 0)

class errorMessage(ttk.Frame):
    def __init__(self, parent, removeAdd):
        ttk.Frame.__init__(self, parent, padding = "10 10 10 10")
        self.parent = parent

        if removeAdd == 0:
            ttk.Label(parent, text="Item may not be empty").grid(
            column=0, row=0)
        elif removeAdd == 1:
            ttk.Label(parent, text="Item or Cost may not be empty").grid(
            column=0, row=0)
        elif removeAdd == 2:
            ttk.Label(parent, text="Item is not contained in List").grid(
            column=0, row=0)
        elif removeAdd == 3:
            ttk.Label(parent, text="Item is already contained in List").grid(
            column=0, row=0)
        
        ttk.Button(parent, text="OK", command=parent.destroy).grid(row=1,
        column = 0)

class ShoppingCart(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding = "10 10 10 10")
        self.parent = parent

        buttonFrame = ttk.Frame()
        buttonFrame.grid(column=0, row=1, columnspan=2, sticky=tk.S)
        
        ttk.Button(buttonFrame, text="Exit", command=parent.destroy).grid(row=1,
        column = 0)
        ttk.Button(buttonFrame, text="Checkout", command=self.checkout).grid(row=1,
        column = 1)
        
        addFrame(parent).grid(row=0,column=0)

    def checkout(self):
        self.parent.destroy()
        table = db.getList()
        total = 0.0
        for item in table:
            total += float(item.cost)
            #print("{0:.2f}".format(total)) #debugging
        checkout = tk.Tk()
        checkout.title("Checkout")
        checkout.geometry("205x300")
        checkoutWindow(checkout, total)

class checkoutWindow(ttk.Frame):
    def __init__(self, parent, total):
        ttk.Frame.__init__(self, parent, padding = "10 10 10 10")
        self.parent = parent
        
        self.total = tk.StringVar()
        total = "{0:.2f}".format(total)
        self.total.set(total)

        contentsFrame = ttk.Frame(parent)
        contentsFrame.grid(column=0, row=0, columnspan=2, sticky=tk.E)
        listFrame = ttk.Frame(parent)
        listFrame.grid(column=0, row=1, columnspan=2, pady=10, sticky='')

        ttk.Label(listFrame, text="Your items were:").grid(
            column=0, row=0, pady=10, sticky='')

        self.displayList(db.getList(), listFrame)
    

        ttk.Label(contentsFrame, text="The total of your cart is:").grid(
            column=0, row=0, pady=10, sticky='')
        ttk.Label(contentsFrame, text=self.total.get()).grid(
            column=0, row=1, pady=10, sticky='')
        ttk.Label(contentsFrame, text="Would you like to checkout?").grid(
            column=0, row=2, pady=10, sticky='')
        
        ttk.Button(parent, text="Yes", command=self.yes).grid(row=2,
            column = 0)
        ttk.Button(parent, text="No", command=self.restartCart).grid(row=2,
            column = 1, sticky=tk.E)

    def displayList(self, list, contentsFrame):
        i = 1
        for item in list:
            contents = (item.name + "| $" + "{0:.2f}".format(item.cost))
            ttk.Label(contentsFrame, text=contents).grid(
                column=0, row=i, sticky=tk.W)
            i += 1

    def yes(self):
        self.parent.destroy()
        thanks = tk.Tk()
        thanks.title("Thanks for shopping with us!")
        thanks.geometry("220x100")
        ThanksMessage(thanks)

    def restartCart(self):
        self.parent.destroy()
        root = tk.Tk()
        root.title("Shopping Cart")
        root.geometry("375x200")
        ShoppingCart(root)
        root.mainloop()

        
class listFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent

        parent.geometry("215x400")
        
        #change window buttons
        ttk.Button(self, text="Add", command=self.changeAdd).grid(column=0, row=1)
        ttk.Button(self, text="Remove", command=self.changeRemove).grid(column=1, row=1)

        self.initComponents()
        #print(db.getList())

    def initComponents(self):
        #init all 'list' window components here
        #contents frame
        contentsFrame = ttk.Frame(self)
        contentsFrame.grid(column=0, row=0, columnspan=2, sticky='')

        #item list
        ttk.Label(contentsFrame, text="List:").grid(
            column=0, row=0, pady=10, sticky=tk.N)
        self.displayList(db.getList(), contentsFrame)

    def displayList(self, list, contentsFrame):
        i = 1
        for item in list:
            contents = (item.name + "| $" + "{0:.2f}".format(item.cost))
            ttk.Label(contentsFrame, text=contents).grid(
                column=0, row=i, sticky=tk.W)
            i += 1
        
    def changeAdd(self):
        self.grid_remove()
        addFrame(self.parent).grid(row=0, column=0)

    def changeRemove(self):
        self.grid_remove()
        removeFrame(self.parent).grid(row=0, column=0)
        
            
class addFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent

        parent.geometry("375x200")

        #textvariables
        self.item = tk.StringVar()
        self.cost = tk.StringVar()

        #change window buttons
        ttk.Button(self, text="List", command=self.changeList).grid(column=1, row=1)
        ttk.Button(self, text="Remove", command=self.changeRemove).grid(column=2, row=1)

        self.initComponents()

    def initComponents(self):
        #contents frame
        contentsFrame = ttk.Frame(self)
        contentsFrame.grid(column=0, row=0, columnspan=2, sticky=tk.E)
        
        #item name
        ttk.Label(contentsFrame, text="Item:").grid(
            column=0, row=0, sticky=tk.E)
        ttk.Entry(contentsFrame, width=25, textvariable=self.item).grid(
            column=1, row=0, sticky=tk.E)        

        #item cost
        ttk.Label(contentsFrame, text="Cost:").grid(
            column=0, row=1, sticky=tk.E)
        ttk.Entry(contentsFrame, width=25, textvariable=self.cost).grid(
            column=1, row=1, sticky=tk.E)

        #make the shop buttons
        buttonFrame = ttk.Frame(contentsFrame)
        buttonFrame.grid(column=0, row=2, columnspan=2, sticky=tk.E)
        
        ttk.Button(buttonFrame, text="Confirm", command=self.addItem).grid(column=0, row=0)
        ttk.Button(buttonFrame, text="Clear", command=self.clear).grid(column=1, row=0)
        
    def clear(self):
        self.item.set("")
        self.cost.set("")

    def addItem(self):
        if self.item.get() != "" and self.cost.get() != "":
            #print(self.item.get()) #debugging
            #print(self.cost.get()) #debugging
            self.checkDouble()
            
        else:
            error = tk.Tk()
            error.title("Error")
            error.geometry("215x60")
            errorMessage(error, 1)
            
    def checkDouble(self):
        double = db.getItem(self.item.get())
        if double == True:
            error = tk.Tk()
            error.title("Error")
            error.geometry("215x60")
            errorMessage(error, 3)
        else:
            item = Item(self.item.get(), self.cost.get())
            db.addItem(item)
            confirm = tk.Tk()
            confirm.title("Confirmation")
            confirm.geometry("215x60")
            confirmMessage(confirm, 1)
        
    def changeList(self):
        self.grid_remove()
        listFrame(self.parent).grid(row=0, column=0)

    def changeRemove(self):
        self.grid_remove()
        removeFrame(self.parent).grid(row=0, column=0)
        

class removeFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent

        parent.geometry("375x200")
        
        #change window buttons
        ttk.Button(self, text="Add", command=self.changeAdd).grid(column=0, row=1)
        ttk.Button(self, text="List", command=self.changeList).grid(column=1, row=1)

        #text variable
        self.item = tk.StringVar()

        self.initComponents()

    def initComponents(self):
        #init all 'list' window components here
        #contents frame
        contentsFrame = ttk.Frame(self)
        contentsFrame.grid(column=0, row=0, columnspan=2, sticky=tk.E)
        
        #item name
        ttk.Label(contentsFrame, text="Item:").grid(
            column=0, row=0, sticky=tk.E)
        ttk.Entry(contentsFrame, width=25, textvariable=self.item).grid(
            column=1, row=0, sticky=tk.E)

        #make the shop buttons
        buttonFrame = ttk.Frame(contentsFrame)
        buttonFrame.grid(column=0, row=2, columnspan=2, sticky=tk.E)
        
        ttk.Button(buttonFrame, text="Confirm", command=self.removeItem).grid(column=0, row=0)
        ttk.Button(buttonFrame, text="Clear", command=self.clear).grid(column=1, row=0)
        
        
    def clear(self):
        self.item.set("")
        self.cost.set("")

    def remove(self):
        #print("doneeee") #debugging
        db.removeItem(self.item.get())
        confirm = tk.Tk()
        confirm.title("Confirmation")
        confirm.geometry("215x60")
        confirmMessage(confirm, 0)

    def removeItem(self):
        #start of complicated method to display diologue boxes to delete items
        if self.item.get() != "":
            #print(self.item.get()) #debugging
            #print(db.ConfirmDelete(self.item.get())) #debugging
            if db.ConfirmDelete(self.item.get()) == False:
                self.confirmRemove()
            else:
                error = tk.Tk()
                error.title("Does not exist")
                error.geometry("215x60")
                errorMessage(error, 2)
        else:
            print("error")
            error = tk.Tk()
            error.title("Error")
            error.geometry("215x60")
            errorMessage(error, 0)

    def confirmRemove(self):
        #print("Remove") #debugging
        confirm = tk.Tk()
        confirm.title("Removal Confirmation")
        confirm.geometry("470x100")
        confirmRemoveMessage(confirm, self)
        
    def changeAdd(self):
        self.grid_remove()
        addFrame(self.parent).grid(row=0, column=0)

    def changeList(self):
        self.grid_remove()
        listFrame(self.parent).grid(row=0, column=0)
    
if __name__ == "__main__":
    db.connect()
    root = tk.Tk()
    root.title("Shopping Cart")
    root.geometry("375x200")
    ShoppingCart(root)
    root.mainloop()
    db.close()
    print("bye") #  :)
