import tkinter.messagebox
from tkinter import *
import requests
import csv
import json
import pandas as pd
import random
import os
import pandas
THEME_COLOR = "#375362"

class FrontPage:
    def __init__(self):
        self.window=Tk()
        self.window.title('Stock Checker')
        self.user_name=None
        self.window.geometry("400x300")
        self.window.config(background=THEME_COLOR)
        # -------------- CANVAS
        self.logo_canvas=Canvas(height=50,width=50,background=THEME_COLOR)
        self.logo_canvas.grid(row=0,column=0,padx=20,pady=20,columnspan=2)
        # -------------- LOGO
        self.logo=Label(text='STOCK CHECK',background='white',font=('Ariel',20,'bold'),bg=THEME_COLOR)
        self.logo.place(x=120,y=30)
        # -------------- BUTTONS
        self.user_login_button=Button(text='Login', background=THEME_COLOR, font=('Ariel',15), pady=20, padx=20, command=self.login_accepted)
        self.user_login_button.grid(row=3,column=0)
        self.user_register_button=Button(text='Register',background=THEME_COLOR,font=('Ariel',15),pady=20,padx=20,command=self.register_button)
        self.user_register_button.grid(row=3,column=1)

        # -------------- ENTRIES
        self.user_name_label=Label(text='Username',fg='white',background=THEME_COLOR,highlightthickness=0)
        self.user_name_label.grid(column=0,row=1)
        self.user_name_input=Entry()
        self.user_name_input.insert(0,'Username')
        self.user_name_input.grid(column=0,row=2,pady=20,padx=5)
        self.password_text=Label(text='Password',fg='white',background=THEME_COLOR,highlightthickness=0)
        self.password_text.grid(column=1,row=1,columnspan=2)
        self.password_entry=Entry(show='*')
        self.password_entry.insert(0,'Password')
        self.password_entry.grid(column=1,row=2)


        self.window.mainloop()

    def register_button(self):
        self.user_name=self.user_name_input.get()
        self.user_password=self.password_entry.get()


        user_details={
            'user_id':random.randint(0,1000),
            'username':self.user_name,
            'password':self.user_password
        }
        panda_df = pd.DataFrame(user_details,index=[0])
        try:
            with open ('./database/user_database.csv',mode='a') as file:
                panda_df.to_csv(file,index=False)
        except OSError:
            # panda_df = pd.DataFrame(user_details, orient='index')
            panda_df.to_csv('./database/user_database.csv', mode='w',index=False)


        # if data[data['username']==self.user_name_input]:
        #     print('login accepted')




    def login_accepted(self):
        user_name=self.user_name_input.get()
        user_password=self.password_entry.get()
        data = pd.read_csv('./database/user_database.csv')
        if user_name in data['username'].values and user_password in data['password'].values :
            self.destroy_widgets()
            secondpage=SecondPage(self.window,user_name)

        else:
            tkinter.messagebox.showerror(title='Not found',message='User details not found')

    def destroy_widgets(self):
        self.logo.destroy()
        self.logo_canvas.destroy()
        self.user_name_input.destroy()
        self.user_name_label.destroy()
        self.password_entry.destroy()
        self.password_text.destroy()
        self.user_login_button.destroy()
        self.user_register_button.destroy()




class SecondPage:
    def __init__(self, second_window,username):

        self.second_window = second_window
        self.username=username


        self.second_window.config(background=THEME_COLOR, width=300, height=400, padx=20)

        # -------------- LOGO CANVAS
        self.logo_canvas = Canvas(self.second_window, height=50, width=50, background=THEME_COLOR)
        self.logo_canvas.place(x=160,y=40)

        # -------------- LOGO
        self.logo = Label(self.second_window, text='STOCK CHECK', background='white', font=('Ariel', 20, 'bold'), bg=THEME_COLOR)
        self.logo.place(x=110,y=50)
        self.welcome_user_label = Label(self.second_window, text=f'Welcome\n{username}', font=('Ariel', 15),
                                bg=THEME_COLOR, fg='white')
        self.welcome_user_label.place(x=0,y=50)

        # Start the mainloop of the window
        #  logout button
        self.logout_button = Button(self.second_window, text="Logout", command=self.logout,highlightthickness=0)
        self.logout_button.place(x=300,y=60)
        # -----------Buttons

        self.stock_add_button = Button(text='Add Stock',font=(50),height=2,width=5,padx=20,pady=10,command=self.add_button,highlightthickness=0)
        self.stock_add_button.place(x=150,y=220)

        self.create_search_button()

    def create_search_button(self):
        self.search_entry=Entry(self.second_window,width=20)
        self.search_entry.insert(0,'Type Product SKU')
        self.search_entry.place(x=90,y=130)
        self.search_button = Button(self.second_window,height=2,width=5,padx=20,pady=5, text="Search", command=self.perform_search,
                                    highlightthickness=0)
        self.search_button.place(x=150,y=170)

    def perform_search(self):
        query = self.search_entry.get()
        SearchPage(self.second_window,self.username,query)
        # query = self.search_entry.get()
        #
        # result = requests.get(url='https://api.sheety.co/0183eb27eded6d48cdbf2d53b83ddf3c/stockapp/sheet1')
        # search_data=result.json()
        #
        # for data in search_data['sheet1']:
        #     if query == data['productCode']:
        #         print(data)


    def add_button(self):
        AddStockPage(self.second_window,self.username)


    def logout(self):
        # Close the second window and return to the front page
        self.second_window.destroy()
        FrontPage()

        self.second_window.mainloop()

class AddStockPage:
    def __init__(self,add_window,username):
        self.add_window=add_window
        self.username=username
        self.added_stock={}
        new_window=Toplevel(self.add_window)
        new_window.title('Add Stock')
        new_window.geometry('300x520')
        new_window.config(background=THEME_COLOR,padx=10, pady=10)
        # -------LABELS nd fields-----
        label = Label(new_window, text='ADD DETAILS OF THE PRODUCT')
        self.product_name_label = Label(new_window,text='Product Name:', background=THEME_COLOR,fg='white')
        self.product_name_label.place(x=30,y=50)
        self.product_name=Entry(new_window)
        self.product_name.place(x=35,y=70,width=170)

        self.product_code_label = Label(new_window, text='Product Code/SKU:', background=THEME_COLOR, fg='white')
        self.product_code_label.place(x=30, y=100)
        self.product_code = Entry(new_window)
        self.product_code.place(x=35, y=120, width=170)

        self.product_quantity_label = Label(new_window, text='Product Quantity:', background=THEME_COLOR, fg='white')
        self.product_quantity_label.place(x=30, y=150)
        self.product_quantity = Entry(new_window)
        self.product_quantity.place(x=35, y=170, width=170)

        self.stock_quantity_label = Label(new_window, text='Quantity in stock:', background=THEME_COLOR, fg='white')
        self.stock_quantity_label.place(x=30, y=200)
        self.stock_quantity = Entry(new_window)
        self.stock_quantity.place(x=35, y=220, width=170)

        self.min_stock_level_label = Label(new_window, text='Minimum stock level:', background=THEME_COLOR, fg='white')
        self.min_stock_level_label.place(x=30, y=250)
        self.min_stock_level = Entry(new_window)
        self.min_stock_level.place(x=35, y=270, width=170)

        self.cost_label = Label(new_window, text='Cost Price:', background=THEME_COLOR, fg='white')
        self.cost_label.place(x=30, y=300)
        self.cost_price = Entry(new_window)
        self.cost_price.place(x=35, y=320, width=170)

        self.selling_price = Label(new_window, text='Selling Price:', background=THEME_COLOR, fg='white')
        self.selling_price.place(x=30, y=350)
        self.selling_price = Entry(new_window)
        self.selling_price.place(x=35, y=370, width=170)

        self.custom_field_label = Label(new_window, text='Custom Field:', background=THEME_COLOR, fg='white')
        self.custom_field_label.place(x=30, y=400)
        self.custom_field = Entry(new_window)
        self.custom_field.place(x=35, y=420, width=170)

        label.pack()

        # submit Button --------
        self.submit_button=Button(new_window,text='Submit',command=self.write_data_to_csv)
        self.submit_button.place(x=70, y=470)

        new_window.mainloop()


    def write_data_to_csv(self):
        data = {'Product Name': [self.product_name.get()],
                'Product Code/SKU': [self.product_code.get()],
                'Product Quantity': [self.product_quantity.get()],
                'Quantity in stock': [self.stock_quantity.get()],
                'Minimum stock level': [self.min_stock_level.get()],
                'Cost Price': [self.cost_price.get()],
                'Selling Price': [self.selling_price.get()],
                'Custom Field': [self.custom_field.get()],
                'Employee':[self.username]}

        df = pd.DataFrame(data)
        df.to_csv('./database/product_data.csv', mode='a', index=False, header=not os.path.exists('./database/product_data.csv'))
        self.write_to_sheety()


    def write_to_sheety(self):
        with open('./database/product_data.csv') as file:
            reader = csv.DictReader(file)
            data = list(reader)

            for row in data:

                sheety_data = {
                    "sheet1": [{
                        "ProductName": row['Product Name'],
                        "ProductCode": row['Product Code/SKU'],
                        "ProductQuantity": row['Product Quantity'],
                        "QuantityStock": row['Quantity in stock'],
                        "MinimumStock": row['Minimum stock level'],
                        "CostPrice": row['Cost Price'],
                        "SellingPrice": row['Selling Price'],
                        "CustomField": row['Custom Field'],
                        "Employee": row['Employee']
                    }]
                }

                headers = {
                    "Content-Type": "application/json"
                }

            result=requests.post(url='https://api.sheety.co/0183eb27eded6d48cdbf2d53b83ddf3c/stockapp/sheet1',
                                   json=sheety_data)
            print(result.content)


class SearchPage:
    def __init__(self,add_window,username,query):
        self.add_window=add_window
        self.username=username
        self.added_stock={}
        new_window=Toplevel(self.add_window)
        new_window.title('Add Stock')
        new_window.geometry('360x400')
        new_window.config(background=THEME_COLOR,padx=10, pady=10)
    # SEARCH PAGE

        result = requests.get(url='https://api.sheety.co/0183eb27eded6d48cdbf2d53b83ddf3c/stockapp/sheet1')
        search_data = result.json()
        self.searched_data={}
        for data in search_data['sheet1']:
            if query == data['productCode']:
                self.searched_data=data

        print(self.searched_data)


        label = Label(new_window, text=f'Hello {self.searched_data["employee"]}')

        label.pack()
        # Widgets

        self.sold_amount = Label(new_window, text='How many sold ?:', background=THEME_COLOR, fg='white')
        self.sold_amount.place(x=30, y=50)

        self.spinbox = Spinbox(new_window,from_=0, to=int(self.searched_data["quantityStock"]), width=5)
        self.spinbox.place(x=35, y=70, width=170)

        self.product_code_label = Label(new_window, text=f'product Code: {self.searched_data["productCode"]}', background=THEME_COLOR, fg='white')
        self.product_code_label.place(x=30, y=100)


        self.product_quantity_label = Label(new_window, text=f'Product Quantity: {self.searched_data["productQuantity"]}', background=THEME_COLOR, fg='white')
        self.product_quantity_label.place(x=30, y=150)


        self.stock_quantity_label = Label(new_window, text=f'Quantity in stock: {self.searched_data["quantityStock"]}', background=THEME_COLOR, fg='white')
        self.stock_quantity_label.place(x=30, y=200)

        self.min_stock_level_label = Label(new_window, text=f'Minimum stock level:{self.searched_data["minimumStock"]}', background=THEME_COLOR, fg='white')
        self.min_stock_level_label.place(x=30, y=250)

        self.cost_label = Label(new_window, text=f'Cost Price: {self.searched_data["costPrice"]}', background=THEME_COLOR, fg='white')
        self.cost_label.place(x=30, y=300)

        self.submit_button = Button(new_window, text='Submit',command=self.submit)
        self.submit_button.place(x=70, y=350)


    def submit(self):

        self.searched_data=self.searched_data
        self.updated_amount=self.searched_data['quantityStock']-int(self.spinbox.get())
        print(self.updated_amount)
        updated_data={
            "sheet1": [{
                "ProductName": self.searched_data['productName'],
                "ProductCode": self.searched_data['productCode'],
                "ProductQuantity": self.searched_data['productQuantity'],
                "QuantityStock": self.updated_amount,
                "MinimumStock": self.searched_data['minimumStock'],
                "CostPrice": self.searched_data['costPrice'],
                "SellingPrice": self.searched_data['sellingPrice'],
                "CustomField": self.searched_data['customField'],
                "Employee": self.searched_data['employee']
            }]
        }

        result = requests.put(url=f'https://api.sheety.co/0183eb27eded6d48cdbf2d53b83ddf3c/stockapp/sheet1/{self.searched_data["id"]}',
                               json=updated_data)

        tkinter.messagebox.showinfo(title='Updated',message='Updated Succesfully')




